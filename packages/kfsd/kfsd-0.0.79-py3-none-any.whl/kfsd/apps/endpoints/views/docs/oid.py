from drf_spectacular.utils import extend_schema

from kfsd.apps.endpoints.views.docs.v1.oid import OIDV1Doc
from kfsd.apps.endpoints.serializers.common.oid import OIDViewModelSerializer
from kfsd.apps.endpoints.serializers.base import (
    NotFoundSerializer,
    ErrorSerializer,
)


class OIDDoc:
    @staticmethod
    def modelviewset():
        return {
            "list": extend_schema(**OIDDoc.modelviewset_list()),
            "retrieve": extend_schema(**OIDDoc.modelviewset_get()),
            "destroy": extend_schema(**OIDDoc.modelviewset_delete()),
            "partial_update": extend_schema(**OIDDoc.modelviewset_patch()),
            "create": extend_schema(**OIDDoc.modelviewset_create()),
        }

    @staticmethod
    def modelviewset_patch():
        return {
            "summary": "OID - Patch",
            "description": "OID Patch",
            "tags": ["OID"],
            "responses": {
                200: OIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": OIDV1Doc.modelviewset_patch_path_examples(),
            "examples": OIDV1Doc.modelviewset_patch_examples(),
        }

    @staticmethod
    def modelviewset_list():
        return {
            "summary": "OID - List",
            "description": "OID - All",
            "tags": ["OID"],
            "responses": {
                200: OIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": OIDV1Doc.modelviewset_list_path_examples(),
            "examples": OIDV1Doc.modelviewset_list_examples(),
        }

    @staticmethod
    def modelviewset_get():
        return {
            "summary": "OID - Get",
            "description": "OID Detail",
            "tags": ["OID"],
            "responses": {
                200: OIDViewModelSerializer,
                404: NotFoundSerializer,
                500: ErrorSerializer,
            },
            "parameters": OIDV1Doc.modelviewset_get_path_examples(),
            "examples": OIDV1Doc.modelviewset_get_examples(),
        }

    @staticmethod
    def modelviewset_create():
        return {
            "summary": "OID - Create",
            "description": "OID - Create",
            "tags": ["OID"],
            "responses": {
                200: OIDViewModelSerializer,
                400: ErrorSerializer,
                404: ErrorSerializer,
                500: ErrorSerializer,
            },
            "examples": OIDV1Doc.modelviewset_create_examples(),
        }

    @staticmethod
    def modelviewset_delete():
        return {
            "summary": "OID - Delete",
            "description": "OID Delete",
            "tags": ["OID"],
            "responses": {204: None, 404: NotFoundSerializer, 500: ErrorSerializer},
            "parameters": OIDV1Doc.modelviewset_delete_path_examples(),
        }
