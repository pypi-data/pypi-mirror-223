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
from howso.openapi.api.trainee_operations_api import TraineeOperationsApi  # noqa: E501
from howso.openapi.exceptions import ApiTypeError


def get_config():
    conf = Configuration()
    conf.client_side_validation = False
    return conf


@mock.patch('howso.openapi.configuration.Configuration.get_default_copy', side_effect=get_config)  # noqa: E501
@mock.patch('howso.openapi.api.trainee_operations_api.ApiClient.call_api', return_value='Mocked Return')  # noqa: E501
class TestTraineeOperationsApi(unittest.TestCase):
    """TraineeOperationsApi unit test stubs"""

    def setUp(self):
        self.api = howso.openapi.api.trainee_operations_api.TraineeOperationsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_trainee_operations_api_init(self, *args):
        """Test case for TraineeOperationsApi init"""
        api_client = ApiClient()
        api = howso.openapi.api.trainee_operations_api.TraineeOperationsApi(api_client)  # noqa: E501
        assert api.api_client == api_client
        assert self.api.api_client != api.api_client

    def test_analyze(self, mock_call_api, *args):
        """Test case for analyze

        Analyze the trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'analyze_request': models.AnalyzeRequest(
                action_features=["throttle_pos","gear_selector"],
                context_features=["speed","engine_temp"],
                k_folds=6,
                num_samples=56,
                dt_values=[2.3,4.5],
                k_values=[1,2,3],
                p_values=[1,2,3],
                bypass_hyperparameter_analysis=True,
                bypass_calculate_feature_residuals=True,
                bypass_calculate_feature_weights=True,
                targeted_model='targetless',
                analyze_level=56,
                num_analysis_samples=56,
                analysis_sub_model_size=56,
                use_deviations=True,
                inverse_residuals_as_weights=True,
                use_case_weights=True,
                weight_feature='',
                experimental_options={ },
            ),
        }
        self.api.analyze(**local_var_params)
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
        if 'analyze_request' in local_var_params:
            body_params = local_var_params['analyze_request']
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
            204: None,
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/analyze',
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

    def test_analyze_with_unexpected_params(self, mock_call_api, *args):
        """Test case for analyze with bad parameters"""
        params = dict(
            trainee_id=None, 
            analyze_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.analyze,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_append_to_series_store(self, mock_call_api, *args):
        """Test case for append_to_series_store

        Append contexts to series store  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'append_to_series_store_request': models.AppendToSeriesStoreRequest(
                series='',
                contexts=[["green",1,"circle"],["yellow",4.1,"square"]],
                context_features=["speed","distance"],
            ),
        }
        self.api.append_to_series_store(**local_var_params)
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
        if 'append_to_series_store_request' in local_var_params:
            body_params = local_var_params['append_to_series_store_request']
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
            '/trainee/{trainee_id}/series/append',
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

    def test_append_to_series_store_with_unexpected_params(self, mock_call_api, *args):
        """Test case for append_to_series_store with bad parameters"""
        params = dict(
            trainee_id=None, 
            append_to_series_store_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.append_to_series_store,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_auto_analyze(self, mock_call_api, *args):
        """Test case for auto_analyze

        Automatically analyze the trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
        }
        self.api.auto_analyze(**local_var_params)
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
            202: "AsyncActionAccepted",
            204: None,
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/analyze/auto',
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

    def test_auto_analyze_with_unexpected_params(self, mock_call_api, *args):
        """Test case for auto_analyze with bad parameters"""
        params = dict(
            trainee_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.auto_analyze,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_evaluate(self, mock_call_api, *args):
        """Test case for evaluate

        Evaluate custom code on cases within a trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'evaluate_request': models.EvaluateRequest(
                features_to_code_map={"age":"(+ 2 #age 0)","status":"(concat \"TEST\" #status 0)"},
                aggregation_code='(apply "+" #age 0)',
            ),
        }
        self.api.evaluate(**local_var_params)
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
        if 'evaluate_request' in local_var_params:
            body_params = local_var_params['evaluate_request']
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
            200: "EvaluateResponse",
            202: "AsyncActionAccepted",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/evaluate',
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

    def test_evaluate_with_unexpected_params(self, mock_call_api, *args):
        """Test case for evaluate with bad parameters"""
        params = dict(
            trainee_id=None, 
            evaluate_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.evaluate,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_feature_mda(self, mock_call_api, *args):
        """Test case for get_feature_mda

        Get the feature mean decrease in accuracy.  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'feature_mda_request': models.FeatureMdaRequest(
                action_feature='class',
                permutation=True,
                robust=True,
                weight_feature='height',
            ),
        }
        self.api.get_feature_mda(**local_var_params)
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
        if 'feature_mda_request' in local_var_params:
            body_params = local_var_params['feature_mda_request']
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
            200: "dict[str, float]",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/feature/mda',
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

    def test_get_feature_mda_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_feature_mda with bad parameters"""
        params = dict(
            trainee_id=None, 
            feature_mda_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_feature_mda,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_workflow_attributes(self, mock_call_api, *args):
        """Test case for get_workflow_attributes

        Get trainee workflow attributes  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
        }
        self.api.get_workflow_attributes(**local_var_params)
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
            200: "TraineeWorkflowAttributes",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/attributes',
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

    def test_get_workflow_attributes_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_workflow_attributes with bad parameters"""
        params = dict(
            trainee_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_workflow_attributes,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_impute(self, mock_call_api, *args):
        """Test case for impute

        Impute  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'impute_request': models.ImputeRequest(
                batch_size=1,
                features=["sepal_width","sepal_length"],
                features_to_impute=["sepal_width"],
            ),
        }
        self.api.impute(**local_var_params)
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
        if 'impute_request' in local_var_params:
            body_params = local_var_params['impute_request']
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
            204: None,
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/impute',
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

    def test_impute_with_unexpected_params(self, mock_call_api, *args):
        """Test case for impute with bad parameters"""
        params = dict(
            trainee_id=None, 
            
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.impute,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_react(self, mock_call_api, *args):
        """Test case for react

        React to one or more contexts  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'react_request': models.ReactRequest(
            ),
        }
        self.api.react(**local_var_params)
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
        if 'react_request' in local_var_params:
            body_params = local_var_params['react_request']
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
            200: "ReactResponse",
            202: "AsyncActionAccepted",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/react',
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

    def test_react_with_unexpected_params(self, mock_call_api, *args):
        """Test case for react with bad parameters"""
        params = dict(
            trainee_id=None, 
            react_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.react,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_react_group(self, mock_call_api, *args):
        """Test case for react_group

        React to a grouping of cases.  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'react_group_request': models.ReactGroupRequest(
                new_cases=[[[1,2,"kitten"],[3,4,"mitten"]]],
                trainees_to_compare=["e9bad190-1078-49b0-bcba-469b51a1b974"],
                features=["height","weight","age"],
                familiarity_conviction_addition=True,
                familiarity_conviction_removal=True,
                kl_divergence_addition=True,
                kl_divergence_removal=True,
                p_value_of_addition=True,
                p_value_of_removal=True,
                distance_contributions=True,
                use_case_weights=True,
                weight_feature='height',
            ),
        }
        self.api.react_group(**local_var_params)
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
        if 'react_group_request' in local_var_params:
            body_params = local_var_params['react_group_request']
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
            200: "ReactGroupResponse",
            202: "AsyncActionAccepted",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/react/group',
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

    def test_react_group_with_unexpected_params(self, mock_call_api, *args):
        """Test case for react_group with bad parameters"""
        params = dict(
            trainee_id=None, 
            react_group_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.react_group,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_react_into_features(self, mock_call_api, *args):
        """Test case for react_into_features

        React into features  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'react_into_features_request': models.ReactIntoFeaturesRequest(
                features=["height","weight","age"],
                familiarity_conviction_addition='',
                familiarity_conviction_removal='',
                p_value_of_addition='',
                p_value_of_removal='',
                distance_contribution='',
                use_case_weights=True,
                weight_feature='height',
            ),
        }
        self.api.react_into_features(**local_var_params)
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
        if 'react_into_features_request' in local_var_params:
            body_params = local_var_params['react_into_features_request']
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
            200: "ReactIntoFeaturesResponse",
            202: "AsyncActionAccepted",
            204: None,
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/react/into-features',
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

    def test_react_into_features_with_unexpected_params(self, mock_call_api, *args):
        """Test case for react_into_features with bad parameters"""
        params = dict(
            trainee_id=None, 
            react_into_features_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.react_into_features,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_react_into_trainee(self, mock_call_api, *args):
        """Test case for react_into_trainee

        React into trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'react_into_trainee_request': models.ReactIntoTraineeRequest(
                contributions=True,
                contributions_robust=True,
                residuals=True,
                residuals_robust=True,
                mda=True,
                mda_permutation=True,
                mda_robust=True,
                mda_robust_permutation=True,
                action_feature='class',
                context_features=["width","height"],
                hyperparameter_param_path=["key","subkey"],
                num_robust_influence_samples=1000,
                num_robust_influence_samples_per_case=1000,
                num_robust_residual_samples=2000,
                num_samples=2000,
                sample_model_fraction=0.15,
                sub_model_size=10000,
                use_case_weights=True,
                weight_feature='height',
            ),
        }
        self.api.react_into_trainee(**local_var_params)
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
        if 'react_into_trainee_request' in local_var_params:
            body_params = local_var_params['react_into_trainee_request']
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
            200: "ReactIntoTraineeResponse",
            202: "AsyncActionAccepted",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/react/into-trainee',
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

    def test_react_into_trainee_with_unexpected_params(self, mock_call_api, *args):
        """Test case for react_into_trainee with bad parameters"""
        params = dict(
            trainee_id=None, 
            react_into_trainee_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.react_into_trainee,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_react_series(self, mock_call_api, *args):
        """Test case for react_series

        React to one or more contexts in series  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'react_series_request': models.ReactSeriesRequest(
            ),
        }
        self.api.react_series(**local_var_params)
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
        if 'react_series_request' in local_var_params:
            body_params = local_var_params['react_series_request']
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
            200: "ReactSeriesResponse",
            202: "AsyncActionAccepted",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/react/series',
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

    def test_react_series_with_unexpected_params(self, mock_call_api, *args):
        """Test case for react_series with bad parameters"""
        params = dict(
            trainee_id=None, 
            react_series_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.react_series,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_remove_series_store(self, mock_call_api, *args):
        """Test case for remove_series_store

        Clear stored series from trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'remove_series_store_request': models.RemoveSeriesStoreRequest(
                series='',
            ),
        }
        self.api.remove_series_store(**local_var_params)
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
        if 'remove_series_store_request' in local_var_params:
            body_params = local_var_params['remove_series_store_request']
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
            '/trainee/{trainee_id}/series/remove',
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

    def test_remove_series_store_with_unexpected_params(self, mock_call_api, *args):
        """Test case for remove_series_store with bad parameters"""
        params = dict(
            trainee_id=None, 
            remove_series_store_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.remove_series_store,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_set_auto_analyze_params(self, mock_call_api, *args):
        """Test case for set_auto_analyze_params

        Set trainee parameters for auto analysis  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'set_auto_analyze_params_request': models.SetAutoAnalyzeParamsRequest(
            ),
        }
        self.api.set_auto_analyze_params(**local_var_params)
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
        if 'set_auto_analyze_params_request' in local_var_params:
            body_params = local_var_params['set_auto_analyze_params_request']
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
            '/trainee/{trainee_id}/analyze/auto/params',
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

    def test_set_auto_analyze_params_with_unexpected_params(self, mock_call_api, *args):
        """Test case for set_auto_analyze_params with bad parameters"""
        params = dict(
            trainee_id=None, 
            set_auto_analyze_params_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.set_auto_analyze_params,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_set_workflow_attributes(self, mock_call_api, *args):
        """Test case for set_workflow_attributes

        Set the trainee workflow attributes  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'trainee_workflow_attributes': models.TraineeWorkflowAttributes(
                hyperparameter_map={".targetless":{"robust":{"k":5,"p":2,"dt":-1}}},
                auto_analyze_enabled=True,
                auto_analyze_limit_size=56,
                analyze_growth_factor=1.337,
                analyze_threshold=56,
            ),
        }
        self.api.set_workflow_attributes(**local_var_params)
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
        if 'trainee_workflow_attributes' in local_var_params:
            body_params = local_var_params['trainee_workflow_attributes']
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
            '/trainee/{trainee_id}/attributes',
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

    def test_set_workflow_attributes_with_unexpected_params(self, mock_call_api, *args):
        """Test case for set_workflow_attributes with bad parameters"""
        params = dict(
            trainee_id=None, 
            trainee_workflow_attributes=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.set_workflow_attributes,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_train(self, mock_call_api, *args):
        """Test case for train

        Train a model  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'train_request': models.TrainRequest(
                cases=[["green",1,"circle"],["yellow",4.1,"square"]],
                features=["height","weight"],
                derived_features=["weight","height"],
                input_is_substituted=True,
                ablatement_params={"species":["exact"],"sepal_length":["tolerance",0.1,0.25]},
                accumulate_weight_feature='height',
                series='',
                train_weights_only=True,
                run_async=False,
            ),
        }
        self.api.train(**local_var_params)
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
        if 'train_request' in local_var_params:
            body_params = local_var_params['train_request']
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
            200: "TrainResponse",
            202: "AsyncActionAccepted",
            401: "Error",
            403: "Error",
            404: None,
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/train',
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

    def test_train_with_unexpected_params(self, mock_call_api, *args):
        """Test case for train with bad parameters"""
        params = dict(
            trainee_id=None, 
            
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.train,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()


if __name__ == '__main__':
    unittest.main()
