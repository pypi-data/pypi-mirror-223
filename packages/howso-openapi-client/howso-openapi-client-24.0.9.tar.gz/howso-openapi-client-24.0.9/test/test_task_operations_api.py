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
from howso.openapi.api.task_operations_api import TaskOperationsApi  # noqa: E501
from howso.openapi.exceptions import ApiTypeError


def get_config():
    conf = Configuration()
    conf.client_side_validation = False
    return conf


@mock.patch('howso.openapi.configuration.Configuration.get_default_copy', side_effect=get_config)  # noqa: E501
@mock.patch('howso.openapi.api.task_operations_api.ApiClient.call_api', return_value='Mocked Return')  # noqa: E501
class TestTaskOperationsApi(unittest.TestCase):
    """TaskOperationsApi unit test stubs"""

    def setUp(self):
        self.api = howso.openapi.api.task_operations_api.TaskOperationsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_task_operations_api_init(self, *args):
        """Test case for TaskOperationsApi init"""
        api_client = ApiClient()
        api = howso.openapi.api.task_operations_api.TaskOperationsApi(api_client)  # noqa: E501
        assert api.api_client == api_client
        assert self.api.api_client != api.api_client

    def test_cancel_action(self, mock_call_api, *args):
        """Test case for cancel_action

        Cancel an async action  # noqa: E501
        """
        local_var_params = {
            'action_id': 'action_id_example',
        }
        self.api.cancel_action(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
        if 'action_id' in local_var_params:
            path_params['action_id'] = local_var_params['action_id']  # noqa: E501

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
            200: "AsyncActionCancel",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/operations/actions/{action_id}/cancel',
            'PUT',
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

    def test_cancel_action_with_unexpected_params(self, mock_call_api, *args):
        """Test case for cancel_action with bad parameters"""
        params = dict(
            action_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.cancel_action,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_action(self, mock_call_api, *args):
        """Test case for get_action

        Status of an async action  # noqa: E501
        """
        local_var_params = {
            'action_id': 'action_id_example',
        }
        self.api.get_action(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
        if 'action_id' in local_var_params:
            path_params['action_id'] = local_var_params['action_id']  # noqa: E501

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
            200: "AsyncAction",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/operations/actions/{action_id}',
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

    def test_get_action_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_action with bad parameters"""
        params = dict(
            action_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_action,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_action_output(self, mock_call_api, *args):
        """Test case for get_action_output

        Output of an async action  # noqa: E501
        """
        local_var_params = {
            'action_id': 'action_id_example',
        }
        self.api.get_action_output(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
        if 'action_id' in local_var_params:
            path_params['action_id'] = local_var_params['action_id']  # noqa: E501

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
            200: "AsyncActionOutput",
            202: "AsyncActionStatus",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
            410: "Error",
        }

        mock_call_api.assert_called_with(
            '/operations/actions/{action_id}/output',
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

    def test_get_action_output_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_action_output with bad parameters"""
        params = dict(
            action_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_action_output,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_list_pending_actions(self, mock_call_api, *args):
        """Test case for list_pending_actions

        List pending async actions.  # noqa: E501
        """
        local_var_params = {
            'search': 'search_example',
            'ordering': 'ordering_example',
        }
        self.api.list_pending_actions(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}

        # Test for query params
        query_params = []
        if 'search' in local_var_params and local_var_params['search'] is not None:  # noqa: E501
            query_params.append(('search', local_var_params['search']))  # noqa: E501
        if 'ordering' in local_var_params and local_var_params['ordering'] is not None:  # noqa: E501
            query_params.append(('ordering', local_var_params['ordering']))  # noqa: E501

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
            200: "list[AsyncAction]",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/operations/actions',
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

    def test_list_pending_actions_with_unexpected_params(self, mock_call_api, *args):
        """Test case for list_pending_actions with bad parameters"""
        params = dict(
            
            
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.list_pending_actions,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_list_pending_trainee_actions(self, mock_call_api, *args):
        """Test case for list_pending_trainee_actions

        List pending trainee async actions.  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'search': 'search_example',
            'ordering': 'ordering_example',
        }
        self.api.list_pending_trainee_actions(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
        if 'trainee_id' in local_var_params:
            path_params['trainee_id'] = local_var_params['trainee_id']  # noqa: E501

        # Test for query params
        query_params = []
        if 'search' in local_var_params and local_var_params['search'] is not None:  # noqa: E501
            query_params.append(('search', local_var_params['search']))  # noqa: E501
        if 'ordering' in local_var_params and local_var_params['ordering'] is not None:  # noqa: E501
            query_params.append(('ordering', local_var_params['ordering']))  # noqa: E501

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
            200: "list[AsyncAction]",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/actions',
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

    def test_list_pending_trainee_actions_with_unexpected_params(self, mock_call_api, *args):
        """Test case for list_pending_trainee_actions with bad parameters"""
        params = dict(
            trainee_id=None, 
            
            
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.list_pending_trainee_actions,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()


if __name__ == '__main__':
    unittest.main()
