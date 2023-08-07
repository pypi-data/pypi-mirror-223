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
from howso.openapi.models.session import Session  # noqa: E501
from howso.openapi.configuration import Configuration


class TestSession(unittest.TestCase):
    """Session unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test Session
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.session.Session()  # noqa: E501
        if include_optional :
            return Session(
                id = '8494e0d2-7d9a-4948-98b3-fa98418fdf1c',
                name = 'session_1',
                user = howso.openapi.models.account_identity.AccountIdentity(
                    uuid = '92295e99-a7c6-4d03-9b4d-abbe49053880', 
                    username = 'johndoe', 
                    full_name = 'John Doe', ),
                metadata = { },
                created_date = '2021-07-15T20:15:21.828365Z',
                modified_date = '2021-07-15T20:15:21.828365Z',
                local_vars_configuration=local_vars_configuration
            )
        else :
            return Session(
                local_vars_configuration=local_vars_configuration
            )

    def testSession(self):
        """Test Session"""
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
