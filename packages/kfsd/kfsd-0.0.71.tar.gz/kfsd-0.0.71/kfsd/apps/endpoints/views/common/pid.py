from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.pid import PID
from kfsd.apps.endpoints.serializers.common.pid import PIDViewModelSerializer
from kfsd.apps.endpoints.views.docs.pid import PIDDoc


@extend_schema_view(**PIDDoc.modelviewset())
class PIDModelViewSet(CustomModelViewSet):
    queryset = PID.objects.all()
    serializer_class = PIDViewModelSerializer
