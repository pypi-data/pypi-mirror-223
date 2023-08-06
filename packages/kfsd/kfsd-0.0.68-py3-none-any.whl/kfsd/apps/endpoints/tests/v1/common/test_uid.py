from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from kfsd.apps.endpoints.tests.endpoints_test_handler import EndpointsTestHandler


class UIDEndpointTestCases(EndpointsTestHandler):
    fixtures = ["v1/tests/common/ids.json"]

    def setUp(self):
        self.__uidListUrl = reverse("uid-list")
        super().setUp()

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_list_uid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        currentPg = 1
        obsResponse = self.list(self.__uidListUrl, currentPg, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_list_uid.json"
        )
        self.assertEqual(obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_get_uid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        dataIdentifier = "USER=admin@kubefacets.com"
        obsResponse = self.get("uid-detail", dataIdentifier, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_get_uid.json"
        )
        self.assertEqual(obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_create_uid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        requestData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/test_create_uid.json"
        )
        self.__obsResponse = self.create(
            self.__uidListUrl, requestData, status.HTTP_201_CREATED
        )

        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_create_uid.json"
        )
        self.assertEqual(self.__obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_patch_uid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
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
            "kfsd/apps/endpoints/tests/v1/common/data/requests/test_create_uid.json"
        )
        self.__obsResponse = self.create(
            self.__uidListUrl, requestData, status.HTTP_201_CREATED
        )

        # Test Patch
        identifier = "USER=gokul@kubefacets.com"
        requestData = {"slug": "gokul1"}
        obsResponse = self.patch(
            "uid-detail", identifier, requestData, status.HTTP_200_OK
        )
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_patch_uid.json"
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

        identifier = "USER=admin@kubefacets.com"
        self.delete("uid-detail", identifier, status.HTTP_204_NO_CONTENT)
        # should return not found as it's already deleted
        self.delete("uid-detail", identifier, status.HTTP_404_NOT_FOUND)
