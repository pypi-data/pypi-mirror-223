from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from kfsd.apps.endpoints.tests.endpoints_test_handler import EndpointsTestHandler


class CIDEndpointTestCases(EndpointsTestHandler):
    fixtures = ["v1/tests/common/ids.json"]

    def setUp(self):
        self.__cidListUrl = reverse("cid-list")
        super().setUp()

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_list_cid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        currentPg = 1
        obsResponse = self.list(self.__cidListUrl, currentPg, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_list_cid.json"
        )
        self.assertEqual(obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_get_cid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        dataIdentifier = "ORG=Kubefacets Inc,PRJ=Config,COLL=SSO"
        obsResponse = self.get("cid-detail", dataIdentifier, status.HTTP_200_OK)
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_get_cid.json"
        )
        self.assertEqual(obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_create_cid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        requestData = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/test_create_cid.json"
        )
        self.__obsResponse = self.create(
            self.__cidListUrl, requestData, status.HTTP_201_CREATED
        )

        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_create_cid.json"
        )
        self.assertEqual(self.__obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_patch_cid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
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
            "kfsd/apps/endpoints/tests/v1/common/data/requests/test_create_cid.json"
        )
        self.__obsResponse = self.create(
            self.__cidListUrl, requestData, status.HTTP_201_CREATED
        )

        # Test Patch
        identifier = "ORG=Kubefacets Inc,PRJ=Config,COLL=FE"
        requestData = {"slug": "frontend"}
        obsResponse = self.patch(
            "cid-detail", identifier, requestData, status.HTTP_200_OK
        )
        expResponse = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/responses/test_patch_cid.json"
        )
        self.assertEqual(obsResponse, expResponse)

    @patch("kfsd.apps.core.auth.api.token.TokenAuth.getTokenUserInfo")
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.getLocalKubefacetsSettingsConfig"
    )
    @patch(
        "kfsd.apps.core.common.kubefacets_config.KubefacetsConfig.deriveRemoteConfig"
    )
    def test_delete_cid(self, remoteConfigMocked, rawSettingsMocked, tokenUserMocked):
        rawConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_settings.json"
        )
        remoteConfig = self.readJSONData(
            "kfsd/apps/endpoints/tests/v1/common/data/requests/kubefacets/remote_config_resp.json"
        )
        rawSettingsMocked.return_value = rawConfig
        remoteConfigMocked.return_value = remoteConfig

        identifier = "ORG=Kubefacets Inc,PRJ=Config,COLL=SSO"
        self.delete("cid-detail", identifier, status.HTTP_204_NO_CONTENT)
        # should return not found as it's already deleted
        self.delete("cid-detail", identifier, status.HTTP_404_NOT_FOUND)
