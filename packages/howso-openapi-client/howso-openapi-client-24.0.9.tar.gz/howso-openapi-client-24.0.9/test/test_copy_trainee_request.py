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
from howso.openapi.models.copy_trainee_request import CopyTraineeRequest  # noqa: E501
from howso.openapi.configuration import Configuration


class TestCopyTraineeRequest(unittest.TestCase):
    """CopyTraineeRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test CopyTraineeRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.copy_trainee_request.CopyTraineeRequest()  # noqa: E501
        if include_optional :
            return CopyTraineeRequest(
                new_trainee_name = 'Trainee1 Copy',
                project_id = '216abfb8-7c7b-47f6-9918-e69fbb2bfc13',
                library_type = 'st',
                resources = howso.openapi.models.trainee_resources.TraineeResources(
                    cpu = howso.openapi.models.cpu_limits.CPULimits(
                        minimum = 56, 
                        maximum = 56, ), 
                    memory = howso.openapi.models.memory_limits.MemoryLimits(
                        minimum = 56, 
                        maximum = 56, ), 
                    replicas = 1, ),
                local_vars_configuration=local_vars_configuration
            )
        else :
            return CopyTraineeRequest(
                local_vars_configuration=local_vars_configuration
            )

    def testCopyTraineeRequest(self):
        """Test CopyTraineeRequest"""
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
