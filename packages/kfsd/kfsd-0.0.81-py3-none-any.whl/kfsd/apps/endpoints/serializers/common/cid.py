from kfsd.apps.endpoints.serializers.common.id import IDModelSerializer
from kfsd.apps.models.tables.cid import CID


class CIDModelSerializer(IDModelSerializer):
    class Meta:
        model = CID
        fields = "__all__"


class CIDViewModelSerializer(CIDModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = CID
        exclude = ("created", "updated", "id")
