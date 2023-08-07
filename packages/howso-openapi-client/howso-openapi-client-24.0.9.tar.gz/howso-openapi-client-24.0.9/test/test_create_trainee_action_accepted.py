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
from howso.openapi.models.create_trainee_action_accepted import CreateTraineeActionAccepted  # noqa: E501
from howso.openapi.configuration import Configuration


class TestCreateTraineeActionAccepted(unittest.TestCase):
    """CreateTraineeActionAccepted unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test CreateTraineeActionAccepted
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.create_trainee_action_accepted.CreateTraineeActionAccepted()  # noqa: E501
        if include_optional :
            return CreateTraineeActionAccepted(
                action_id = '',
                operation_type = 'react',
                tracking = {"url":"https://api.example.com/api/v2/action/cecc4d1e-0ba2-4879-97d9-cda0f455037b"},
                estimated_completion = '2021-09-08T18:37:04Z',
                rejected_after = '2021-09-09T18:37:04Z',
                trainee_id = '',
                local_vars_configuration=local_vars_configuration
            )
        else :
            return CreateTraineeActionAccepted(
                local_vars_configuration=local_vars_configuration
            )

    def testCreateTraineeActionAccepted(self):
        """Test CreateTraineeActionAccepted"""
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
