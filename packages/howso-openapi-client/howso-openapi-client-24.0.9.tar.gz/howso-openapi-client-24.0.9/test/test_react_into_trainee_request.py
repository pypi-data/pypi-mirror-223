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
from howso.openapi.models.react_into_trainee_request import ReactIntoTraineeRequest  # noqa: E501
from howso.openapi.configuration import Configuration


class TestReactIntoTraineeRequest(unittest.TestCase):
    """ReactIntoTraineeRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test ReactIntoTraineeRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.react_into_trainee_request.ReactIntoTraineeRequest()  # noqa: E501
        if include_optional :
            return ReactIntoTraineeRequest(
                contributions = True,
                contributions_robust = True,
                residuals = True,
                residuals_robust = True,
                mda = True,
                mda_permutation = True,
                mda_robust = True,
                mda_robust_permutation = True,
                action_feature = 'class',
                context_features = ["width","height"],
                hyperparameter_param_path = ["key","subkey"],
                num_robust_influence_samples = 1000,
                num_robust_influence_samples_per_case = 1000,
                num_robust_residual_samples = 2000,
                num_samples = 2000,
                sample_model_fraction = 0.15,
                sub_model_size = 10000,
                use_case_weights = True,
                weight_feature = 'height',
                local_vars_configuration=local_vars_configuration
            )
        else :
            return ReactIntoTraineeRequest(
                local_vars_configuration=local_vars_configuration
            )

    def testReactIntoTraineeRequest(self):
        """Test ReactIntoTraineeRequest"""
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
