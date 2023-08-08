from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class PIDV1Doc:
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
                "PID - List All",
                value=[
                    {
                        "identifier": "ORG=Kubefacets Inc,PRJ=Config",
                        "slug": "config",
                        "name": "Config",
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
                        "PID - Get",
                        summary="PID Identifier",
                        description="PID - Get",
                        value="ORG=Kubefacets Inc,PRJ=Config",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "PID - Get",
                value={
                    "identifier": "ORG=Kubefacets Inc,PRJ=Config",
                    "slug": "config",
                    "name": "Config",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "PID - Create",
                value={
                    "identifier": "ORG=Kubefacets Inc,PRJ=Config",
                    "slug": "config",
                    "name": "Config",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "PID - Create",
                value={
                    "identifier": "ORG=Kubefacets Inc,PRJ=Config",
                    "slug": "config",
                    "name": "Config",
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
                        "PID - Delete",
                        summary="PID Identifier",
                        description="PID - Delete",
                        value="ORG=Kubefacets Inc,PRJ=Config",
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
                        "PID - Patch",
                        summary="PID Identifier",
                        description="PID - Patch",
                        value="ORG=Kubefacets Inc,PRJ=Config",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "PID - Patch",
                value={
                    "slug": "config1",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "PID - Patch",
                value={
                    "identifier": "ORG=Kubefacets Inc,PRJ=Config",
                    "slug": "config1",
                    "name": "Config",
                },
                request_only=False,
                response_only=True,
            ),
        ]
