from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.uid import UID
from kfsd.apps.endpoints.serializers.common.uid import UIDViewModelSerializer
from kfsd.apps.endpoints.views.docs.uid import UIDDoc


@extend_schema_view(**UIDDoc.modelviewset())
class UIDModelViewSet(CustomModelViewSet):
    queryset = UID.objects.all()
    serializer_class = UIDViewModelSerializer
