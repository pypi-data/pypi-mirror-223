from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.docs.v1.tid import TIDV1Doc
from kfsd.apps.endpoints.serializers.common.tid import TIDViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class TIDDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**TIDDoc.modelviewset_list()),
            "retrieve": extend_schema(**TIDDoc.modelviewset_get()),
            "destroy": extend_schema(**TIDDoc.modelviewset_delete()),
            "partial_update": extend_schema(**TIDDoc.modelviewset_patch()),
            "create": extend_schema(**TIDDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "TID - Patch",
            "description": "TID Patch",
            "tags": ["TID"],
            "responses": {
                200: TIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": TIDV1Doc.modelviewset_patch_path_examples(),
            "examples": TIDV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "TID - List",
            "description": "TID - All",
            "tags": ["TID"],
            "responses": {
                200: TIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": TIDV1Doc.modelviewset_list_path_examples(),
            "examples": TIDV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "TID - Get",
            "description": "TID Detail",
            "tags": ["TID"],
            "responses": {
                200: TIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": TIDV1Doc.modelviewset_get_path_examples(),
            "examples": TIDV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "TID - Create",
            "description": "TID - Create",
            "tags": ["TID"],
            "responses": {
                200: TIDViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": TIDV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "TID - Delete",
            "description": "TID Delete",
            "tags": ["TID"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": TIDV1Doc.modelviewset_delete_path_examples(),
        }
