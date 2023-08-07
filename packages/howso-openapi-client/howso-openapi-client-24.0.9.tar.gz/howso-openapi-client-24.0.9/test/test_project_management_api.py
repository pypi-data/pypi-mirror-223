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
from howso.openapi.api.project_management_api import ProjectManagementApi  # noqa: E501
from howso.openapi.exceptions import ApiTypeError


def get_config():
    conf = Configuration()
    conf.client_side_validation = False
    return conf


@mock.patch('howso.openapi.configuration.Configuration.get_default_copy', side_effect=get_config)  # noqa: E501
@mock.patch('howso.openapi.api.project_management_api.ApiClient.call_api', return_value='Mocked Return')  # noqa: E501
class TestProjectManagementApi(unittest.TestCase):
    """ProjectManagementApi unit test stubs"""

    def setUp(self):
        self.api = howso.openapi.api.project_management_api.ProjectManagementApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_project_management_api_init(self, *args):
        """Test case for ProjectManagementApi init"""
        api_client = ApiClient()
        api = howso.openapi.api.project_management_api.ProjectManagementApi(api_client)  # noqa: E501
        assert api.api_client == api_client
        assert self.api.api_client != api.api_client

    def test_create_project(self, mock_call_api, *args):
        """Test case for create_project

        Create a project.  # noqa: E501
        """
        local_var_params = {
            'project_identity': models.ProjectIdentity(
                id='12d99ae5-e8a2-4232-a256-81b3eb913d16',
                name='My Project',
            ),
        }
        self.api.create_project(**local_var_params)
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
        if 'project_identity' in local_var_params:
            body_params = local_var_params['project_identity']
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
            201: "Project",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/manage/projects/',
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

    def test_create_project_with_unexpected_params(self, mock_call_api, *args):
        """Test case for create_project with bad parameters"""
        params = dict(
            project_identity=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.create_project,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_delete_project(self, mock_call_api, *args):
        """Test case for delete_project

        Delete a project.  # noqa: E501
        """
        local_var_params = {
            'project_id': 'project_id_example',
        }
        self.api.delete_project(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
        if 'project_id' in local_var_params:
            path_params['project_id'] = local_var_params['project_id']  # noqa: E501

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
            '/manage/projects/{project_id}/',
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

    def test_delete_project_with_unexpected_params(self, mock_call_api, *args):
        """Test case for delete_project with bad parameters"""
        params = dict(
            project_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.delete_project,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_project(self, mock_call_api, *args):
        """Test case for get_project

        Get a project's details.  # noqa: E501
        """
        local_var_params = {
            'project_id': 'project_id_example',
        }
        self.api.get_project(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
        if 'project_id' in local_var_params:
            path_params['project_id'] = local_var_params['project_id']  # noqa: E501

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
            200: "Project",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/manage/projects/{project_id}/',
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

    def test_get_project_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_project with bad parameters"""
        params = dict(
            project_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_project,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_list_projects(self, mock_call_api, *args):
        """Test case for list_projects

        List your projects.  # noqa: E501
        """
        local_var_params = {
            'search': 'search_example',
        }
        self.api.list_projects(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}

        # Test for query params
        query_params = []
        if 'search' in local_var_params and local_var_params['search'] is not None:  # noqa: E501
            query_params.append(('search', local_var_params['search']))  # noqa: E501

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
            200: "list[Project]",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/manage/projects/',
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

    def test_list_projects_with_unexpected_params(self, mock_call_api, *args):
        """Test case for list_projects with bad parameters"""
        params = dict(
            
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.list_projects,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_update_project(self, mock_call_api, *args):
        """Test case for update_project

        Update a project.  # noqa: E501
        """
        local_var_params = {
            'project_id': 'project_id_example',
            'project_identity': models.ProjectIdentity(
                id='12d99ae5-e8a2-4232-a256-81b3eb913d16',
                name='My Project',
            ),
        }
        self.api.update_project(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
        if 'project_id' in local_var_params:
            path_params['project_id'] = local_var_params['project_id']  # noqa: E501

        # Test for query params
        query_params = []

        # Test for header params
        header_params = {}

        # Test for form params
        form_params = []
        local_var_files = {}

        # Test for body params
        body_params = None
        if 'project_identity' in local_var_params:
            body_params = local_var_params['project_identity']
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
            200: "Project",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/manage/projects/{project_id}/',
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

    def test_update_project_with_unexpected_params(self, mock_call_api, *args):
        """Test case for update_project with bad parameters"""
        params = dict(
            project_id=None, 
            project_identity=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.update_project,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()


if __name__ == '__main__':
    unittest.main()
