from kfsd.apps.endpoints.serializers.common.id import IDModelSerializer
from kfsd.apps.models.tables.pid import PID


class PIDModelSerializer(IDModelSerializer):
    class Meta:
        model = PID
        fields = "__all__"


class PIDViewModelSerializer(PIDModelSerializer):
    id = None
    created = None
    updated = None

    class Meta:
        model = PID
        exclude = ("created", "updated", "id")
