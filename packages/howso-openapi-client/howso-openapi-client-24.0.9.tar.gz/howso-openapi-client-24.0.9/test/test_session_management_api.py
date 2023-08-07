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
from howso.openapi.api.session_management_api import SessionManagementApi  # noqa: E501
from howso.openapi.exceptions import ApiTypeError


def get_config():
    conf = Configuration()
    conf.client_side_validation = False
    return conf


@mock.patch('howso.openapi.configuration.Configuration.get_default_copy', side_effect=get_config)  # noqa: E501
@mock.patch('howso.openapi.api.session_management_api.ApiClient.call_api', return_value='Mocked Return')  # noqa: E501
class TestSessionManagementApi(unittest.TestCase):
    """SessionManagementApi unit test stubs"""

    def setUp(self):
        self.api = howso.openapi.api.session_management_api.SessionManagementApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_session_management_api_init(self, *args):
        """Test case for SessionManagementApi init"""
        api_client = ApiClient()
        api = howso.openapi.api.session_management_api.SessionManagementApi(api_client)  # noqa: E501
        assert api.api_client == api_client
        assert self.api.api_client != api.api_client

    def test_begin_session(self, mock_call_api, *args):
        """Test case for begin_session

        Start a new session.  # noqa: E501
        """
        local_var_params = {
            'begin_session_request': models.BeginSessionRequest(
                name='session_1',
                metadata={ },
            ),
        }
        self.api.begin_session(**local_var_params)
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
        if 'begin_session_request' in local_var_params:
            body_params = local_var_params['begin_session_request']
        # Test for HTTP header `Accept`
        header_params['Accept'] = self.api.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Test for HTTP header `Content-Type`
        header_params['Content-Type'] = self.api.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Test for auth settings
        auth_settings = ['oauth_ums']  # noqa: E501

        # Test for response types
        response_types_map = {
            201: "Session",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/session',
            'POST',
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

    def test_begin_session_with_unexpected_params(self, mock_call_api, *args):
        """Test case for begin_session with bad parameters"""
        params = dict(
            begin_session_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.begin_session,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_active_session(self, mock_call_api, *args):
        """Test case for get_active_session

        Get active session.  # noqa: E501
        """
        local_var_params = {
        }
        self.api.get_active_session(**local_var_params)
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
            200: "Session",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/session',
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

    def test_get_active_session_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_active_session with bad parameters"""
        params = dict(
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_active_session,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_session(self, mock_call_api, *args):
        """Test case for get_session

        Get a session's details.  # noqa: E501
        """
        local_var_params = {
            'session_id': 'session_id_example',
        }
        self.api.get_session(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
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
            200: "Session",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/manage/sessions/{session_id}/',
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

    def test_get_session_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_session with bad parameters"""
        params = dict(
            session_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_session,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_list_sessions(self, mock_call_api, *args):
        """Test case for list_sessions

        List your sessions.  # noqa: E501
        """
        local_var_params = {
            'search': 'search_example',
            'project': 'project_example',
        }
        self.api.list_sessions(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}

        # Test for query params
        query_params = []
        if 'search' in local_var_params and local_var_params['search'] is not None:  # noqa: E501
            query_params.append(('search', local_var_params['search']))  # noqa: E501
        if 'project' in local_var_params and local_var_params['project'] is not None:  # noqa: E501
            query_params.append(('project', local_var_params['project']))  # noqa: E501

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
            200: "list[Session]",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/manage/sessions/',
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

    def test_list_sessions_with_unexpected_params(self, mock_call_api, *args):
        """Test case for list_sessions with bad parameters"""
        params = dict(
            
            
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.list_sessions,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_update_session(self, mock_call_api, *args):
        """Test case for update_session

        Update a session.  # noqa: E501
        """
        local_var_params = {
            'session_id': 'session_id_example',
            'update_session_request': models.UpdateSessionRequest(
                metadata={ },
            ),
        }
        self.api.update_session(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
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
        if 'update_session_request' in local_var_params:
            body_params = local_var_params['update_session_request']
        # Test for HTTP header `Accept`
        header_params['Accept'] = self.api.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Test for HTTP header `Content-Type`
        header_params['Content-Type'] = self.api.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Test for auth settings
        auth_settings = ['oauth_ums']  # noqa: E501

        # Test for response types
        response_types_map = {
            200: "Session",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/manage/sessions/{session_id}/',
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

    def test_update_session_with_unexpected_params(self, mock_call_api, *args):
        """Test case for update_session with bad parameters"""
        params = dict(
            session_id=None, 
            update_session_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.update_session,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()


if __name__ == '__main__':
    unittest.main()
