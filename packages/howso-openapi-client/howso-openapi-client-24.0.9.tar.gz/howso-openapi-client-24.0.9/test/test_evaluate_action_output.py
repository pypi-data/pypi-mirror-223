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
from howso.openapi.models.evaluate_action_output import EvaluateActionOutput  # noqa: E501
from howso.openapi.configuration import Configuration


class TestEvaluateActionOutput(unittest.TestCase):
    """EvaluateActionOutput unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test EvaluateActionOutput
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.evaluate_action_output.EvaluateActionOutput()  # noqa: E501
        if include_optional :
            return EvaluateActionOutput(
                action_id = '7271bc67-c563-45cd-9258-7e4c3958c170',
                status = 'complete',
                operation_type = 'react',
                output = howso.openapi.models.evaluate_response.EvaluateResponse(
                    aggregated = 4, 
                    evaluated = {"age":[5,7,9],"status":["TEST1","TEST2"]}, ),
                local_vars_configuration=local_vars_configuration
            )
        else :
            return EvaluateActionOutput(
                status = 'complete',
                operation_type = 'react',
                local_vars_configuration=local_vars_configuration
            )

    def testEvaluateActionOutput(self):
        """Test EvaluateActionOutput"""
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
