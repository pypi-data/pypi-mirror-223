import pika
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
        self.__connection = self.connect()
        self.__channel = self.__connection.channel()
        self.declareExchanges()
        atexit.register(close_rabbitmq_connection)

    @classmethod
    @Singleton
    def getSingleton(cls):
        return cls()

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
        exchanges = self.__config.findConfigs(["services.rabbitmq.exchanges"])[0]
        for exchangeAttrs in exchanges:
            self.__channel.exchange_declare(**exchangeAttrs)

    def declareQueues(self, serviceConfigId):
        declarations = self.__config.findConfigs(
            ["services.rabbitmq.consumers.declarations"]
        )[0]
        for queueAttrs in declarations:
            queueAttrs["queue"] = queueAttrs["queue"].format(service_id=serviceConfigId)
            self.__channel.queue_declare(**queueAttrs)

    def bindQueues(self, serviceConfigId):
        binds = self.__config.findConfigs(["services.rabbitmq.consumers.binds"])[0]
        for bindAttrs in binds:
            if "identifier" in bindAttrs:
                bindAttrs.pop("identifier")

            bindAttrs["queue"] = bindAttrs["queue"].format(service_id=serviceConfigId)
            bindAttrs["routing_key"] = bindAttrs["routing_key"].format(
                service_id=serviceConfigId
            )
            self.__channel.queue_bind(**bindAttrs)

    def consumeQueues(self, serviceConfigId, callback):
        queues = self.__config.findConfigs(["services.rabbitmq.consumers.queues"])[0]
        for queueAttrs in queues:
            queueAttrs["queue"] = queueAttrs["queue"].format(service_id=serviceConfigId)
            self.consume(queueAttrs, callback)

    def publish(self, attrs, msg):
        attrs[self.BODY] = msg
        properties = DictUtils.get(attrs, self.PROPERTIES, None)
        if properties:
            properties = pika.BasicProperties(**properties)
            attrs[self.PROPERTIES] = properties

        self.__channel.basic_publish(**attrs)

    def consume(self, attrs, callback):
        attrs[self.ON_MESSAGE_CALLBACK] = callback
        self.__channel.basic_consume(**attrs)

    def closeConnection(self):
        self.__connection.close()

    def startConsuming(self):
        self.__channel.start_consuming()


def close_rabbitmq_connection():
    logger.info("Closing RabbitMQ Connection!")
    try:
        rabbitMQ = RabbitMQ.getSingleton()
        rabbitMQ.closeConnection()
    except Exception as e:
        logger.error("Could not close RabbitMQ connection!: {}".format(e))
