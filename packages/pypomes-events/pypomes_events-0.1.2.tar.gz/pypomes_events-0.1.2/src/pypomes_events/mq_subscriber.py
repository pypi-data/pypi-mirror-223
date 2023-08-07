from typing import Any, Final
from pika import frame as Frame
from pika import spec as Spec
from pika import SelectConnection, URLParameters
from pika.channel import Channel
from pika.connection import Connection
from pika.exchange_type import ExchangeType
import logging
import time
import threading

MQS_CONNECTION_OPEN: Final[int] = 1
MQS_CONNECTION_CLOSED: Final[int] = 2
MQS_CONNECTION_ERROR: Final[int] = -1
MQS_INITIALIZING: Final[int] = 0


class _MqSubscriber:
    """
    Consumidor que lidará com as interações com o *RabbitMQ*, em modo de multi-processamento,
    resolvendo situações inesperadas como fechamento de canal e de conexão.

    Se o *RabbitMQ* fechar a conexão, esse objeto irá parar e indicar que a reconexão é necessária.
    Nesse caso, deve-se examinar o log da execução, pois as razões pelas quais a conexão pode ser
    fechada são limitadas, e geralmente estão vinculados a problemas relacionados a permissões
    ou a *timeout* de *sockets*. Se o canal for fechado, isso indicará um problema com um dos comandos
    que foram emitidos.
    """
    # instance attributes
    should_reconnect: bool
    started_consumption: bool
    mq_url: str
    exchange_name: str
    exchange_type: ExchangeType | str
    queue_name: str
    msg_target: callable
    logger: logging.Logger
    closing: bool
    consuming: bool
    prefetch_count: int
    consumer_tag: str | None
    channel: Channel | None
    state: int
    state_msg: str

    # 'Any', em lugar de 'None', evita o alerta "Cannot find reference 'ioloop' in 'Connection'"
    conn: Connection | Any

    def __init__(self, mq_url: str, exchange_name: str, exchange_type: str,
                 queue_name: str, msg_target: callable, logger: logging.Logger = None) -> None:
        """
        Cria uma nova instância do consumidor, com os parâmetros necessários para a interação com o *RabbitMQ*.

        :param mq_url: a URL usada para a conexão
        :param msg_target: a função a ser a quem as mensagens seráo entregues
        :param logger: o logger para registro das operações
        :param exchange_name: o nome do comutador
        :param exchange_type: o tipo do comutador
        :param queue_name: o nome da fila
        :param msg_target: a função callback o ser chamada
        :param logger: o agente pats logging das operações
        """
        self.state = MQS_INITIALIZING
        self.state_msg = "Attenpting to initialize the subscriber"
        self.mq_url = mq_url
        self.msg_target = msg_target
        self.logger = logger

        self.exchange_name = exchange_name
        match exchange_type:
            case "direct":
                self.exchange_type = ExchangeType.direct
            case "fanout":
                self.exchange_type = ExchangeType.fanout
            case "headers":
                self.exchange_type = ExchangeType.headers
            case _:  # 'topic'
                self.exchange_type = ExchangeType.topic

        self.queue_name = queue_name

        self.started_consumption = False
        self.should_reconnect = False
        self.consuming = False
        self.closing = False

        self.conn = None
        self.channel = None
        self.consumer_tag = None

        # parâmetro para o QOS do canal - para maior rendimento na produção, experimente valores mais altos
        self.prefetch_count = 1
        self.logger.info("Instanciado, com comutador "
                         f"'{exchange_name}' tipo '{exchange_type}', e fila '{queue_name}'")

    def run(self) -> None:
        """
        Executa o consumidor, conectando-o ao *RabbitMQ* e depois
        iniciando o *IOLoop* para bloquear e permitir que o *SelectConnection* opere.
        """
        self.conn = self.connect()
        self.conn.ioloop.start()

    def connect(self) -> Connection:
        """
        Conecta com o *RabbitMQ*, retornando o identificador da conexão.
        Quando a conexão for estabelecida, o método *on_connection_open* será invocado por *pika*.

        :return: a conexão obtida
        """
        # suprime usuário e senha da url no log
        #   url: <protocol>//<user>:<password>@<ip-address>
        first: int = self.mq_url.find("//")
        last = self.mq_url.find("@")
        self.logger.info(f"Conectando com '{self.mq_url[0:first]}{self.mq_url[last:]}'")

        # obtem e retorna a conexão
        return SelectConnection(
            parameters=URLParameters(self.mq_url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed)

    def on_connection_open(self, _unused_connection: Connection) -> None:
        """
        Callback chamado quando a conexão com *RabbitMQ* é estabelecida.
        O identificador para o objeto de conexão é passado, para o caso em que faça necessário.
        No momento, ele é apenas marcado como não utilizado.

        :param _unused_connection: a conexão com o RabbitMQ
        """
        self.state = MQS_CONNECTION_OPEN
        msg: str = f"Connection established: queue '{self.queue_name}'"
        self.state_msg = msg
        if self.logger is not None:
            self.logger.info(msg)
        self.open_channel()

    def on_connection_open_error(self, _unused_connection: Connection, error: str) -> None:
        """
        Invocado por *pika* se a conexão com o *RabbitMQ* não puder ser estabelecida.

        :param _unused_connection: a conexão tentada com o RabbitMQ
        :param error: a mensagem de erro
        """
        self.state = MQS_CONNECTION_ERROR
        msg: str = f"Error attempting to connect: {error}"
        self.state_msg = msg
        if self.logger is not None:
            self.logger.error(msg)
        self.reconnect()

    def on_connection_closed(self, _unused_connection: Connection, reason: Exception) -> None:
        """
        Invocado por pika quando a conexão com o *RabbitMQ* é inesperadamente fechada.
        Nesse caso, a reconexão é tentada.

        :param _unused_connection: a conexão fechada inesperadamente
        :param reason: exceção representando o motivo para a perda da conexão
        """
        self.state = MQS_CONNECTION_CLOSED
        msg: str = f"Connection was closed: {reason}"
        self.state_msg = msg
        if self.logger is not None:
            self.logger.warning(msg)
        self.channel = None
        if self.closing:
            self.conn.ioloop.stop()
        else:
            self.reconnect()

    def close_connection(self) -> None:
        """
        Fecha a conexão com o RabbitMQ.
        """
        self.consuming = False
        if self.conn.is_closing:
            self.logger.info("Conexão em processo de fechamento")
        elif self.conn.is_closed:
            self.logger.info("Conexão já fechada")
        else:
            self.logger.info("Fechando a conexão")
            self.conn.close()

    def reconnect(self) -> None:
        """
        Invocado por *pika* se a conexão não puder ser aberta, ou se estiver fechada.
        Indica que uma reconexão é necessária e, em seguida, interrompe a ioloop.
        """
        self.should_reconnect = True
        self.stop()

    def open_channel(self) -> None:
        """
        Abre um novo canal com *RabbitMQ*, emitindo o comando RPC *Channel.Open*.
        Quando o *RabbitMQ* responde que o canal está aberto, o
        método indicado em *on_channel_open_callback* será invocado por *pika*.
        """
        self.logger.info("Criando um novo canal")
        self.conn.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel: Channel) -> None:
        """
        Invocado por *pika* quando o canal for aberto.
        O objeto do canal é passado, para que possa ser usado, se necessário.
        Com o canal agora aberto, o comutador a ser usado é declarado.

        :param channel: O canal que foi aberto
        """
        self.logger.info("O canal foi aberto, estabelecendo o callback no fechamento do canal")
        self.channel = channel
        self.channel.add_on_close_callback(self.on_channel_closed)
        self.setup_exchange()

    def on_channel_closed(self, channel: Channel, reason: Exception) -> None:
        """
        Invocado por *pika* quando *RabbitMQ* fechar inesperadamente o canal.
        Os canais geralmente são fechados quando se tenta fazer algo que
        viola o protocolo, como declarar novamente um comutador ou fila com
        parâmetros diferentes. Neste caso, a conexão é fechada para shutdown do objeto.

        :param channel: o canal que foi fechado
        :param reason: a razão para o fechamento do canal
        """
        self.logger.warning(f"O canal '{channel}' foi fechado: {reason}")
        self.close_connection()

    def setup_exchange(self) -> None:
        """
        Verifica se o comutador está configurada no *RabbitMQ*, invocando o comando RPC *Exchange.Declare*
        com o parametro *passive=True*. Se essa configuração for confirmada, *on_exchange_declare_ok*
        será invocado por *pika*.
        """
        self.logger.info(f"Declarando o comutador: '{self.exchange_name}'")
        self.channel.exchange_declare(exchange=self.exchange_name,
                                      exchange_type=self.exchange_type,
                                      passive=True,
                                      durable=True,
                                      callback=self.on_exchange_declare_ok)

    def on_exchange_declare_ok(self, _unused_frame: Frame.Method) -> None:
        """
        Invocado por *pika* quando o RabbitMQ concluir o comando RPC *Exchange.Declare*.

        :param _unused_frame: Exchange.DeclareOk response frame
        """
        self.logger.info(f"Comutador declarado: '{self.exchange_name}")
        self.setup_queue()

    def setup_queue(self) -> None:
        """
        Verifica se a fila está configurada no RabbitMQ invocando o comando RPC *Queue.Declare*
        com o parâmetro "passive=True". Se essa configuração for confirmada, *on_queue_declare_ok*
         será invocado por *pika*.
        """
        self.logger.info(f"Declarando a fila '{self.queue_name}'")
        self.channel.queue_declare(queue=self.queue_name,
                                   passive=True,
                                   durable=True,
                                   callback=self.on_queue_declare_ok)

    def on_queue_declare_ok(self, _unused_frame: Frame.Method) -> None:
        """
        Invocado por *pika* quando a chamada RPC *Queue.Declare* feito em setup_queue for concluído.
        Aqui se enlaça a fila e o exchange, com a chave de roteamento, pela emissão do comando RPC *Queue.Bind*.
        Quando esse enlace for concluído *on_bind_ok* será invocado por *pika*.

        :param _unused_frame: o frame Queue.DeclareOk
        """
        self.logger.info(f"Feito enlace entre comutador '{self.exchange_name}' e fila '{self.queue_name}'")
        self.setup_qos()

    def setup_qos(self) -> None:
        """
        Configura o prefetch do consumidor, definindo-se o número máximo de mensagens a serem entregues,
        pendentes as declaração de recebimento. Nesse caso, o consumidor deve sempre declarar ao RabbitMQ^^ o
        recebimento de cada mensagem. Deve-se experimentar diferentes valores de *prefetch*, para se alcançar o
        desempenho desejado.
        """
        self.channel.basic_qos(prefetch_count=self.prefetch_count,
                               callback=self.on_basic_qos_ok)

    def on_basic_qos_ok(self, _unused_frame: Frame.Method) -> None:
        """
        Invocado por pika quando o método *Basic.QoS* for concluído. Neste ponto, inicia-se o
        consumo de mensagens chamando *start_consuming*, que invocará os comandos RPC necessários
        para iniciar o processo.

        :param _unused_frame: o frame de response Basic.QosOk
        """
        self.logger.info(f"QOS configurado para {self.prefetch_count}")
        self.start_consuming()

    def start_consuming(self) -> None:
        """
        Configura o consumidor, chamando primeiramente *add_on_cancel_callback* no canal,
        para que o consumidor seja notificado se *RabbitMQ* o cancelar por algum motivo.
        Em seguida, o comando RPC *Basic.Consume* é emitido, o qual retorna a etiqueta usada para
        identificar exclusivamente o consumidor junto ao *RabbitMQ*.
        O valor dessa etiqueta é mantido, para que possa ser usado quando do cancelamento do consumidor.
        O método *on_message* é passado como *callback*, a ser invocado na chegada de mensagens.
        """
        self.logger.info("Adicionando callback para cancelamento do consumidor")
        self.channel.add_on_cancel_callback(self.on_consumer_cancelled)

        self.consumer_tag = self.channel.basic_consume(queue=self.queue_name,
                                                       on_message_callback=self.on_message)
        self.started_consumption = True
        self.consuming = True

    def on_consumer_cancelled(self, method_frame: Frame.Method) -> None:
        """
        Invocado por pika quando *RabbitMQ* envia o *Basic.Cancel* para um consumidor recebendo mensagens.

        :param method_frame: The Basic.Cancel frame
        """
        self.logger.info("O consumidor foi cancelado remotamente, encerrando: %r", method_frame)
        if self.channel:
            self.channel.close()

    def on_message(self, _unused_channel: Channel, basic_deliver: Spec.Basic.Deliver,
                   properties: Spec.BasicProperties, msg_body: bytes) -> None:
        """
        Invocado pelo pika quando uma mensagem do *RabbitMQ* é entregue.
        O objeto *basic_deliver* que é passado contem o comutador, a chave de roteamento,
        a etiqueta de entrega e um sinalizador de reenvio da mensagem.
        O parâmetro propriedades contem as propriedades da mensagem.
        O parâmetro body contem o corpo da mensagem enviada.
        O recebimento da mensagem é então declarado ao *RabbitMQ*, enviando-se o comando RPC *Basic.Ack*
        com a etiqueta de entrega.

        :param _unused_channel: o objeto Channel
        :param basic_deliver: o objeto Basic.Deliver
        :param properties: o objeto Spec.BasicProperties
        :param msg_body: o corpo da mensagem
        """
        self.logger.info(f"Msg '{basic_deliver.delivery_tag}' "
                         f"recebida de '{properties.app_id}': {msg_body.decode()}")
        self.channel.basic_ack(basic_deliver.delivery_tag)

        # transmite a mensagem ao destinatário
        self.msg_target(msg_body)

    def stop_consuming(self) -> None:
        """
        Envia o comando RPC *Basic.Cancel* para informar *RabbitMQ* da decisão de parar de consumir mensagens.
        """
        if self.channel:
            self.logger.info("Enviando o comando RPC Basic.Cancel para RabbitMQ")
            self.channel.basic_cancel(consumer_tag=self.consumer_tag,
                                      callback=self.on_cancel_ok)

    def on_cancel_ok(self, _unused_frame: Frame.Method) -> None:
        """
        Invocado por *pika* quando o *RabbitMQ* reconhece o cancelamento de um consumidor.
        Neste ponto fecha-se o canal, o que fará com que on_channel_closed seja invocado,
        o que, por sua vez, fechará a conexão.

        :param _unused_frame: The Basic.CancelOk frame
        """
        self.consuming = False
        self.logger.info(f"RabbitMQ reconheceu o cancelamento do consumidor: '{self.consumer_tag}'")
        self.close_channel()

    def close_channel(self) -> None:
        """
        Fecha o canal com RabbitMQ de forma limpa, emitindo o comando RPC *Channel.Close*.
        """
        self.logger.info("Fechando o canal...")
        self.channel.close()

    def get_state(self) -> int:
        """
        Return the current state of the subscriber.

        The state is one of:
            - MQS_CONNECTION_OPEN
            - MQS_CONNECTION_CLOSED
            - MQS_CONNECTION_ERROR
            - MQS_INITIALIZING

        :return: the current state of the subscriber.
        """
        return self.state

    def get_state_msg(self) -> str:
        """
        Return the message associated with the current state of the subscriber.

        :return: the state message.
        """

    def stop(self) -> None:
        """
        Desliga de forma limpa a conexão com o *RabbitMQ*, parando o consumidor.
        Quando *RabbitMQ* confirmar o cancelamento, *on_cancel_ok* será invocado por *pika*,
        o que fechará o canal e terminará a conexão. O *IOLoop* é iniciado novamente, porque
        precisa estar em execução para que *pika* possa se comunicar com *RabbitMQ*.
        Todos os comandos emitidos antes de iniciar o *IOLoop* são armazenados em *buffer*, mas não processados.
        """
        if not self.closing:
            self.closing = True
            self.logger.info("Parando...")
            if self.consuming:
                self.stop_consuming()
                self.conn.ioloop.start()
            else:
                self.conn.ioloop.stop()
            self.logger.info("Parado")


