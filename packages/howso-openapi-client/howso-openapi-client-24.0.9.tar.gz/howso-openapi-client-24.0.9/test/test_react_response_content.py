# coding: utf-8

"""
Howso API

OpenAPI implementation for interacting with the Howso API. 
"""

from __future__ import absolute_import

import unittest
import datetime
import pprint

import howso.openapi
from howso.openapi.models.react_response_content import ReactResponseContent  # noqa: E501
from howso.openapi.configuration import Configuration


class TestReactResponseContent(unittest.TestCase):
    """ReactResponseContent unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test ReactResponseContent
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.react_response_content.ReactResponseContent()  # noqa: E501
        if include_optional :
            return ReactResponseContent(
                action_features = ["class"],
                action_values = [["virginica"],["versicolor"]],
                context_values = [[5.2,4.1,1.5,0.1],[6.3,2.9,5.6,1.8]],
                boundary_cases = [[{".session":"training_set",".session_training_index":81,".influence_weight":0.117768,"class":"versicolor","petal_length":6.7,"petal_width":3,"sepal_length":5,"sepal_width":1.7}]],
                categorical_action_probabilities = [{"class":{"versicolor":0.47110612119158973,"virginica":0.5288938788084102}}],
                feature_residuals = [{"sepal_length":{"mean_absolute_error":0.5432,"mean_absolute_error_high":0.3606,"mean_absolute_error_low":0.4614},"sepal_width":{"mean_absolute_error":0.1648,"mean_absolute_error_high":0.16106,"mean_absolute_error_low":0.1685},"class":{"mean_absolute_error":0.1,"nominal_prediction_rates":[{"versicolor":{"correct_rate":0.9,"false_negative_rate":0.066667,"false_positive_rate":0.033334}}]}}],
                outlying_feature_values = [{"petal_width":{"input_case_value":0.9,"local_min":1.1},"petal_length":{"input_case_value":5.3,"local_max":5.2}}],
                influential_cases = [[{".session":"training_set",".session_training_index":119,".influence_weight":0.117768,".raw_influence_weight":6.649027E-7,"familiarity_conviction":0.13356,"class":"versicolor","petal_length":6.7,"petal_width":3,"sepal_length":5,"sepal_width":1.7}]],
                most_similar_cases = [[{".session":"training_set",".session_training_index":119,"class":"versicolor","petal_length":6.4,"petal_width":3.2,"sepal_length":5.3,"sepal_width":2.3}]],
                observational_errors = [{"class":0.5,"petal_length":1.08,"petal_width":0.57,"sepal_length":1.79,"sepal_width":1.29}],
                feature_mda = [{"petal_length":0.61,"petal_width":0.44,"sepal_length":-0.42,"sepal_width":-0.47}],
                feature_mda_ex_post = [{"petal_length":0.61,"petal_width":0.44,"sepal_length":-0.42,"sepal_width":-0.47}],
                feature_contributions = [{"petal_length":0.61,"petal_width":0.44,"sepal_length":-0.42,"sepal_width":-0.47}],
                case_mda = [[{"mda":0.55,".session":"fd2baec1-56db-468d-88e6-efc6c2b97428",".session_training_index":10}]],
                case_contributions = [[{"action_delta":0.73,".session":"fd2baec1-56db-468d-88e6-efc6c2b97428",".session_training_index":11}]],
                case_feature_residuals = [{"class":0.0,"petal_length":4.93,"petal_width":3.037}],
                local_case_feature_residual_convictions = [{"class":0.0,"petal_length":4.93,"petal_width":3.037}],
                global_case_feature_residual_convictions = [{"class":0.0,"petal_length":4.93,"petal_width":3.037}],
                hypothetical_values = [{"sepal_length":0.04,"sepal_width":2.08}],
                distance_ratio = [1.03],
                distance_ratio_parts = [{"local_distance_contribution":0.5,"nearest_distance":1.0}],
                distance_contribution = [1.2],
                prediction_similarity_conviction = [0.2],
                prediction_residual_conviction = [0.45],
                most_similar_case_indices = [[{".session":"training_set",".session_training_index":119,".distance":0.2}]],
                local_vars_configuration=local_vars_configuration
            )
        else :
            return ReactResponseContent(
                local_vars_configuration=local_vars_configuration
            )

    def testReactResponseContent(self):
        """Test ReactResponseContent"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

        test_config = Configuration.get_default_copy()
        inst_with_configuration = self.make_instance(
            include_optional=False,
            local_vars_configuration=test_config
        )
        assert inst_with_configuration.local_vars_configuration == test_config

        assert isinstance(inst_req_only.to_dict(), dict)
        assert isinstance(inst_req_only.to_str(), str)
        assert inst_req_and_optional.__eq__(inst_req_and_optional) is True
        assert inst_req_and_optional.__eq__(None) is False
        assert inst_req_and_optional.__ne__(inst_req_and_optional) is False
        assert inst_req_and_optional.__ne__(None) is True
        assert repr(inst_req_and_optional) == inst_req_and_optional.to_str()
        assert inst_req_only.to_str() == pprint.pformat(inst_req_only.to_dict())


if __name__ == '__main__':
    unittest.main()
