from typing import Any, Final
from pika.channel import Channel
from pika.connection import Connection
from pika.exchange_type import ExchangeType
from pika.spec import BasicProperties
import logging
import pika
import pika.frame as Frame
import threading

MQP_CONNECTION_OPEN: Final[int] = 1
MQP_CONNECTION_CLOSED: Final[int] = 2
MQP_CONNECTION_ERROR: Final[int] = -1
MQP_INITIALIZING: Final[int] = 0


class _MqPublisher(threading.Thread):
    """
    Este é um exemplo de publicador que pode lidar com interações inesperadas
    com *RabbitMQ*, tais como fechamento de canal e interrupções na conexão.

    Se o *RabbitMQ* fechar a conexão, ela será reaberta. Nesses casos, deve-se sempre
    observe a saída, pois são poucas as razões pelas quais a conexão pode ser fechado,
    e elas geralmente estão relacionadas a permissões ou tempos limite de uso de *sockets*.

    Eessa classe usa confirmações de entrega, e demonstra uma maneira de acompanhar
    mensagens que foram enviadas, e verificar se foram confirmadas pelo *RabbitMQ*.
    """
    # instance attributes
    started_publishing: bool
    mq_url: str
    exchange_name: str
    exchange_type: ExchangeType | str
    stopped: bool
    acked: int
    nacked: int
    msg_last_filed: int
    msg_last_sent: int
    logger: logging.Logger
    publish_interval: int
    reconnect_delay: int
    channel: Channel | None
    state: int
    state_msg: str

    # structure ('n' is the sequential message number, int > 0):
    # <{ n: { "header": <str>,
    #        "body":  <bytes>,
    #        "mimetype": <str>,
    #        "routing_key": <str>
    #      },...
    # }>
    messages: dict | None

    # 'Any',instead of 'None', prevents the alert "Cannot find reference 'ioloop' in 'Connection'"
    conn: Connection | Any

    # mutex for controlling concurrent access to the messages
    msg_lock: threading.Lock

    def __init__(self, mq_url: str, exchange_name: str, exchange_type: str, logger: logging.Logger) -> None:
        """
        Cria uma nova instância do publicador,
        com os parâmetros necessários para a interação com o *RabbitMQ*.

        :param mq_url: A URL usada para a conexão
        :param exchange_name: o nome do comutador
        :param exchange_type: o tipo do comutador
        :param logger: o logger para registro das operações
        """
        threading.Thread.__init__(self)

        self.state = MQP_INITIALIZING
        self.state_msg = "Attenpting to initialize the publisher"
        self.mq_url = mq_url
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

        self.started_publishing = False
        self.conn = None
        self.channel = None
        self.stopped = False

        self.acked = 0
        self.nacked = 0
        self.msg_last_filed = 0
        self.msg_last_sent = 0
        self.publish_interval = 1
        self.reconnect_delay = 5

        self.messages = None
        # inicializa mutex
        self.msg_lock = threading.Lock()

        if self.logger is not None:
            self.logger.info("Publisher instantiated, with exchange "
                             f"'{exchange_name}' of type '{exchange_type}'")

    # ponto de entrada para a thread
    def run(self) -> None:
        """
        Initialize the publisher, by connecting with *RabbitMQ* e initiating the o *IOLoop*.
        """
        # stay in the loop, until 'stop()' is invoked
        while not self.stopped:
            if self.logger is not None:
                self.logger.info("Iniciado")
            self.messages = {}
            self.acked = 0
            self.nacked = 0
            self.msg_last_sent = 0

            # conect with RabbitMQ
            self.conn = self.connect()

            # initiate the IOLoop, blocking until it is interrupted
            self.conn.ioloop.start()

        if self.logger is not None:
            self.logger.info("Finished")

    def connect(self) -> Connection:
        """
        Connect with *RabbitMQ*, and return the connection identifier.
        When the connection is established, *on_connection_open* will be invooked by *pika*.

        :return: the connection obtained
        """
        if self.logger is not None:
            # do not write user and password from URL in the log
            #   url: <protocol>//<user>:<password>@<ip-address>
            first: int = self.mq_url.find("//")
            last = self.mq_url.find("@")
            if self.logger is not None:
                self.logger.info(f"Connecting with '{self.mq_url[0:first]}{self.mq_url[last:]}'")

        # obtain anf return the connection
        return pika.SelectConnection(
            pika.URLParameters(self.mq_url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed)

    def on_connection_open(self, _connection: Connection) -> None:
        """
        *Callback* chamado quando a conexão com *RabbitMQ* é estabelecida.
        O identificador para o objeto de conexão é passado, para o caso em que faça necessário.
        No momento, ele é apenas marcado como não utilizado.

        :param _connection: a conexão com o RabbitMQ
        """
        self.state = MQP_CONNECTION_OPEN
        self.state_msg = "Connection was open"
        if self.logger is not None:
            self.logger.info(self.state_msg)
        self.open_channel()

    def on_connection_open_error(self, _connection: Connection, error: Exception) -> None:
        """
        Invocado por *pika* se a conexão com o *RabbitMQ* não puder ser estabelecida.

        :param _connection: a conexão tentada com o RabbitMQ
        :param error: a mensagem de erro
        """
        self.state = MQP_CONNECTION_ERROR
        self.state_msg = f"Error establishing connection: {error}"
        if self.logger is not None:
            self.logger.error(self.state_msg)
            self.logger.info(f"Reconnecting in {self.reconnect_delay} segundos")
        self.conn.ioloop.call_later(self.reconnect_delay, self.conn.ioloop.stop)

    def on_connection_closed(self, _connection: Connection, reason: Exception) -> None:
        """
        Invocado por *pika* quando a conexão com o *RabbitMQ* é inesperadamente fechada.
        Nesse caso, a reconexão com *RabbitMQ* é tentada.

        :param _connection: a conexão fechada inesperadamente
        :param reason: exceção representando o motivo para a perda da conexão
        """
        self.state = MQP_CONNECTION_CLOSED
        self.state_msg = f"Connection was closed: {reason}"
        self.channel = None
        if self.stopped:
            self.conn.ioloop.stop()
        else:
            if self.logger is not None:
                self.logger.warning(self.state_msg)
                self.logger.info(f"Reconnecting in {self.reconnect_delay} seconds")
            self.conn.ioloop.call_later(self.reconnect_delay, self.conn.ioloop.stop)

    def open_channel(self) -> None:
        """
        Abre um novo canal com *RabbitMQ*, emitindo o comando RPC *Channel.Open*.
        Quando o *RabbitMQ* responde que o canal está aberto, o
        método indicado em *on_channel_open_callback* será invocado por *pika*.
        """
        if self.logger is not None:
            self.logger.info("Criando um novo canal")
        self.conn.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel) -> None:
        """
        Invocado por *pika* quando o canal for aberto.
        O objeto do canal é passado, para que possa ser usado, se necessário.
        Com o canal agora aberto, o comutador a ser usado é declarada.

        :param channel: O canal que foi aberto
        """
        if self.logger is not None:
            self.logger.info("O canal foi aberto. Estabelecendo o callback no fechamento do canal")
        self.channel = channel
        self.channel.add_on_close_callback(self.on_channel_closed)
        self.setup_exchange()

    def on_channel_closed(self, channel: Channel, reason: Exception) -> None:
        """
        Invocado por *pika* quando *RabbitMQ* fechar inesperadamente o canal.
        Os canais geralmente são fechados quando se tenta fazer algo que
        viola o protocolo, como declarar novamente um comutador ou fila com
        parâmetros diferentes. Neste caso, a conexão é fechada para *shutdown* do objeto.

        :param channel: o canal que foi fechado
        :param reason: a razão para o fechamento do canal
        """
        if self.logger is not None:
            self.logger.warning(f"O canal '{channel}' foi fechado: {reason}")
        self.channel = None
        if not self.stopped and not self.conn.is_closed and not self.conn.is_closing:
            self.conn.close()

    def setup_exchange(self) -> None:
        """
        Verifica se o comutador está configurado no *RabbitMQ*, invocando o comando RPC *Exchange.Declare*
        com o parâmetro *passive=True*. Se essa configuração for confirmada, *on_exchange_declare_ok*
        será invocado por *pika*.
        """
        if self.logger is not None:
            self.logger.info(f"Declarando o comutador: '{self.exchange_name}'")
        self.channel.exchange_declare(exchange=self.exchange_name,
                                      exchange_type=self.exchange_type,
                                      passive=True,
                                      durable=True,
                                      callback=self.on_exchange_declare_ok)

    def on_exchange_declare_ok(self, _unused_frame: Frame.Method) -> None:
        """
        Invocado por *pika* quando o *RabbitMQ* conclui o comando RPC *Exchange.Declare*.
        Possibilita as confirmações de entrega e agenda a primeira mensagem a ser enviada para *RabbitMQ*.
        Envia o comando RPC *confirm_delivery* para *RabbitMQ*, para habilitar a entrega de confirmações no canal.

        A única maneira de desativar isso é fechar o canal e criar um novo. Quando a mensagem do *RabitMQ*
        é confirmada, o método *on_delivery_confirmation* será invocado, passando um *Basic.Ack* ou *Basic.Nack*
        do *RabbitMQ*, que indicará quais mensagens estão sendo confirmadas ou rejeitadas.

        :param _unused_frame: Exchange.DeclareOk response frame
        """
        if self.logger is not None:
            self.logger.info(f"Comutador declarado: '{self.exchange_name}', pronto para publicação.")
        self.channel.confirm_delivery(ack_nack_callback=self.on_delivery_confirmation)
        self.started_publishing = True

    def on_delivery_confirmation(self, method_frame: Frame.Method) -> None:
        """
        Invocado por *pika* quando *RabbitMQ* responde a um comando RPC *Basic.Publish*,
        passando um *frame* *Basic.Ack* ou *Basic.Nack*, com a etiqueta de entrega da mensagem que foi publicada.

        A etiqueta de entrega é um contador inteiro que indica o número da mensagem que foi enviada
        no canal, via *Basic.Publish*. A manutenção da estrutura messages usada para gerenciar as mensagens a
        serem enviadas, ou que estão pendentes de confirmação, é efetuada, e a estatística é gravada no *log*.

        :param method_frame: frame Basic.Ack ou Basic.Nack
        """
        confirmation_type: str = method_frame.method.NAME.split(".")[1].lower()
        ack_multiple: bool = method_frame.method.multiple
        delivery_tag: int = method_frame.method.delivery_tag

        if self.logger is not None:
            self.logger.info(f"Recebida confirmação de entrega: etiqueta '{delivery_tag}', "
                             f"tipo '{confirmation_type}', múltiplo: {ack_multiple}")

        if confirmation_type == "ack":
            self.acked += 1
        else:  # elif confirmation_type == "nack":
            self.nacked += 1

        with self.msg_lock:
            self.messages.pop(delivery_tag)

            if ack_multiple:
                msg_tags: list[int] = []
                for msg_tag in self.messages:
                    if msg_tag <= delivery_tag:
                        msg_tags.append(msg_tag)
                        if confirmation_type == "ack":
                            self.acked += 1
                        else:  # confirmation_type == "nack":
                            self.nacked += 1

                for msg_tag in msg_tags:
                    self.messages.pop(msg_tag)

            if self.logger is not None:
                self.logger.info(f"Mensagens: publicadas {self.msg_last_sent}, "
                                 f"a serem confirmadas {len(self.messages)}, "
                                 f"bem sucedidas {self.acked}, mal sucedidas {self.nacked}")

    def send_message(self) -> None:
        """
        Se o publicador não estiver parando, publica uma mensagem no *RabbitMQ*, anexando ao objeto *messages*
        os dados da mensagem enviada. Esse objeto é usado para verificar a confirmação das entregas em
        *on_delivery_confirmation*.
        """
        # o canal existe e está aberto ?
        if self.channel is not None and self.channel.is_open:
            # sim, prossiga
            self.msg_last_sent += 1

            with self.msg_lock:
                message: dict = self.messages[self.msg_last_sent]

            properties: BasicProperties = pika.BasicProperties(app_id="mq-publisher",
                                                               content_type=message["mimetype"],
                                                               headers=message["headers"])
            routing_key: str = message.get("routing_key")

            msg_body: bytes = message["body"]
            self.channel.basic_publish(exchange=self.exchange_name,
                                       routing_key=routing_key,
                                       body=msg_body,
                                       properties=properties)
            if self.logger is not None:
                self.logger.info(f"Msg '{self.msg_last_sent}' publicada, chave '{routing_key}'")
        elif self.logger is not None:
            # não, reporte o erro
            self.logger.error("Não é possível publicar: "
                              "não há canal aberto com o servidor de mensagens")

    def publish_message(self, errors: list[str], msg_body: str | bytes, routing_key: str,
                        msg_mimetype: str = "application/text", msg_headers: str = None) -> None:
        """
        Publish a message at *RabbitMQ*, if it is not stopping,
        adding to the messages object the message data to be delivered.
        This object will be used for message delivery confirmation on the *callback* *on_delivery_confirmation*.

        *RabbitMQ* is told to invoke *send_message* in *publish_interval* seconds.
        The delivery intervals may be accelerated or decelerated, by changing this variable.
        """
        # does the channel exist and is open ?
        if self.channel is not None and self.channel.is_open:
            # yes, proceed
            msg_bytes: bytes = msg_body if isinstance(msg_body, bytes) else msg_body.encode()
            self.msg_last_filed += 1

            with self.msg_lock:
                self.messages[self.msg_last_filed] = {"headers": msg_headers,
                                                      "body": msg_bytes,
                                                      "mimetype": msg_mimetype,
                                                      "routing_key": routing_key}

            # schedule message delivery to happen in 'publish_interval' seconds
            self.conn.ioloop.call_later(self.publish_interval, self.send_message)
            if self.logger is not None:
                self.logger.info(f"Msg '{self.msg_last_filed}' agendada para publicação em "
                                 f"{self.publish_interval}s, chave '{routing_key}': {msg_bytes.decode()}")
        else:
            # no, report the error
            errmsg: str = "Messagen refused: no open channel to the message server exists"
            errors.append(errmsg)
            if self.logger is not None:
                self.logger.error(errmsg)

    def get_state(self) -> int:
        """
        Return the state of the events publisher. One of:
            - MQP_CONNECTION_OPEN
            - MQP_CONNECTION_CLOSED
            - MQP_CONNECTION_ERROR
            - MQP_INITIALIZING

        :return: the state of the publisher
        """
        return self.state

    def get_state_msg(self) -> str:
        """
        Return the message associated with the current state of the publisher.

        :return: the state message.
        """

    def stop(self):
        """
        Para o publicador, fechando o canal e a conexão. Um sinalizador é definido,
        para que o processo de agendamento do envio de novas mensagens se interrompa.
        """
        if self.logger is not None:
            self.logger.info("Finalizando...")
        self.stopped = True
        self.close_channel()
        self.close_connection()

    def close_channel(self):
        """
        Fecha o canal com *RabbitMQ*, enviando o comando RPC *Channel.Close*.
        """
        if self.channel is not None:
            if self.logger is not None:
                self.logger.info("Fechando o canal...")
            self.channel.close()

    def close_connection(self):
        """
        Fecha a cconexão com o RabbitMQ.
        """
        if self.conn is not None:
            if self.logger is not None:
                self.logger.info("Fechando a conexão...")
            self.conn.close()
