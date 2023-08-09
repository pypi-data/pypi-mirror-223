from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from kfsd.apps.endpoints.tests.endpoints_test_handler import EndpointsTestHandler


class OIDEndpointTestCases(EndpointsTestHandler):
    fixtures = ["v1/tests/common/ids.json"]

    def setUp(self):
        self.__oidListUrl = reverse("oid-list")
        super().setUp()

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_list_oid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        currentPg = 1
        obsResponse = self.list(self.__oidListUrl, currentPg, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_list_oid.json"
        )
        self.assertEqual(obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_get_oid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        dataIdentifier = "ORG=Kubefacets Inc"
        obsResponse = self.get("oid-detail", dataIdentifier, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_get_oid.json"
        )
        self.assertEqual(obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_create_oid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        requestData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/test_create_oid.json"
        )
        self.__obsResponse = self.create(
            self.__oidListUrl, requestData, status.HTTP_201_CREATED
        )

        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_create_oid.json"
        )
        self.assertEqual(self.__obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_patch_oid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        # Create Test data
        requestData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/test_create_oid.json"
        )
        self.__obsResponse = self.create(
            self.__oidListUrl, requestData, status.HTTP_201_CREATED
        )

        # Test Patch
        identifier = "ORG=SnappyGuide Inc"
        requestData = {"slug": "snappyguide"}
        obsResponse = self.patch(
            "oid-detail", identifier, requestData, status.HTTP_200_OK
        )
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_patch_oid.json"
        )
        self.assertEqual(obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_delete_uid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        identifier = "ORG=Kubefacets Inc"
        self.delete("oid-detail", identifier, status.HTTP_204_NO_CONTENT)
        # should return not found as it's already deleted
        self.delete("oid-detail", identifier, status.HTTP_404_NOT_FOUND)
