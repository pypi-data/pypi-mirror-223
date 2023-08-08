from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class CIDV1Doc:
    @staticmethod
    def modelviewset_list_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.QUERY,
                name="page",
                required=False,
                type=OpenApiTypes.INT,
                examples=[
                    OpenApiExample("Example 1", summary="Pagination", value=1),
                    OpenApiExample("Example 2", summary="Pagination", value=2),
                ],
            )
        ]

    @staticmethod
    def modelviewset_list_examples():
        return [
            OpenApiExample(
                "CID - List All",
                value=[
                    {
                        "identifier": "ORG=Kubefacets Inc,PRJ=Config,COLL=SSO",
                        "slug": "sso",
                        "name": "SSO",
                    }
                ],
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_get_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "CID - Get",
                        summary="CID Identifier",
                        description="CID - Get",
                        value="ORG=Kubefacets Inc,PRJ=Config,COLL=SSO",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "CID - Get",
                value={
                    "identifier": "ORG=Kubefacets Inc,PRJ=Config,COLL=SSO",
                    "slug": "sso",
                    "name": "SSO",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "CID - Create",
                value={
                    "identifier": "ORG=Kubefacets Inc,PRJ=Config,COLL=Cert",
                    "slug": "cert",
                    "name": "Cert",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "CID - Create",
                value={
                    "identifier": "ORG=Kubefacets Inc,PRJ=Config,COLL=Cert",
                    "slug": "cert",
                    "name": "Cert",
                },
                request_only=False,
                response_only=True,
            ),
        ]

    @staticmethod
    def modelviewset_delete_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "CID - Delete",
                        summary="CID Identifier",
                        description="CID - Delete",
                        value="ORG=Kubefacets Inc,PRJ=Config,COLL=Cert",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_path_examples():
        return [
            OpenApiParameter(
                location=OpenApiParameter.PATH,
                name="identifier",
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        "CID - Patch",
                        summary="CID Identifier",
                        description="CID - Patch",
                        value="ORG=Kubefacets Inc,PRJ=Config,COLL=Cert",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "CID - Patch",
                value={
                    "slug": "certs",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "TID - Patch",
                value={
                    "identifier": "ORG=Kubefacets Inc,PRJ=Config,COLL=Cert",
                    "slug": "certs",
                    "name": "Cert",
                },
                request_only=False,
                response_only=True,
            ),
        ]
