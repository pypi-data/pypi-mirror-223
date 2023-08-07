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
from howso.openapi.api.trainee_session_management_api import TraineeSessionManagementApi  # noqa: E501
from howso.openapi.exceptions import ApiTypeError


def get_config():
    conf = Configuration()
    conf.client_side_validation = False
    return conf


@mock.patch('howso.openapi.configuration.Configuration.get_default_copy', side_effect=get_config)  # noqa: E501
@mock.patch('howso.openapi.api.trainee_session_management_api.ApiClient.call_api', return_value='Mocked Return')  # noqa: E501
class TestTraineeSessionManagementApi(unittest.TestCase):
    """TraineeSessionManagementApi unit test stubs"""

    def setUp(self):
        self.api = howso.openapi.api.trainee_session_management_api.TraineeSessionManagementApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_trainee_session_management_api_init(self, *args):
        """Test case for TraineeSessionManagementApi init"""
        api_client = ApiClient()
        api = howso.openapi.api.trainee_session_management_api.TraineeSessionManagementApi(api_client)  # noqa: E501
        assert api.api_client == api_client
        assert self.api.api_client != api.api_client

    def test_delete_trainee_session(self, mock_call_api, *args):
        """Test case for delete_trainee_session

        Remove session from trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'session_id': 'session_id_example',
        }
        self.api.delete_trainee_session(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
        if 'trainee_id' in local_var_params:
            path_params['trainee_id'] = local_var_params['trainee_id']  # noqa: E501
        if 'session_id' in local_var_params:
            path_params['session_id'] = local_var_params['session_id']  # noqa: E501

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
        response_types_map = {}

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/session/{session_id}',
            'DELETE',
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

    def test_delete_trainee_session_with_unexpected_params(self, mock_call_api, *args):
        """Test case for delete_trainee_session with bad parameters"""
        params = dict(
            trainee_id=None, 
            session_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.delete_trainee_session,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_trainee_session_indices(self, mock_call_api, *args):
        """Test case for get_trainee_session_indices

        Retrieves the session indices for the provided session.  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'session_id': 'session_id_example',
        }
        self.api.get_trainee_session_indices(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
        if 'trainee_id' in local_var_params:
            path_params['trainee_id'] = local_var_params['trainee_id']  # noqa: E501
        if 'session_id' in local_var_params:
            path_params['session_id'] = local_var_params['session_id']  # noqa: E501

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
            200: "list[int]",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/session/{session_id}/indices',
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

    def test_get_trainee_session_indices_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_trainee_session_indices with bad parameters"""
        params = dict(
            trainee_id=None, 
            session_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_trainee_session_indices,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_trainee_session_training_indices(self, mock_call_api, *args):
        """Test case for get_trainee_session_training_indices

        Retrieves the session training indices for the provided session.  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'session_id': 'session_id_example',
        }
        self.api.get_trainee_session_training_indices(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
        if 'trainee_id' in local_var_params:
            path_params['trainee_id'] = local_var_params['trainee_id']  # noqa: E501
        if 'session_id' in local_var_params:
            path_params['session_id'] = local_var_params['session_id']  # noqa: E501

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
            200: "list[int]",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/session/{session_id}/training-indices',
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

    def test_get_trainee_session_training_indices_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_trainee_session_training_indices with bad parameters"""
        params = dict(
            trainee_id=None, 
            session_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_trainee_session_training_indices,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_trainee_sessions(self, mock_call_api, *args):
        """Test case for get_trainee_sessions

        Get all session IDs for a trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
        }
        self.api.get_trainee_sessions(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
        if 'trainee_id' in local_var_params:
            path_params['trainee_id'] = local_var_params['trainee_id']  # noqa: E501

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
            200: "list[SessionIdentity]",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/sessions',
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

    def test_get_trainee_sessions_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_trainee_sessions with bad parameters"""
        params = dict(
            trainee_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_trainee_sessions,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()


if __name__ == '__main__':
    unittest.main()
