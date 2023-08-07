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
from howso.openapi.models.react_group_request import ReactGroupRequest  # noqa: E501
from howso.openapi.configuration import Configuration


class TestReactGroupRequest(unittest.TestCase):
    """ReactGroupRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test ReactGroupRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.react_group_request.ReactGroupRequest()  # noqa: E501
        if include_optional :
            return ReactGroupRequest(
                new_cases = [[[1,2,"kitten"],[3,4,"mitten"]]],
                trainees_to_compare = ["e9bad190-1078-49b0-bcba-469b51a1b974"],
                features = ["height","weight","age"],
                familiarity_conviction_addition = True,
                familiarity_conviction_removal = True,
                kl_divergence_addition = True,
                kl_divergence_removal = True,
                p_value_of_addition = True,
                p_value_of_removal = True,
                distance_contributions = True,
                use_case_weights = True,
                weight_feature = 'height',
                local_vars_configuration=local_vars_configuration
            )
        else :
            return ReactGroupRequest(
                local_vars_configuration=local_vars_configuration
            )

    def testReactGroupRequest(self):
        """Test ReactGroupRequest"""
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
