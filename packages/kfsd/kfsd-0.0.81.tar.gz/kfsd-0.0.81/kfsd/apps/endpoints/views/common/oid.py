from drf_spectacular.utils import extend_schema_view

from kfsd.apps.endpoints.views.common.custom_model import CustomModelViewSet
from kfsd.apps.models.tables.oid import OID
from kfsd.apps.endpoints.serializers.common.oid import OIDViewModelSerializer
from kfsd.apps.endpoints.views.docs.oid import OIDDoc


@extend_schema_view(**OIDDoc.modelviewset())
class OIDModelViewSet(CustomModelViewSet):
    queryset = OID.objects.all()
    serializer_class = OIDViewModelSerializer
