from typing import Any, Final
from pika.channel import Channel
from pika.connection import Connection
from pika.exchange_type import ExchangeType
from pika.spec import BasicProperties
from pypomes_core import APP_PREFIX, env_get_str
import logging
import pika
import time
import pika.frame as Frame
import threading

MQ_EXCHANGE_NAME: Final[str] = env_get_str(f"{APP_PREFIX}_MQ_EXCHANGE_NAME")
MQ_EXCHANGE_TYPE: Final[str] = env_get_str(f"{APP_PREFIX}_MQ_EXCHANGE_TYPE")
MQ_ROUTING_BASE: Final[str] = env_get_str(f"{APP_PREFIX}_MQ_ROUTING_BASE")
MQ_URL: Final[str] = env_get_str(f"{APP_PREFIX}_MQ_URL")

MQP_CONNECTION_OPEN: Final[int] = 1
MQP_CONNECTION_CLOSED: Final[int] = 2
MQP_CONNECTION_ERROR: Final[int] = -1
MQP_INITIALIZING: Final[int] = 0


class MqPublisher(threading.Thread):
    """
    Este é um exemplo de publicador que pode lidar com interações inesperadas
    com *RabbitMQ*, tais como fechamento de canal e interrupções na conexão.

    Se o *RabbitMQ* fechar a conexão, ela será reaberta. Nesses casos, deve-se sempre
    observe a saída, pois são poucas as razões pelas quais a conexão pode ser fechado,
    e elas geralmente estão relacionadas a permissões ou tempos limite de uso de *sockets*.

    Eessa classe usa confirmações de entrega, e demonstra uma maneira de acompanhar
    mensagens que foram enviadas, e verificar se foram confirmadas pelo *RabbitMQ*.
    """
    # atributos públicos
    started_publishing: bool
    # structure ('n' is the sequential message number, int > 0):
    # <{ n: { "header": <str>,
    #        "body":  <bytes>,
    #        "mimetype": <str>,
    #        "routing_key": <str>
    #      },...
    # }>
    messages: dict | None

    # protected attributes
    _mq_url: str
    _exchange_name: str
    _exchange_type: ExchangeType | str
    _stopped: bool
    _acked: int
    _nacked: int
    _msg_last_filed: int
    _msg_last_sent: int
    _logger: logging.Logger
    _publish_interval: int
    _reconnect_delay: int
    _channel: Channel | None
    _state: int
    _state_msg: str

    # 'Any',instead of 'None', prevents the alert "Cannot find reference 'ioloop' in 'Connection'"
    _connection: Connection | Any

    # mutex for controlling concurrent access to the messages
    _msg_lock: threading.Lock

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

        self._state = MQP_INITIALIZING
        self._state_msg = "Attenpting to initialize the publisher"
        self._mq_url = mq_url
        self._logger = logger
        self._exchange_name = exchange_name

        match exchange_type:
            case "direct":
                self._exchange_type = ExchangeType.direct
            case "fanout":
                self._exchange_type = ExchangeType.fanout
            case "headers":
                self._exchange_type = ExchangeType.headers
            case _:  # 'topic'
                self._exchange_type = ExchangeType.topic

        self.started_publishing = False
        self._connection = None
        self._channel = None
        self._stopped = False

        self._acked = 0
        self._nacked = 0
        self._msg_last_filed = 0
        self._msg_last_sent = 0
        self._publish_interval = 1
        self._reconnect_delay = 5

        self.messages = None
        # inicializa mutex
        self._msg_lock = threading.Lock()

        if self._logger is not None:
            self._logger.info("Publisher instantiated, with exchange "
                              f"'{exchange_name}' of type '{exchange_type}'")

    # ponto de entrada para a thread
    def run(self) -> None:
        """
        Initialize the publisher, by connecting with *RabbitMQ* e initiating the o *IOLoop*.
        """
        # stay in the loop, until 'stop()' is invoked
        while not self._stopped:
            self._logger.info("Iniciado")
            self.messages = {}
            self._acked = 0
            self._nacked = 0
            self._msg_last_sent = 0

            # conect with RabbitMQ
            self._connection = self.connect()

            # initiate the IOLoop, blocking until it is interrupted
            self._connection.ioloop.start()

        self._logger.info("Finished")

    def connect(self) -> Connection:
        """
        Connect with *RabbitMQ*, and return the connection identifier.
        When the connection is established, *on_connection_open* will be invooked by *pika*.

        :return: the connection obtained
        """
        if self._logger is not None:
            # do not write user and password from URL in the log
            #   url: <protocol>//<user>:<password>@<ip-address>
            first: int = self._mq_url.find("//")
            last = self._mq_url.find("@")
            self._logger.info(f"Connecting with '{self._mq_url[0:first]}{self._mq_url[last:]}'")

        # obtain anf return the connection
        return pika.SelectConnection(
            pika.URLParameters(self._mq_url),
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
        self._state = MQP_CONNECTION_OPEN
        self._state_msg = "Connection was open"
        self._logger.info(self._state_msg)
        self.open_channel()

    def on_connection_open_error(self, _connection: Connection, error: Exception) -> None:
        """
        Invocado por *pika* se a conexão com o *RabbitMQ* não puder ser estabelecida.

        :param _connection: a conexão tentada com o RabbitMQ
        :param error: a mensagem de erro
        """
        self._state = MQP_CONNECTION_ERROR
        self._state_msg = f"Error establishing connection: {error}"
        self._logger.error(self._state_msg)
        self._logger.info(f"Reconnecting in {self._reconnect_delay} segundos")
        self._connection.ioloop.call_later(self._reconnect_delay, self._connection.ioloop.stop)

    def on_connection_closed(self, _connection: Connection, reason: Exception) -> None:
        """
        Invocado por *pika* quando a conexão com o *RabbitMQ* é inesperadamente fechada.
        Nesse caso, a reconexão com *RabbitMQ* é tentada.

        :param _connection: a conexão fechada inesperadamente
        :param reason: exceção representando o motivo para a perda da conexão
        """
        self._state = MQP_CONNECTION_CLOSED
        self._state_msg = f"Connection was closed: {reason}"
        self._channel = None
        if self._stopped:
            self._connection.ioloop.stop()
        else:
            self._logger.warning(self._state_msg)
            self._logger.info(f"Reconnecting in {self._reconnect_delay} seconds")
            self._connection.ioloop.call_later(self._reconnect_delay, self._connection.ioloop.stop)

    def open_channel(self) -> None:
        """
        Abre um novo canal com *RabbitMQ*, emitindo o comando RPC *Channel.Open*.
        Quando o *RabbitMQ* responde que o canal está aberto, o
        método indicado em *on_channel_open_callback* será invocado por *pika*.
        """
        self._logger.info("Criando um novo canal")
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel) -> None:
        """
        Invocado por *pika* quando o canal for aberto.
        O objeto do canal é passado, para que possa ser usado, se necessário.
        Com o canal agora aberto, o comutador a ser usado é declarada.

        :param channel: O canal que foi aberto
        """
        self._logger.info("O canal foi aberto. Estabelecendo o callback no fechamento do canal")
        self._channel = channel
        self._channel.add_on_close_callback(self.on_channel_closed)
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
        self._logger.warning(f"O canal '{channel}' foi fechado: {reason}")
        self._channel = None
        if not self._stopped and not self._connection.is_closed and not self._connection.is_closing:
            self._connection.close()

    def setup_exchange(self) -> None:
        """
        Verifica se o comutador está configurado no *RabbitMQ*, invocando o comando RPC *Exchange.Declare*
        com o parâmetro *passive=True*. Se essa configuração for confirmada, *on_exchange_declare_ok*
        será invocado por *pika*.
        """
        self._logger.info(f"Declarando o comutador: '{self._exchange_name}'")
        self._channel.exchange_declare(exchange=self._exchange_name,
                                       exchange_type=self._exchange_type,
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
        self._logger.info(f"Comutador declarado: '{self._exchange_name}', pronto para publicação.")
        self._channel.confirm_delivery(ack_nack_callback=self.on_delivery_confirmation)
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

        self._logger.info(f"Recebida confirmação de entrega: etiqueta '{delivery_tag}', "
                          f"tipo '{confirmation_type}', múltiplo: {ack_multiple}")

        if confirmation_type == "ack":
            self._acked += 1
        else:  # elif confirmation_type == "nack":
            self._nacked += 1

        with self._msg_lock:
            self.messages.pop(delivery_tag)

            if ack_multiple:
                msg_tags: list[int] = []
                for msg_tag in self.messages:
                    if msg_tag <= delivery_tag:
                        msg_tags.append(msg_tag)
                        if confirmation_type == "ack":
                            self._acked += 1
                        else:  # confirmation_type == "nack":
                            self._nacked += 1

                for msg_tag in msg_tags:
                    self.messages.pop(msg_tag)

            self._logger.info(f"Mensagens: publicadas {self._msg_last_sent}, "
                              f"a serem confirmadas {len(self.messages)}, "
                              f"bem sucedidas {self._acked}, mal sucedidas {self._nacked}")

    def send_message(self) -> None:
        """
        Se o publicador não estiver parando, publica uma mensagem no *RabbitMQ*, anexando ao objeto *messages*
        os dados da mensagem enviada. Esse objeto é usado para verificar a confirmação das entregas em
        *on_delivery_confirmation*.
        """
        # o canal existe e está aberto ?
        if self._channel is not None and self._channel.is_open:
            # sim, prossiga
            self._msg_last_sent += 1

            with self._msg_lock:
                message: dict = self.messages[self._msg_last_sent]

            properties: BasicProperties = pika.BasicProperties(app_id="mq-publisher",
                                                               content_type=message["mimetype"],
                                                               headers=message["headers"])
            routing_key: str = message.get("routing_key")

            msg_body: bytes = message["body"]
            self._channel.basic_publish(exchange=self._exchange_name,
                                        routing_key=routing_key,
                                        body=msg_body,
                                        properties=properties)
            self._logger.info(f"Msg '{self._msg_last_sent}' publicada, chave '{routing_key}'")
        else:
            # não, reporte o erro
            self._logger.error("Não é possível publicar: "
                               "não há canal aberto com o servidor de mensagens")

    def publish_message(self, msg_body: str | bytes, routing_key: str,
                        msg_mimetype: str = "application/text", msg_headers: str = None) -> None:
        """
        Publica uma mensagem no *RabbitMQ*, se a classe não estiver parando,
        anexando ao objeto messages os dados da mensagem a ser entregue.

        Esse objeto será usada para verificar as confirmações de entrega no *callback* *on_delivery_confirmation*.

        O *RabbitMQ* é avisado para invocar *send_message* em *self._publish_interval* segundos.
        Os intervalos de entrega podem ser acelerados ou desacelerados, alterando-se essa variável.
        """
        # o canal existe e está aberto ?
        if self._channel is not None and self._channel.is_open:
            # sim, prossiga
            msg_bytes: bytes = msg_body if isinstance(msg_body, bytes) else msg_body.encode()
            self._msg_last_filed += 1

            with self._msg_lock:
                self.messages[self._msg_last_filed] = {"headers": msg_headers,
                                                       "body": msg_bytes,
                                                       "mimetype": msg_mimetype,
                                                       "routing_key": routing_key}

            # agenda entrega de mensagem para acontecer em 'self._publish_interval' segundos
            self._connection.ioloop.call_later(self._publish_interval, self.send_message)
            self._logger.info(f"Msg '{self._msg_last_filed}' agendada para publicação em "
                              f"{self._publish_interval}s, chave '{routing_key}': {msg_bytes.decode()}")
        else:
            # não, reporte o erro
            self._logger.error("Mensagem recusada: não há canal aberto com o servidor de mensagens")

    def get_state(self) -> int:
        """
        Retorna o estado do publicador, que pode ser:

        - MQP_CONNECTION_OPEN
        - MQP_CONNECTION_CLOSED
        - MQP_CONNECTION_ERROR
        - MQP_INITIALIZING

        :return: o estado do publicador
        """
        return self._state

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
        self._logger.info("Finalizando...")
        self._stopped = True
        self.close_channel()
        self.close_connection()

    def close_channel(self):
        """
        Fecha o canal com *RabbitMQ*, enviando o comando RPC *Channel.Close*.
        """
        if self._channel is not None:
            self._logger.info("Fechando o canal...")
            self._channel.close()

    def close_connection(self):
        """
        Fecha a cconexão com o RabbitMQ.
        """
        if self._connection is not None:
            self._logger.info("Fechando a conexão...")
            self._connection.close()


def create_publisher(errors: list[str], logger: logging.Logger = None) -> MqPublisher:

    # instantiate the events publisher
    result: MqPublisher | None = MqPublisher(MQ_URL, MQ_EXCHANGE_NAME, MQ_EXCHANGE_TYPE, logger)
    result.daemon = True
    result.start()

    # wait for the conclusion
    while result.get_state() == MQP_INITIALIZING:
        time.sleep(0.001)

    # did connecting with the publisher fail ?
    if result.get_state() == MQP_CONNECTION_ERROR:
        # yes, report the error
        errors.append(result.get_state_msg())
        result = None
    elif logger is not None:
        # no, register the instantiation of the publisher
        logger.info("Events publisher instantiated: exchange "
                    f"'{MQ_EXCHANGE_NAME}' of type {MQ_EXCHANGE_TYPE}")

    return result
