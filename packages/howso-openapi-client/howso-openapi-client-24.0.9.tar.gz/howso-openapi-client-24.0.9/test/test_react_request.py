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
from howso.openapi.models.react_request import ReactRequest  # noqa: E501
from howso.openapi.configuration import Configuration


class TestReactRequest(unittest.TestCase):
    """ReactRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test ReactRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.react_request.ReactRequest()  # noqa: E501
        if include_optional :
            return ReactRequest(
                contexts = [["green",1,"circle"],["yellow",4.1,"square"]],
                actions = [["virginica"],["versicolor"]],
                input_is_substituted = True,
                substitute_output = True,
                details = howso.openapi.models.react_details.ReactDetails(
                    robust_computation = True, 
                    influential_cases = True, 
                    influential_cases_familiarity_convictions = True, 
                    influential_cases_raw_weights = True, 
                    most_similar_cases = True, 
                    num_most_similar_cases = 1, 
                    num_most_similar_case_indices = 1, 
                    num_robust_influence_samples_per_case = 1, 
                    boundary_cases = True, 
                    num_boundary_cases = 1, 
                    boundary_cases_familiarity_convictions = True, 
                    feature_residuals = True, 
                    feature_mda = True, 
                    feature_mda_ex_post = True, 
                    feature_contributions = True, 
                    case_feature_residuals = True, 
                    case_mda = True, 
                    case_contributions = True, 
                    global_case_feature_residual_convictions = True, 
                    local_case_feature_residual_convictions = True, 
                    outlying_feature_values = True, 
                    categorical_action_probabilities = True, 
                    hypothetical_values = { }, 
                    distance_ratio = True, 
                    distance_contribution = True, 
                    prediction_similarity_conviction = True, 
                    prediction_residual_conviction = True, 
                    observational_errors = True, ),
                context_features = ["speed","distance","time_of_day"],
                action_features = ["gas","brake","honk"],
                derived_context_features = ["speed","distance"],
                derived_action_features = ["brake"],
                desired_conviction = 0.5,
                use_regional_model_residuals = True,
                feature_bounds_map = {"my_feature_name":{"min":1,"max":2}},
                generate_new_cases = 'attempt',
                preserve_feature_values = ["brake","honk"],
                new_case_threshold = 'min',
                case_indices = [["session1",1],["session1",2],["session2",1]],
                leave_case_out = True,
                ordered_by_specified_features = True,
                use_case_weights = True,
                weight_feature = 'gas',
                allow_nulls = True,
                num_cases_to_generate = 1,
                into_series_store = 'myseries',
                run_async = True,
                local_vars_configuration=local_vars_configuration
            )
        else :
            return ReactRequest(
                local_vars_configuration=local_vars_configuration
            )

    def testReactRequest(self):
        """Test ReactRequest"""
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