class _MqSubscriberMaster(threading.Thread):
    """
    Objeto que fará a reconexão do *MqPublisher*, se este indica que a reconexão é necessária.
    """
    # instance attributes
    consumer: _MqSubscriber | None
    mq_url: str
    msg_target: callable
    exchange_name: str
    exchange_type: str
    logger: logging.Logger
    queue_name: str
    reconnect_delay: int
    stopped: bool

    def __init__(self, mq_url: str, exchange_name: str, exchange_type: str,
                 queue_name: str, msg_target: callable, logger: logging.Logger) -> None:

        threading.Thread.__init__(self)

        self.mq_url = mq_url
        self.msg_target = msg_target
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.logger = logger
        self.reconnect_delay = 0
        self.stopped = False

        # instancia o consumidor
        self.consumer = _MqSubscriber(self.mq_url, self.exchange_name, self.exchange_type,
                                      self.queue_name, self.msg_target, self.logger)

    def run(self) -> None:
        """
        Ponto de entrada para a *thread*.
        """
        while True:
            # executa o consumidor, bloqueando até que ele seja interrompido
            self.consumer.run()

            # interrompe o consumidor
            self.consumer.stop()

            if self.stopped or not self.__maybe_reconnect():
                break

    def stop(self) -> None:

        self.stopped = True
        if self.consumer is not None:
            self.consumer.stop()
            self.consumer = None

    def __maybe_reconnect(self) -> bool:
        """
        Decide se o consumidor deve ser recriado, para que a conexão seja restabelecida.

        :return: a decisão de recriação da conexÃo
        """
        result: bool = self.consumer.should_reconnect

        if result:
            reconnect_delay = self.__get_reconnect_delay()
            self.logger.info(f"Reconectando em {reconnect_delay} segundos")
            time.sleep(reconnect_delay)

            # cria uma nova instância do consumidor
            self.consumer = _MqSubscriber(self.mq_url, self.exchange_name, self.exchange_type,
                                          self.queue_name, self.msg_target, self.logger)

        return result

    def __get_reconnect_delay(self) -> int:

        if self.consumer.started_consumption:
            self.reconnect_delay = 0
        else:
            self.reconnect_delay += 1

        if self.reconnect_delay > 30:
            self.reconnect_delay = 30

        return self.reconnect_delay
