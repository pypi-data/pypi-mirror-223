from drf_spectacular.utils import OpenApiExample, OpenApiTypes, OpenApiParameter


class TIDV1Doc:
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
                "TID - List All",
                value=[
                    {
                        "identifier": "ORG=Kubefacets Inc,TEAM=Sales",
                        "slug": "sales",
                        "name": "Sales",
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
                        "TID - Get",
                        summary="TID Identifier",
                        description="TID - Get",
                        value="ORG=Kubefacets Inc,TEAM=Sales",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_get_examples():
        return [
            OpenApiExample(
                "TID - Get",
                value={
                    "identifier": "ORG=Kubefacets Inc,TEAM=Sales",
                    "slug": "sales",
                    "name": "Sales",
                },
                request_only=False,
                response_only=True,
            )
        ]

    @staticmethod
    def modelviewset_create_examples():
        return [
            OpenApiExample(
                "TID - Create",
                value={
                    "identifier": "ORG=Kubefacets Inc,TEAM=Sales",
                    "slug": "sales",
                    "name": "Sales",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "TID - Create",
                value={
                    "identifier": "ORG=Kubefacets Inc,TEAM=Sales",
                    "slug": "sales",
                    "name": "Sales",
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
                        "TID - Delete",
                        summary="TID Identifier",
                        description="TID - Delete",
                        value="ORG=Kubefacets Inc,TEAM=Sales",
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
                        "TID - Patch",
                        summary="TID Identifier",
                        description="TID - Patch",
                        value="ORG=Kubefacets Inc,TEAM=Sales",
                    )
                ],
            )
        ]

    @staticmethod
    def modelviewset_patch_examples():
        return [
            OpenApiExample(
                "TID - Patch",
                value={
                    "slug": "sales1",
                },
                request_only=True,
                response_only=False,
            ),
            OpenApiExample(
                "TID - Patch",
                value={
                    "identifier": "ORG=Kubefacets Inc,TEAM=Sales",
                    "slug": "sales1",
                    "name": "Sales",
                },
                request_only=False,
                response_only=True,
            ),
        ]
