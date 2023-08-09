from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView
from rest_framework import routers
from kfsd.apps.endpoints.views.common.cid import CIDModelViewSet
from kfsd.apps.endpoints.views.common.pid import PIDModelViewSet
from kfsd.apps.endpoints.views.common.tid import TIDModelViewSet
from kfsd.apps.endpoints.views.common.uid import UIDModelViewSet
from kfsd.apps.endpoints.views.common.oid import OIDModelViewSet
from kfsd.apps.endpoints.views.utils.utils import UtilsViewSet
from kfsd.apps.endpoints.views.utils.common import CommonViewSet
from kfsd.apps.endpoints.views.common.outpost import OutpostModelViewSet

router = routers.DefaultRouter()
router.include_format_suffixes = False

router.register("cids", CIDModelViewSet, basename="cid")
router.register("pids", PIDModelViewSet, basename="pid")
router.register("tids", TIDModelViewSet, basename="tid")
router.register("oids", OIDModelViewSet, basename="oid")
router.register("uids", UIDModelViewSet, basename="uid")
router.register("utils", UtilsViewSet, basename="utils")
router.register("common", CommonViewSet, basename="common")
router.register("outpost", OutpostModelViewSet, basename="outpost")

urlpatterns = [
    path("", include(router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema-api"),
]
