from kfsd.apps.endpoints.serializers.common.id import IDModelSerializer
from kfsd.apps.models.tables.uid import UID


class UIDModelSerializer(IDModelSerializer):
    class Meta:
        model = UID
        fields = "__all__"


class UIDViewModelSerializer(UIDModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = UID
        exclude = ("created", "updated", "id")
