from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.docs.v1.pid import PIDV1Doc
from kfsd.apps.endpoints.serializers.common.pid import PIDViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class PIDDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**PIDDoc.modelviewset_list()),
            "retrieve": extend_schema(**PIDDoc.modelviewset_get()),
            "destroy": extend_schema(**PIDDoc.modelviewset_delete()),
            "partial_update": extend_schema(**PIDDoc.modelviewset_patch()),
            "create": extend_schema(**PIDDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "PID - Patch",
            "description": "PID Patch",
            "tags": ["PID"],
            "responses": {
                200: PIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": PIDV1Doc.modelviewset_patch_path_examples(),
            "examples": PIDV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "PID - List",
            "description": "PID - All",
            "tags": ["PID"],
            "responses": {
                200: PIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": PIDV1Doc.modelviewset_list_path_examples(),
            "examples": PIDV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "PID - Get",
            "description": "PID Detail",
            "tags": ["PID"],
            "responses": {
                200: PIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": PIDV1Doc.modelviewset_get_path_examples(),
            "examples": PIDV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "PID - Create",
            "description": "PID - Create",
            "tags": ["PID"],
            "responses": {
                200: PIDViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": PIDV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "PID - Delete",
            "description": "PID Delete",
            "tags": ["PID"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": PIDV1Doc.modelviewset_delete_path_examples(),
        }
