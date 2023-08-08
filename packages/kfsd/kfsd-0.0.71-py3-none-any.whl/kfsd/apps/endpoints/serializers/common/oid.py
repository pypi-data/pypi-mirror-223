from kfsd.apps.endpoints.serializers.common.id import IDModelSerializer
from kfsd.apps.models.tables.oid import OID


class OIDModelSerializer(IDModelSerializer):
    class Meta:
        model = OID
        fields = "__all__"


class OIDViewModelSerializer(OIDModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = OID
        exclude = ("created", "updated", "id")
