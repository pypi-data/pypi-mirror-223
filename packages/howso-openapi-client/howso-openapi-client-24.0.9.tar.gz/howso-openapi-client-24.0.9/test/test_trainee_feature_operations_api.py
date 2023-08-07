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
from howso.openapi.api.trainee_feature_operations_api import TraineeFeatureOperationsApi  # noqa: E501
from howso.openapi.exceptions import ApiTypeError


def get_config():
    conf = Configuration()
    conf.client_side_validation = False
    return conf


@mock.patch('howso.openapi.configuration.Configuration.get_default_copy', side_effect=get_config)  # noqa: E501
@mock.patch('howso.openapi.api.trainee_feature_operations_api.ApiClient.call_api', return_value='Mocked Return')  # noqa: E501
class TestTraineeFeatureOperationsApi(unittest.TestCase):
    """TraineeFeatureOperationsApi unit test stubs"""

    def setUp(self):
        self.api = howso.openapi.api.trainee_feature_operations_api.TraineeFeatureOperationsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_trainee_feature_operations_api_init(self, *args):
        """Test case for TraineeFeatureOperationsApi init"""
        api_client = ApiClient()
        api = howso.openapi.api.trainee_feature_operations_api.TraineeFeatureOperationsApi(api_client)  # noqa: E501
        assert api.api_client == api_client
        assert self.api.api_client != api.api_client

    def test_add_feature(self, mock_call_api, *args):
        """Test case for add_feature

        Add a feature to a trainee.  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'feature_add_request': models.FeatureAddRequest(
            ),
        }
        self.api.add_feature(**local_var_params)
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
        if 'feature_add_request' in local_var_params:
            body_params = local_var_params['feature_add_request']
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
            '/trainee/{trainee_id}/feature/add',
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

    def test_add_feature_with_unexpected_params(self, mock_call_api, *args):
        """Test case for add_feature with bad parameters"""
        params = dict(
            trainee_id=None, 
            feature_add_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.add_feature,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_extreme_cases(self, mock_call_api, *args):
        """Test case for get_extreme_cases

        Get extreme top or bottom cases for specified feature(s) from a trainee  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'extreme_cases_request': models.ExtremeCasesRequest(
                num=3,
                sort_feature='weight',
                features=["height","weight"],
            ),
        }
        self.api.get_extreme_cases(**local_var_params)
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
        if 'extreme_cases_request' in local_var_params:
            body_params = local_var_params['extreme_cases_request']
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
            '/trainee/{trainee_id}/cases/extreme',
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

    def test_get_extreme_cases_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_extreme_cases with bad parameters"""
        params = dict(
            trainee_id=None, 
            extreme_cases_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_extreme_cases,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_feature_attributes(self, mock_call_api, *args):
        """Test case for get_feature_attributes

        Get trainee feature attributes  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
        }
        self.api.get_feature_attributes(**local_var_params)
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
            200: "dict[str, FeatureAttributes]",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/feature/attributes',
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

    def test_get_feature_attributes_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_feature_attributes with bad parameters"""
        params = dict(
            trainee_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_feature_attributes,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_feature_contributions(self, mock_call_api, *args):
        """Test case for get_feature_contributions

        Get contributions of features  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'feature_contributions_request': models.FeatureContributionsRequest(
                action_feature='age',
                robust=True,
                weight_feature='height',
            ),
        }
        self.api.get_feature_contributions(**local_var_params)
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
        if 'feature_contributions_request' in local_var_params:
            body_params = local_var_params['feature_contributions_request']
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
            '/trainee/{trainee_id}/feature/contributions',
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

    def test_get_feature_contributions_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_feature_contributions with bad parameters"""
        params = dict(
            trainee_id=None, 
            feature_contributions_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_feature_contributions,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_feature_conviction(self, mock_call_api, *args):
        """Test case for get_feature_conviction

        Retrieve conviction for features in the model.  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'feature_conviction_request': models.FeatureConvictionRequest(
                features=["height","weight","age"],
                action_features=["age"],
                familiarity_conviction_addition=True,
                familiarity_conviction_removal=True,
                use_case_weights=True,
                weight_feature='height',
            ),
        }
        self.api.get_feature_conviction(**local_var_params)
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
        if 'feature_conviction_request' in local_var_params:
            body_params = local_var_params['feature_conviction_request']
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
            200: "FeatureConviction",
            202: "AsyncActionAccepted",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/feature/conviction',
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

    def test_get_feature_conviction_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_feature_conviction with bad parameters"""
        params = dict(
            trainee_id=None, 
            feature_conviction_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_feature_conviction,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_feature_residuals(self, mock_call_api, *args):
        """Test case for get_feature_residuals

        Get residuals of features  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'feature_residuals_request': models.FeatureResidualsRequest(
                action_feature='age',
                robust=True,
                robust_hyperparameters=True,
                weight_feature='height',
            ),
        }
        self.api.get_feature_residuals(**local_var_params)
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
        if 'feature_residuals_request' in local_var_params:
            body_params = local_var_params['feature_residuals_request']
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
            '/trainee/{trainee_id}/feature/residuals',
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

    def test_get_feature_residuals_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_feature_residuals with bad parameters"""
        params = dict(
            trainee_id=None, 
            feature_residuals_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_feature_residuals,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_marginal_stats(self, mock_call_api, *args):
        """Test case for get_marginal_stats

        Get marginal stats for features  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'feature_marginal_stats_request': models.FeatureMarginalStatsRequest(
                weight_feature='height',
            ),
        }
        self.api.get_marginal_stats(**local_var_params)
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
        if 'feature_marginal_stats_request' in local_var_params:
            body_params = local_var_params['feature_marginal_stats_request']
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
            200: "FeatureMarginalStats",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/feature/stats/marginal',
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

    def test_get_marginal_stats_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_marginal_stats with bad parameters"""
        params = dict(
            trainee_id=None, 
            feature_marginal_stats_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_marginal_stats,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_prediction_stats(self, mock_call_api, *args):
        """Test case for get_prediction_stats

        Get prediction stats for features  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'feature_prediction_stats_request': models.FeaturePredictionStatsRequest(
                action_feature='age',
                robust=True,
                robust_hyperparameters=True,
                stats=["mae","recall","precision"],
                weight_feature='height',
                condition={"age":[5,20]},
                precision='exact',
                num_cases=1,
                num_robust_influence_samples_per_case=1000,
            ),
        }
        self.api.get_prediction_stats(**local_var_params)
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
        if 'feature_prediction_stats_request' in local_var_params:
            body_params = local_var_params['feature_prediction_stats_request']
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
            200: "FeaturePredictionStats",
            202: "AsyncActionAccepted",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/feature/stats/prediction',
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

    def test_get_prediction_stats_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_prediction_stats with bad parameters"""
        params = dict(
            trainee_id=None, 
            feature_prediction_stats_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_prediction_stats,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_get_substitution_map(self, mock_call_api, *args):
        """Test case for get_substitution_map

        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
        }
        self.api.get_substitution_map(**local_var_params)
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
            200: "dict[str, object]",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/substitution-map',
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

    def test_get_substitution_map_with_unexpected_params(self, mock_call_api, *args):
        """Test case for get_substitution_map with bad parameters"""
        params = dict(
            trainee_id=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.get_substitution_map,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_remove_feature(self, mock_call_api, *args):
        """Test case for remove_feature

        Remove a feature from a trainee.  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'feature_remove_request': models.FeatureRemoveRequest(
                feature='year',
                condition={"year":"16","end_of_month_revenue":["0","100000"]},
                condition_session='session1',
            ),
        }
        self.api.remove_feature(**local_var_params)
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
        if 'feature_remove_request' in local_var_params:
            body_params = local_var_params['feature_remove_request']
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
            '/trainee/{trainee_id}/feature/remove',
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

    def test_remove_feature_with_unexpected_params(self, mock_call_api, *args):
        """Test case for remove_feature with bad parameters"""
        params = dict(
            trainee_id=None, 
            feature_remove_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.remove_feature,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_set_feature_attributes(self, mock_call_api, *args):
        """Test case for set_feature_attributes

        Set all trainee feature attributes  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'request_body': {
                'inner': howso.openapi.models.feature_attributes.FeatureAttributes(
                    type = 'continuous', 
                    auto_derive_on_train = {"derive_type":"progress","series_id_features":["x","y"]}, 
                    bounds = howso.openapi.models.feature_bounds.FeatureBounds(
                        min = 0, 
                        max = 10, 
                        allowed = ["car","plane"], 
                        allow_null = True, ), 
                    cycle_length = 360, 
                    data_type = 'string', 
                    date_time_format = '%Y-%m-%d-%H.%M.%S', 
                    decimal_places = 56, 
                    dependent_features = ["width","length"], 
                    derived_feature_code = '(- #y 0 #x 1)', 
                    dropna = True, 
                    id_feature = True, 
                    locale = 'en-US', 
                    non_sensitive = True, 
                    null_is_dependent = True, 
                    observational_error = 1.337, 
                    original_type = {"data_type":"string","length":128}, 
                    original_format = {"python":{"date_time_format":"%Y-%m-%d-%H.%M.%S.%f"}}, 
                    post_process = '(set_digits #sepal_length 0 2 (list 1) -1 -1 (true))', 
                    significant_digits = 2, 
                    subtype = 'int-id', 
                    time_delta_format = 'seconds', 
                    time_series = howso.openapi.models.feature_time_series.FeatureTimeSeries(
                        type = 'rate', 
                        order = 0, 
                        derived_orders = 1.337, 
                        delta_min = [2.0], 
                        delta_max = [5.5], 
                        lags = [1], 
                        num_lags = 1, 
                        rate_min = [0.2], 
                        rate_max = [0.55], 
                        series_has_terminators = True, 
                        stop_on_terminator = True, 
                        time_feature = True, ), 
                    unique = True, ),
            },
        }
        self.api.set_feature_attributes(**local_var_params)
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
        if 'request_body' in local_var_params:
            body_params = local_var_params['request_body']
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
            200: "dict[str, FeatureAttributes]",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/feature/attributes',
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

    def test_set_feature_attributes_with_unexpected_params(self, mock_call_api, *args):
        """Test case for set_feature_attributes with bad parameters"""
        params = dict(
            trainee_id=None, 
            request_body=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.set_feature_attributes,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_set_substitution_map(self, mock_call_api, *args):
        """Test case for set_substitution_map

        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'request_body': {
                'inner': None,
            },
        }
        self.api.set_substitution_map(**local_var_params)
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
        if 'request_body' in local_var_params:
            body_params = local_var_params['request_body']
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
            '/trainee/{trainee_id}/substitution-map',
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

    def test_set_substitution_map_with_unexpected_params(self, mock_call_api, *args):
        """Test case for set_substitution_map with bad parameters"""
        params = dict(
            trainee_id=None, 
            request_body=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.set_substitution_map,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()


if __name__ == '__main__':
    unittest.main()
