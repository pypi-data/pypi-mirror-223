from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from kfsd.apps.endpoints.tests.endpoints_test_handler import EndpointsTestHandler


class PIDEndpointTestCases(EndpointsTestHandler):
    fixtures = ["v1/tests/common/ids.json"]

    def setUp(self):
        self.__pidListUrl = reverse("pid-list")
        super().setUp()

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_list_pid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        currentPg = 1
        obsResponse = self.list(self.__pidListUrl, currentPg, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_list_pid.json"
        )
        self.assertEqual(obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_get_pid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        dataIdentifier = "ORG=Kubefacets Inc,PRJ=Config"
        obsResponse = self.get("pid-detail", dataIdentifier, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_get_pid.json"
        )
        self.assertEqual(obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_create_pid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        requestData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/test_create_pid.json"
        )
        self.__obsResponse = self.create(
            self.__pidListUrl, requestData, status.HTTP_201_CREATED
        )

        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_create_pid.json"
        )
        self.assertEqual(self.__obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_patch_pid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
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
            "kfsd/apps/endpoints/tests/v1/common/data/requests/test_create_pid.json"
        )
        self.__obsResponse = self.create(
            self.__pidListUrl, requestData, status.HTTP_201_CREATED
        )

        # Test Patch
        identifier = "ORG=Kubefacets Inc,PRJ=Config1"
        requestData = {"slug": "config2"}
        obsResponse = self.patch(
            "pid-detail", identifier, requestData, status.HTTP_200_OK
        )
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_patch_pid.json"
        )
        self.assertEqual(obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_delete_pid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        identifier = "ORG=Kubefacets Inc,PRJ=Config"
        self.delete("pid-detail", identifier, status.HTTP_204_NO_CONTENT)
        # should return not found as it's already deleted
        self.delete("pid-detail", identifier, status.HTTP_404_NOT_FOUND)
