from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.docs.v1.uid import UIDV1Doc
from kfsd.apps.endpoints.serializers.common.uid import UIDViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class UIDDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**UIDDoc.modelviewset_list()),
            "retrieve": extend_schema(**UIDDoc.modelviewset_get()),
            "destroy": extend_schema(**UIDDoc.modelviewset_delete()),
            "partial_update": extend_schema(**UIDDoc.modelviewset_patch()),
            "create": extend_schema(**UIDDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "UID - Patch",
            "description": "UID Patch",
            "tags": ["UID"],
            "responses": {
                200: UIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": UIDV1Doc.modelviewset_patch_path_examples(),
            "examples": UIDV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "UID - List",
            "description": "UID - All",
            "tags": ["UID"],
            "responses": {
                200: UIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": UIDV1Doc.modelviewset_list_path_examples(),
            "examples": UIDV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "UID - Get",
            "description": "UID Detail",
            "tags": ["UID"],
            "responses": {
                200: UIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": UIDV1Doc.modelviewset_get_path_examples(),
            "examples": UIDV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "UID - Create",
            "description": "UID - Create",
            "tags": ["UID"],
            "responses": {
                200: UIDViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": UIDV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "UID - Delete",
            "description": "UID Delete",
            "tags": ["UID"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": UIDV1Doc.modelviewset_delete_path_examples(),
        }
