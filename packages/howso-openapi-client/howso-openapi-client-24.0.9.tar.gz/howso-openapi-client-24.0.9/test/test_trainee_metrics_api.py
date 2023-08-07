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
from howso.openapi.api.trainee_metrics_api import TraineeMetricsApi  # noqa: E501
from howso.openapi.exceptions import ApiTypeError


def get_config():
    conf = Configuration()
    conf.client_side_validation = False
    return conf


@mock.patch('howso.openapi.configuration.Configuration.get_default_copy', side_effect=get_config)  # noqa: E501
@mock.patch('howso.openapi.api.trainee_metrics_api.ApiClient.call_api', return_value='Mocked Return')  # noqa: E501
class TestTraineeMetricsApi(unittest.TestCase):
    """TraineeMetricsApi unit test stubs"""

    def setUp(self):
        self.api = howso.openapi.api.trainee_metrics_api.TraineeMetricsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_trainee_metrics_api_init(self, *args):
        """Test case for TraineeMetricsApi init"""
        api_client = ApiClient()
        api = howso.openapi.api.trainee_metrics_api.TraineeMetricsApi(api_client)  # noqa: E501
        assert api.api_client == api_client
        assert self.api.api_client != api.api_client

    def test_distances(self, mock_call_api, *args):
        """Test case for distances

        Computes distances matrix.  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'distances_request': models.DistancesRequest(
                features=["height","weight","class"],
                action_feature='class',
                case_indices=[["session1",1],["session2",1]],
                feature_values=[5],
                use_case_weights=True,
                weight_feature='weight',
                row_offset=56,
                row_count=56,
                column_offset=56,
                column_count=56,
            ),
        }
        self.api.distances(**local_var_params)
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
        if 'distances_request' in local_var_params:
            body_params = local_var_params['distances_request']
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
            200: "DistancesResponse",
            400: "Error",
            401: "Error",
            403: "Error",
            404: "Error",
        }

        mock_call_api.assert_called_with(
            '/trainee/{trainee_id}/metrics/distances',
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

    def test_distances_with_unexpected_params(self, mock_call_api, *args):
        """Test case for distances with bad parameters"""
        params = dict(
            trainee_id=None, 
            distances_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.distances,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()

    def test_pairwise_distances(self, mock_call_api, *args):
        """Test case for pairwise_distances

        Computes pairwise distances for specified from and to cases or values.  # noqa: E501
        """
        local_var_params = {
            'trainee_id': 'trainee_id_example',
            'pairwise_distances_request': models.PairwiseDistancesRequest(
                from_case_indices=[["session1",1]],
                from_values=[[4,5.8]],
                to_case_indices=[["session1",2]],
                to_values=[[2,9.8]],
                features=["height","weight","class"],
                action_feature='class',
                use_case_weights=True,
                weight_feature='weight',
            ),
        }
        self.api.pairwise_distances(**local_var_params)
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
        if 'pairwise_distances_request' in local_var_params:
            body_params = local_var_params['pairwise_distances_request']
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
            '/trainee/{trainee_id}/metrics/pairwise-distances',
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

    def test_pairwise_distances_with_unexpected_params(self, mock_call_api, *args):
        """Test case for pairwise_distances with bad parameters"""
        params = dict(
            trainee_id=None, 
            pairwise_distances_request=None, 
        )
        kw_params = dict(_test_bad_request_parameter=True)
        self.assertRaises(
            ApiTypeError,
            self.api.pairwise_distances,
            *params,
            **kw_params,
        )
        mock_call_api.assert_not_called()


if __name__ == '__main__':
    unittest.main()
