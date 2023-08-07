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
from howso.openapi.api.trainee_case_operations_api import TraineeCaseOperationsApi  # noqa: E501
from howso.openapi.exceptions import ApiTypeError


def get_config():
    conf = Configuration()
    conf.client_side_validation = False
    return conf


@mock.patch('howso.openapi.configuration.Configuration.get_default_copy', side_effect=get_config)  # noqa: E501
@mock.patch('howso.openapi.api.trainee_case_operations_api.ApiClient.call_api', return_value='Mocked Return')  # noqa: E501
class TestTraineeCaseOperationsApi(unittest.TestCase):
    """TraineeCaseOperationsApi unit test stubs"""

    def setUp(self):
        self.api = howso.openapi.api.trainee_case_operations_api.TraineeCaseOperationsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_trainee_case_operations_api_init(self, *args):
        """Test case for TraineeCaseOperationsApi init"""
        api_client = ApiClient()
        api = howso.openapi.api.trainee_case_operations_api.TraineeCaseOperationsApi(api_client)  # noqa: E501
        assert api.api_client == api_client
        assert self.api.api_client != api.api_client

    def test_edit_cases(self, mock_call_api, *args):
        """Test case for edit_cases

        Edit one or more cases in a trainee.  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'case_edit_request': models.CaseEditRequest(
                features=["age","gender"],
                feature_values=[18,"male"],
                case_indices=[["session1",1],["session2",1]],
                condition={"age":[5,20]},
                condition_session='session1',
                num_cases=1,
                precision='exact',
            ),
        }
        self.api.edit_cases(**local_var_params)
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
        if 'case_edit_request' in local_var_params:
            body_params = local_var_params['case_edit_request']
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
            200: "CaseCountResponse",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/cases/edit',
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

    def test_edit_cases_with_unexpected_params(self, mock_call_api, *args):
        """Test case for edit_cases with bad parameters"""
        params = dict(
            trainee_id=None, 
            case_edit_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.edit_cases,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_cases(self, mock_call_api, *args):
        """Test case for get_cases

        Get case data from a trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'cases_request': models.CasesRequest(
                features=["height","weight","age"],
                session='session1',
                indicate_imputed=True,
                case_indices=[["session1",1],["session2",1]],
                condition={"species":"frog","weight":[12,32]},
                num_cases=1,
                precision='exact',
            ),
        }
        self.api.get_cases(**local_var_params)
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
        if 'cases_request' in local_var_params:
            body_params = local_var_params['cases_request']
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
            200: "Cases",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/cases',
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

    def test_get_cases_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_cases with bad parameters"""
        params = dict(
            trainee_id=None, 
            
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_cases,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_num_training_cases(self, mock_call_api, *args):
        """Test case for get_num_training_cases

        Get the number of cases for a trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
        }
        self.api.get_num_training_cases(**local_var_params)
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
            200: "CaseCountResponse",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/cases/count',
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

    def test_get_num_training_cases_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_num_training_cases with bad parameters"""
        params = dict(
            trainee_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_num_training_cases,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_remove_cases(self, mock_call_api, *args):
        """Test case for remove_cases

        Remove one or more cases from a trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'case_remove_request': models.CaseRemoveRequest(
                num_cases=1,
                condition={"species":"frog","weight":[12,32]},
                condition_session='session1',
                distribute_weight_feature='age',
                precision='exact',
                preserve_session_data=True,
            ),
        }
        self.api.remove_cases(**local_var_params)
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
        if 'case_remove_request' in local_var_params:
            body_params = local_var_params['case_remove_request']
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
            200: "CaseCountResponse",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/cases/remove',
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

    def test_remove_cases_with_unexpected_params(self, mock_call_api, *args):
        """Test case for remove_cases with bad parameters"""
        params = dict(
            trainee_id=None, 
            case_remove_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.remove_cases,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()


if __name__ == '__main__':
    unittest.main()
