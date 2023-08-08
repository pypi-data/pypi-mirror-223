from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class OIDV1Doc:
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
                "OID - List All",
                value=[
                    {
                        "identifier": "ORG=Kubefacets Inc",
                        "slug": "kubefacets-inc",
                        "name": "Kubefacets Inc",
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
                        "OID - Get",
                        summary="OID Identifier",
                        description="OID - Get",
                        value="ORG=Kubefacets Inc",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "OID - Get",
                value={
                    "identifier": "ORG=Kubefacets Inc",
                    "slug": "kubefacets-inc",
                    "name": "Kubefacets Inc",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "OID - Create",
                value={
                    "identifier": "ORG=Kubefacets Inc",
                    "slug": "kubefacets-inc",
                    "name": "Kubefacets Inc",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "OID - Create",
                value={
                    "identifier": "ORG=Kubefacets Inc",
                    "slug": "kubefacets-inc",
                    "name": "Kubefacets Inc",
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
                        "OID - Delete",
                        summary="OID Identifier",
                        description="OID - Delete",
                        value="ORG=Kubefacets Inc",
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
                        "OID - Patch",
                        summary="OID Identifier",
                        description="OID - Patch",
                        value="ORG=Kubefacets Inc",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "OID - Patch",
                value={
                    "name": "Kubefacets",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "OID - Patch",
                value={
                    "identifier": "ORG=Kubefacets Inc",
                    "name": "Kubefacets",
                    "slug": "kubefacets-inc",
                },
                request_only=False,
                response_only=True,
            ),
        ]
