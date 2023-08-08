from django.core.management.base import BaseCommand
from kfsd.apps.core.msmq.rabbitmq.base import RabbitMQ
from kfsd.apps.core.utils.time import Time
from kfsd.apps.endpoints.serializers.common.outpost import MsgSerializer
from kfsd.apps.endpoints.serializers.common.uid import UIDViewModelSerializer
from kfsd.apps.endpoints.serializers.common.oid import OIDViewModelSerializer
from kfsd.apps.endpoints.serializers.common.pid import PIDViewModelSerializer
from kfsd.apps.endpoints.serializers.common.tid import TIDViewModelSerializer
from kfsd.apps.endpoints.serializers.common.cid import CIDViewModelSerializer


from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.utils.dict import DictUtils
from kfsd.apps.models.tables.outpost import Outpost, send_msg
from kfsd.apps.models.constants import (
    OUTPOST_ACTION_CLEAR,
    UID_ACTION_CREATE,
    OID_ACTION_CREATE,
    PID_ACTION_CREATE,
    TID_ACTION_CREATE,
    CID_ACTION_CREATE,
    UID_ACTION_UPDATE,
    OID_ACTION_UPDATE,
    PID_ACTION_UPDATE,
    TID_ACTION_UPDATE,
    CID_ACTION_UPDATE,
    UID_ACTION_DELETE,
    OID_ACTION_DELETE,
    PID_ACTION_DELETE,
    TID_ACTION_DELETE,
    CID_ACTION_DELETE,
)

from kfsd.apps.models.tables.uid import UID
from kfsd.apps.models.tables.oid import OID
from kfsd.apps.models.tables.tid import TID
from kfsd.apps.models.tables.pid import PID
from kfsd.apps.models.tables.cid import CID


import json

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


def clear_outpost(data):
    outpostQS = Outpost.objects.filter(status="E").order_by("created")
    identifiers = [outpost.identifier for outpost in outpostQS]
    logger.info(
        "Recd CLEAR_OUTPOST command on msmq, identifiers: {} with 'Error' status found.".format(
            identifiers if identifiers else None
        )
    )
    for outpostIns in outpostQS:
        send_msg(outpostIns)


def create_id(serializer, data):
    idSerailizer = serializer(data=data)
    idSerailizer.is_valid(raise_exception=True)
    idSerailizer.save()


def update_id(identifier, model, serializer, data):
    instance = model.objects.get(identifier=identifier)
    serializedData = serializer(instance, data=data, partial=True)
    serializedData.is_valid(raise_exception=True)
    serializedData.save()


def delete_id(identifier, model):
    instance = model.objects.get(identifier=identifier)
    instance.delete()


def get_id_model_serializer(action):
    if action.endswith("_UID"):
        return UID, UIDViewModelSerializer
    elif action.endswith("_OID"):
        return OID, OIDViewModelSerializer
    elif action.endswith("_TID"):
        return TID, TIDViewModelSerializer
    elif action.endswith("_PID"):
        return PID, PIDViewModelSerializer
    elif action.endswith("_CID"):
        return CID, CIDViewModelSerializer


def process_id(requestData):
    action = DictUtils.get_by_path(requestData, "action")
    data = DictUtils.get_by_path(requestData, "data")
    identifier = DictUtils.get_by_path(requestData, "data.identifier")
    logger.info(
        "Recd {} command on msmq, request data: {}".format(
            action, json.dumps(requestData, indent=4)
        )
    )
    model, serializer = get_id_model_serializer(action)
    if action in [
        UID_ACTION_CREATE,
        OID_ACTION_CREATE,
        TID_ACTION_CREATE,
        PID_ACTION_CREATE,
        CID_ACTION_CREATE,
    ]:
        create_id(serializer, data)

    if action in [
        UID_ACTION_UPDATE,
        OID_ACTION_UPDATE,
        TID_ACTION_UPDATE,
        PID_ACTION_UPDATE,
        CID_ACTION_UPDATE,
    ]:
        update_id(identifier, model, serializer, data)

    if action in [
        UID_ACTION_DELETE,
        OID_ACTION_DELETE,
        TID_ACTION_DELETE,
        PID_ACTION_DELETE,
        CID_ACTION_DELETE,
    ]:
        delete_id(identifier, model)


callback_map = {
    OUTPOST_ACTION_CLEAR: clear_outpost,
    UID_ACTION_CREATE: process_id,
    OID_ACTION_CREATE: process_id,
    TID_ACTION_CREATE: process_id,
    PID_ACTION_CREATE: process_id,
    CID_ACTION_CREATE: process_id,
    UID_ACTION_UPDATE: process_id,
    OID_ACTION_UPDATE: process_id,
    TID_ACTION_UPDATE: process_id,
    PID_ACTION_UPDATE: process_id,
    CID_ACTION_UPDATE: process_id,
    UID_ACTION_DELETE: process_id,
    OID_ACTION_DELETE: process_id,
    TID_ACTION_DELETE: process_id,
    PID_ACTION_DELETE: process_id,
    CID_ACTION_DELETE: process_id,
}


def base_callback(ch, method, properties, body):
    bodyStr = body.decode().replace("'", '"')
    jsonStr = json.loads(bodyStr)
    serializedData = MsgSerializer(data=jsonStr)
    serializedData.is_valid(raise_exception=True)

    action = DictUtils.get(serializedData.data, "action")
    if action in callback_map:
        callback_map[action](serializedData.data)
    else:
        logger.error("Action : {} not handled in message consumption".format(action))


class Command(BaseCommand):
    help = "Listens to a RabbitMQ topic"

    def __init__(self, callbackFn=base_callback):
        self.__callbackFn = callbackFn

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--service_config_id",
            type=str,
            help="Service Config Id",
        )

    def connectToMSMQ(self, serviceConfigId):
        try:
            msmqHandler = RabbitMQ.getSingleton(serviceConfigId)
            return msmqHandler
        except Exception as e:
            print(e)
            logger.error(
                "Error connecting to RabbitMQ, check if RabbitMQ instance is up!"
            )
            Time.sleep(30)
            self.connectToMSMQ()

    def handle(self, *args, **options):
        logger.info("Listening to MSMQ messages...")
        serviceConfigId = DictUtils.get(options, "service_config_id")
        msmqHandler = self.connectToMSMQ(serviceConfigId)
        msmqHandler.consumeQueues(self.__callbackFn)
        msmqHandler.startConsuming()
