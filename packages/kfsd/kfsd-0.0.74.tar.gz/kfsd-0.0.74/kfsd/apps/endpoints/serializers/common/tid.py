from kfsd.apps.endpoints.serializers.common.id import IDModelSerializer
from kfsd.apps.models.tables.tid import TID


class TIDModelSerializer(IDModelSerializer):
    class Meta:
        model = TID
        fields = "__all__"


class TIDViewModelSerializer(TIDModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = TID
        exclude = ("created", "updated", "id")
