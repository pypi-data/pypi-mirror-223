from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.tid import TID
from kfsd.apps.endpoints.serializers.common.tid import TIDViewModelSerializer
from kfsd.apps.endpoints.views.docs.tid import TIDDoc


@extend_schema_view(**TIDDoc.modelviewset())
class TIDModelViewSet(CustomModelViewSet):
    queryset = TID.objects.all()
    serializer_class = TIDViewModelSerializer
