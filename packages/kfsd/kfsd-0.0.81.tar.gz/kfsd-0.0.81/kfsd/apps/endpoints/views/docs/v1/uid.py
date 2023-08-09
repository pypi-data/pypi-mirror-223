from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class UIDV1Doc:
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
                "UID - List All",
                value=[
                    {
                        "identifier": "USER=admin@kubefacets.com",
                        "slug": "admin",
                        "name": "admin@kubefacets.com",
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
                        "UID - Get",
                        summary="UID Identifier",
                        description="UID - Get",
                        value="USER=admin@kubefacets.com",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "UID - Get",
                value={
                    "identifier": "USER=admin@kubefacets.com",
                    "slug": "admin",
                    "name": "admin@kubefacets.com",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "UID - Create",
                value={
                    "identifier": "USER=admin@kubefacets.com",
                    "slug": "admin",
                    "name": "admin@kubefacets.com",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "UID - Create",
                value={
                    "identifier": "USER=admin@kubefacets.com",
                    "slug": "admin",
                    "name": "admin@kubefacets.com",
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
                        "UID - Delete",
                        summary="UID Identifier",
                        description="UID - Delete",
                        value="USER=admin@kubefacets.com",
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
                        "UID - Delete",
                        summary="UID Identifier",
                        description="UID - Delete",
                        value="USER=admin@kubefacets.com",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "UID - Patch",
                value={
                    "name": "admin1",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "UID - Patch",
                value={
                    "identifier": "USER=admin@kubefacets.com",
                    "name": "admin@kubefacets.com",
                    "slug": "admin",
                },
                request_only=False,
                response_only=True,
            ),
        ]
