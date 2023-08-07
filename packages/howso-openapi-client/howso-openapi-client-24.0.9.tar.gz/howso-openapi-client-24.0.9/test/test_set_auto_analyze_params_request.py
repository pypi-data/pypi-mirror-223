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
from howso.openapi.models.set_auto_analyze_params_request import SetAutoAnalyzeParamsRequest  # noqa: E501
from howso.openapi.configuration import Configuration


class TestSetAutoAnalyzeParamsRequest(unittest.TestCase):
    """SetAutoAnalyzeParamsRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test SetAutoAnalyzeParamsRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.set_auto_analyze_params_request.SetAutoAnalyzeParamsRequest()  # noqa: E501
        if include_optional :
            return SetAutoAnalyzeParamsRequest(
                action_features = ["throttle_pos","gear_selector"],
                context_features = ["speed","engine_temp"],
                k_folds = 6,
                num_samples = 56,
                dt_values = [2.3,4.5],
                k_values = [1,2,3],
                p_values = [1,2,3],
                bypass_hyperparameter_analysis = True,
                bypass_calculate_feature_residuals = True,
                bypass_calculate_feature_weights = True,
                targeted_model = 'targetless',
                analyze_level = 56,
                num_analysis_samples = 56,
                analysis_sub_model_size = 56,
                use_deviations = True,
                inverse_residuals_as_weights = True,
                use_case_weights = True,
                weight_feature = '',
                experimental_options = { },
                auto_analyze_enabled = True,
                auto_analyze_limit_size = 100000,
                analyze_growth_factor = 3,
                analyze_threshold = 100,
                local_vars_configuration=local_vars_configuration
            )
        else :
            return SetAutoAnalyzeParamsRequest(
                local_vars_configuration=local_vars_configuration
            )

    def testSetAutoAnalyzeParamsRequest(self):
        """Test SetAutoAnalyzeParamsRequest"""
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
