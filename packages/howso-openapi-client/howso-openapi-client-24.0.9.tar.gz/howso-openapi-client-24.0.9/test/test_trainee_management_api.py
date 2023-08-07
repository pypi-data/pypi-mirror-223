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
from howso.openapi.api.trainee_management_api import TraineeManagementApi  # noqa: E501
from howso.openapi.exceptions import ApiTypeError


def get_config():
    conf = Configuration()
    conf.client_side_validation = False
    return conf


@mock.patch('howso.openapi.configuration.Configuration.get_default_copy', side_effect=get_config)  # noqa: E501
@mock.patch('howso.openapi.api.trainee_management_api.ApiClient.call_api', return_value='Mocked Return')  # noqa: E501
class TestTraineeManagementApi(unittest.TestCase):
    """TraineeManagementApi unit test stubs"""

    def setUp(self):
        self.api = howso.openapi.api.trainee_management_api.TraineeManagementApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_trainee_management_api_init(self, *args):
        """Test case for TraineeManagementApi init"""
        api_client = ApiClient()
        api = howso.openapi.api.trainee_management_api.TraineeManagementApi(api_client)  # noqa: E501
        assert api.api_client == api_client
        assert self.api.api_client != api.api_client

    def test_acquire_trainee_resources(self, mock_call_api, *args):
        """Test case for acquire_trainee_resources

        Acquire Trainee resources  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'trainee_acquire_resources_request': models.TraineeAcquireResourcesRequest(
                timeout=0,
            ),
        }
        self.api.acquire_trainee_resources(**local_var_params)
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
        if 'trainee_acquire_resources_request' in local_var_params:
            body_params = local_var_params['trainee_acquire_resources_request']
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
            202: "AsyncActionAccepted",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/resources/acquire',
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

    def test_acquire_trainee_resources_with_unexpected_params(self, mock_call_api, *args):
        """Test case for acquire_trainee_resources with bad parameters"""
        params = dict(
            trainee_id=None, 
            
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.acquire_trainee_resources,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_copy_trainee(self, mock_call_api, *args):
        """Test case for copy_trainee

        Copy Trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'copy_trainee_request': models.CopyTraineeRequest(
                new_trainee_name='Trainee1 Copy',
                project_id='216abfb8-7c7b-47f6-9918-e69fbb2bfc13',
                library_type='st',
                resources=howso.openapi.models.trainee_resources.TraineeResources(
                    cpu = howso.openapi.models.cpu_limits.CPULimits(
                        minimum = 56, 
                        maximum = 56, ), 
                    memory = howso.openapi.models.memory_limits.MemoryLimits(
                        minimum = 56, 
                        maximum = 56, ), 
                    replicas = 1, ),
            ),
        }
        self.api.copy_trainee(**local_var_params)
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
        if 'copy_trainee_request' in local_var_params:
            body_params = local_var_params['copy_trainee_request']
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
            201: "Trainee",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/copy',
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

    def test_copy_trainee_with_unexpected_params(self, mock_call_api, *args):
        """Test case for copy_trainee with bad parameters"""
        params = dict(
            trainee_id=None, 
            
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.copy_trainee,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_create_trainee(self, mock_call_api, *args):
        """Test case for create_trainee

        Create Trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_create_request': models.TraineeCreateRequest(
                library_type='st',
                timeout=0,
                resources=howso.openapi.models.trainee_resources.TraineeResources(
                    cpu = howso.openapi.models.cpu_limits.CPULimits(
                        minimum = 56, 
                        maximum = 56, ), 
                    memory = howso.openapi.models.memory_limits.MemoryLimits(
                        minimum = 56, 
                        maximum = 56, ), 
                    replicas = 1, ),
                trainee={"name":"iris","features":{"sepal_length":{"type":"continuous"},"sepal_width":{"type":"continuous"},"class":{"type":"nominal"}}},
            ),
        }
        self.api.create_trainee(**local_var_params)
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
        if 'trainee_create_request' in local_var_params:
            body_params = local_var_params['trainee_create_request']
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
            202: "CreateTraineeActionAccepted",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainees',
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

    def test_create_trainee_with_unexpected_params(self, mock_call_api, *args):
        """Test case for create_trainee with bad parameters"""
        params = dict(
            trainee_create_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.create_trainee,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_delete_trainee(self, mock_call_api, *args):
        """Test case for delete_trainee

        Delete Trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
        }
        self.api.delete_trainee(**local_var_params)
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
        response_types_map = {}

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}',
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

    def test_delete_trainee_with_unexpected_params(self, mock_call_api, *args):
        """Test case for delete_trainee with bad parameters"""
        params = dict(
            trainee_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.delete_trainee,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_destruct_trainee(self, mock_call_api, *args):
        """Test case for destruct_trainee

        Teardown a trainee instance  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'force': True,
        }
        self.api.destruct_trainee(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}
        if 'trainee_id' in local_var_params:
            path_params['trainee_id'] = local_var_params['trainee_id']  # noqa: E501

        # Test for query params
        query_params = []
        if 'force' in local_var_params and local_var_params['force'] is not None:  # noqa: E501
            query_params.append(('force', local_var_params['force']))  # noqa: E501

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
            200: "DestructTraineeResponse",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/internal/trainee/{trainee_id}/destruct',
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

    def test_destruct_trainee_with_unexpected_params(self, mock_call_api, *args):
        """Test case for destruct_trainee with bad parameters"""
        params = dict(
            trainee_id=None, 
            
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.destruct_trainee,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_trainee(self, mock_call_api, *args):
        """Test case for get_trainee

        Get Trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
        }
        self.api.get_trainee(**local_var_params)
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
            200: "Trainee",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}',
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

    def test_get_trainee_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_trainee with bad parameters"""
        params = dict(
            trainee_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_trainee,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_list_trainees(self, mock_call_api, *args):
        """Test case for list_trainees

        List your trainees.  # noqa: E501
        """
        local_var_params = {
            'search': 'search_example',
            'project': 'project_example',
        }
        self.api.list_trainees(**local_var_params)
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
            200: "list[TraineeIdentity]",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/manage/trainees/',
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

    def test_list_trainees_with_unexpected_params(self, mock_call_api, *args):
        """Test case for list_trainees with bad parameters"""
        params = dict(
            
            
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.list_trainees,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_persist_trace(self, mock_call_api, *args):
        """Test case for persist_trace

        Persist trainee trace  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
        }
        self.api.persist_trace(**local_var_params)
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
            200: "TraceResponse",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/persist-trace',
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

    def test_persist_trace_with_unexpected_params(self, mock_call_api, *args):
        """Test case for persist_trace with bad parameters"""
        params = dict(
            trainee_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.persist_trace,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_persist_trainee(self, mock_call_api, *args):
        """Test case for persist_trainee

        Persist trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
        }
        self.api.persist_trainee(**local_var_params)
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
        response_types_map = {}

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/persist',
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

    def test_persist_trainee_with_unexpected_params(self, mock_call_api, *args):
        """Test case for persist_trainee with bad parameters"""
        params = dict(
            trainee_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.persist_trainee,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_release_trainee_resources(self, mock_call_api, *args):
        """Test case for release_trainee_resources

        Release Trainee resources  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
        }
        self.api.release_trainee_resources(**local_var_params)
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
        response_types_map = {}

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/resources/release',
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

    def test_release_trainee_resources_with_unexpected_params(self, mock_call_api, *args):
        """Test case for release_trainee_resources with bad parameters"""
        params = dict(
            trainee_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.release_trainee_resources,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_resolve_trainee(self, mock_call_api, *args):
        """Test case for resolve_trainee

        """
        local_var_params = {
            'name': 'name_example',
            'project': 'project_example',
        }
        self.api.resolve_trainee(**local_var_params)
        collection_formats = {}

        # Test for path params
        path_params = {}

        # Test for query params
        query_params = []
        if 'name' in local_var_params and local_var_params['name'] is not None:  # noqa: E501
            query_params.append(('name', local_var_params['name']))  # noqa: E501
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
            200: "TraineeIdentity",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
            409: "Error",
        }

        mock_call_api.assert_called_with(
            '/manage/trainees/resolve/',
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

    def test_resolve_trainee_with_unexpected_params(self, mock_call_api, *args):
        """Test case for resolve_trainee with bad parameters"""
        params = dict(
            name=None, 
            
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.resolve_trainee,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_self_destruct_trainee(self, mock_call_api, *args):
        """Test case for self_destruct_trainee

        Unexpectedly fail a trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
        }
        self.api.self_destruct_trainee(**local_var_params)
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
        response_types_map = {}

        mock_call_api.assert_called_with(
            '/internal/trainee/{trainee_id}/destruct',
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

    def test_self_destruct_trainee_with_unexpected_params(self, mock_call_api, *args):
        """Test case for self_destruct_trainee with bad parameters"""
        params = dict(
            trainee_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.self_destruct_trainee,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_set_random_seed(self, mock_call_api, *args):
        """Test case for set_random_seed

        Set Trainee's random seed  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'random_seed_request': models.RandomSeedRequest(
                seed='myseed1',
            ),
        }
        self.api.set_random_seed(**local_var_params)
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
        if 'random_seed_request' in local_var_params:
            body_params = local_var_params['random_seed_request']
        # Test for HTTP header `Accept`
        header_params['Accept'] = self.api.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Test for HTTP header `Content-Type`
        header_params['Content-Type'] = self.api.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Test for auth settings
        auth_settings = ['oauth_ums']  # noqa: E501

        # Test for response types
        response_types_map = {}

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/random-seed',
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

    def test_set_random_seed_with_unexpected_params(self, mock_call_api, *args):
        """Test case for set_random_seed with bad parameters"""
        params = dict(
            trainee_id=None, 
            random_seed_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.set_random_seed,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_set_trainee(self, mock_call_api, *args):
        """Test case for set_trainee

        Set Trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'trainee_request': models.TraineeRequest(
            ),
        }
        self.api.set_trainee(**local_var_params)
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
        if 'trainee_request' in local_var_params:
            body_params = local_var_params['trainee_request']
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
            200: "Trainee",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}',
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

    def test_set_trainee_with_unexpected_params(self, mock_call_api, *args):
        """Test case for set_trainee with bad parameters"""
        params = dict(
            trainee_id=None, 
            trainee_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.set_trainee,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()


if __name__ == '__main__':
    unittest.main()
