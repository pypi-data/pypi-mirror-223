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
from howso.openapi.models.trace_response import TraceResponse  # noqa: E501
from howso.openapi.configuration import Configuration


class TestTraceResponse(unittest.TestCase):
    """TraceResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test TraceResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.trace_response.TraceResponse()  # noqa: E501
        if include_optional :
            return TraceResponse(
                presigned_url = 'https://presigned.example.com/trainees/trace/7b530d1c-769f-4fdd-a2ec-1a441275fdc2_execution.trace?AWSAccessKeyId=somepassword&Signature=fSV0Y3HRztT1jwoMZ5SBKmqCHn8%3D&Expires=1628714941',
                expires_at = '2021-08-11 20:49:01.694693',
                local_vars_configuration=local_vars_configuration
            )
        else :
            return TraceResponse(
                local_vars_configuration=local_vars_configuration
            )

    def testTraceResponse(self):
        """Test TraceResponse"""
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
