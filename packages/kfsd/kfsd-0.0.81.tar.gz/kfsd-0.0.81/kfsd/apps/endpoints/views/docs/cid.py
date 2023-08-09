from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.docs.v1.cid import CIDV1Doc
from kfsd.apps.endpoints.serializers.common.cid import CIDViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class CIDDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**CIDDoc.modelviewset_list()),
            "retrieve": extend_schema(**CIDDoc.modelviewset_get()),
            "destroy": extend_schema(**CIDDoc.modelviewset_delete()),
            "partial_update": extend_schema(**CIDDoc.modelviewset_patch()),
            "create": extend_schema(**CIDDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "CID - Patch",
            "description": "CID Patch",
            "tags": ["CID"],
            "responses": {
                200: CIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": CIDV1Doc.modelviewset_patch_path_examples(),
            "examples": CIDV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "CID - List",
            "description": "CID - All",
            "tags": ["CID"],
            "responses": {
                200: CIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": CIDV1Doc.modelviewset_list_path_examples(),
            "examples": CIDV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "CID - Get",
            "description": "CID Detail",
            "tags": ["CID"],
            "responses": {
                200: CIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": CIDV1Doc.modelviewset_get_path_examples(),
            "examples": CIDV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "CID - Create",
            "description": "CID - Create",
            "tags": ["CID"],
            "responses": {
                200: CIDViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": CIDV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "CID - Delete",
            "description": "CID Delete",
            "tags": ["CID"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": CIDV1Doc.modelviewset_delete_path_examples(),
        }
