import pika
import pika.exceptions
import atexit
from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.common.kubefacets_config import KubefacetsConfig
from kfsd.apps.core.utils.http.django.config import DjangoConfig
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.core.common.singleton import Singleton

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class RabbitMQ:
    PROPERTIES = "properties"
    BODY = "body"
    ON_MESSAGE_CALLBACK = "on_message_callback"

    def __init__(self):
        self.__config = DjangoConfig(KubefacetsConfig().getConfig())
        self.establish_connection()
        self.declareExchanges()
        atexit.register(lambda: close_rabbitmq_connection(self))

    @classmethod
    @Singleton
    def getSingleton(cls):
        return cls()

    def isConnectionOpen(self):
        return self.__connection.is_open

    def establish_connection(self):
        self.__connection = self.connect()

    def createChannel(self):
        self.__channel = self.__connection.channel()

    def closeChannel(self):
        self.__channel.close()

    def getConfig(self):
        return self.__config

    def connect(self):
        connectionConfig = self.__config.findConfigs(["services.rabbitmq.connect"])[
            0
        ].copy()
        logger.info("Connecting to RabbitMQ: {}".format(connectionConfig))
        authCredentials = connectionConfig.pop("credentials")
        connectionConfig["credentials"] = self.constructCredentials(
            DictUtils.get(authCredentials, "username"),
            DictUtils.get(authCredentials, "pwd"),
        )
        connection_params = pika.ConnectionParameters(**connectionConfig)
        return pika.BlockingConnection(connection_params)

    def constructCredentials(self, username, pwd):
        return pika.PlainCredentials(username, pwd)

    def declareExchanges(self):
        self.createChannel()
        exchanges = self.__config.findConfigs(["services.rabbitmq.exchanges"])[0]
        for exchangeAttrs in exchanges:
            self.__channel.exchange_declare(**exchangeAttrs)

        self.closeChannel()

    def declareQueues(self, serviceConfigId):
        self.createChannel()
        declarations = self.__config.findConfigs(
            ["services.rabbitmq.consumers.declarations"]
        )[0]
        for queueAttrs in declarations:
            queueAttrs["queue"] = queueAttrs["queue"].format(service_id=serviceConfigId)
            self.__channel.queue_declare(**queueAttrs)
        self.closeChannel()

    def bindQueues(self, serviceConfigId):
        self.createChannel()
        binds = self.__config.findConfigs(["services.rabbitmq.consumers.binds"])[0]
        for bindAttrs in binds:
            if "identifier" in bindAttrs:
                bindAttrs.pop("identifier")

            bindAttrs["queue"] = bindAttrs["queue"].format(service_id=serviceConfigId)
            bindAttrs["routing_key"] = bindAttrs["routing_key"].format(
                service_id=serviceConfigId
            )
            self.__channel.queue_bind(**bindAttrs)
        self.closeChannel()

    def consumeQueues(self, serviceConfigId, callback):
        queues = self.__config.findConfigs(["services.rabbitmq.consumers.queues"])[0]
        for queueAttrs in queues:
            queueAttrs["queue"] = queueAttrs["queue"].format(service_id=serviceConfigId)
            self.consume(queueAttrs, callback)

    def publish(self, attrs, msg):
        try:
            attrs[self.BODY] = msg
            properties = DictUtils.get(attrs, self.PROPERTIES, None)
            if properties:
                properties = pika.BasicProperties(**properties)
                attrs[self.PROPERTIES] = properties

            self.createChannel()
            self.__channel.basic_publish(**attrs)
            self.closeChannel()
        except pika.exceptions.StreamLostError:
            logger.error("Recd StreamLostError exception, attempting to reconnect..")
            self.closeConnection()
            self.establish_connection()
            self.publish(attrs, msg)

    def consume(self, attrs, callback):
        attrs[self.ON_MESSAGE_CALLBACK] = callback
        self.createChannel()
        self.__channel.basic_consume(**attrs)

    def closeConnection(self):
        self.__connection.close()

    def startConsuming(self):
        self.__channel.start_consuming()


def close_rabbitmq_connection(self):
    logger.info("Closing RabbitMQ Connection!")
    try:
        self.closeConnection()
    except Exception as e:
        logger.error("Could not close RabbitMQ connection!: {}".format(e))
