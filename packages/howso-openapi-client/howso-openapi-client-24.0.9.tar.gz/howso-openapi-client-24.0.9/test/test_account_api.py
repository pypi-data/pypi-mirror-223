# coding: utf-8

"""
Howso API

OpenAPI implementation for interacting with the Howso API. 
"""

from __future__ import absolute_import

import unittest
from unittest import mock

import howso.openapi
from howso.openapi import models
from howso.openapi.api_client import ApiClient
from howso.openapi.configuration import Configuration
from howso.openapi.api.account_api import AccountApi  # noqa: E501
from howso.openapi.exceptions import ApiTypeError


def get_config():
    conf = Configuration()
    conf.client_side_validation = False
    return conf


@mock.patch('howso.openapi.configuration.Configuration.get_default_copy', side_effect=get_config)  # noqa: E501
@mock.patch('howso.openapi.api.account_api.ApiClient.call_api', return_value='Mocked Return')  # noqa: E501
class TestAccountApi(unittest.TestCase):
    """AccountApi unit test stubs"""

    def setUp(self):
        self.api = howso.openapi.api.account_api.AccountApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_account_api_init(self, *args):
        """Test case for AccountApi init"""
        api_client = ApiClient()
        api = howso.openapi.api.account_api.AccountApi(api_client)  # noqa: E501
        assert api.api_client == api_client
        assert self.api.api_client != api.api_client

    def test_me(self, mock_call_api, *args):
        """Test case for me

        Get your account details.  # noqa: E501
        """
        local_var_params = {
        }
        self.api.me(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}

        # Test for query params
        query_params = []

        # Test for header params
        header_params = {}

        # Test for form params
        form_params = []
        local_var_files = {}

        # Test for body params
        body_params = None
        # Test for HTTP header `Accept`
        header_params['Accept'] = self.api.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Test for auth settings
        auth_settings = ['oauth_ums']  # noqa: E501

        # Test for response types
        response_types_map = {
            200: "Account",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/manage/accounts/me/',
            'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_types_map=response_types_map,
            auth_settings=auth_settings,
            async_req=mock.ANY,
            _return_http_data_only=mock.ANY,
            _preload_content=mock.ANY,
            _request_timeout=mock.ANY,
            collection_formats=mock.ANY,
            _request_auth=mock.ANY
        )

    def test_me_with_unexpected_params(self, mock_call_api, *args):
        """Test case for me with bad parameters"""
        params = dict(
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.me,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()


if __name__ == '__main__':
    unittest.main()
