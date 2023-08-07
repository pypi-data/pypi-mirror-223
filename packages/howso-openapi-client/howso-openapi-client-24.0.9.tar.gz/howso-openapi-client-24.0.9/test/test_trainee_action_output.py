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
from howso.openapi.models.trainee_action_output import TraineeActionOutput  # noqa: E501
from howso.openapi.configuration import Configuration


class TestTraineeActionOutput(unittest.TestCase):
    """TraineeActionOutput unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test TraineeActionOutput
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.trainee_action_output.TraineeActionOutput()  # noqa: E501
        if include_optional :
            return TraineeActionOutput(
                action_id = '7271bc67-c563-45cd-9258-7e4c3958c170',
                status = 'complete',
                operation_type = 'react',
                output = howso.openapi.models.trainee.Trainee(
                    name = 'My Trainee', 
                    features = {"speed":{"type":"continuous"},"distance":{"type":"continuous"},"throttle":{"type":"continuous","bounds":{"min":1,"max":5}},"brake":{"type":"nominal"}}, 
                    default_context_features = ["speed","distance"], 
                    default_action_features = ["throttle","brake"], 
                    persistence = 'allow', 
                    project_id = '575fe6e1-d49e-4a74-9430-c645d354451a', 
                    id = '671ae520-4797-4b00-ba61-fb47bfadf0a3', 
                    metadata = {"requested_by":"Bob","department":"Accounting"}, ),
                local_vars_configuration=local_vars_configuration
            )
        else :
            return TraineeActionOutput(
                status = 'complete',
                operation_type = 'react',
                local_vars_configuration=local_vars_configuration
            )

    def testTraineeActionOutput(self):
        """Test TraineeActionOutput"""
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
