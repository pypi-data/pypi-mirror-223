from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.cid import CID
from kfsd.apps.endpoints.serializers.common.cid import CIDViewModelSerializer
from kfsd.apps.endpoints.views.docs.cid import CIDDoc


@extend_schema_view(**CIDDoc.modelviewset())
class CIDModelViewSet(CustomModelViewSet):
    queryset = CID.objects.all()
    serializer_class = CIDViewModelSerializer
