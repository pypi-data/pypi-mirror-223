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
from howso.openapi.models.feature_remove_request import FeatureRemoveRequest  # noqa: E501
from howso.openapi.configuration import Configuration


class TestFeatureRemoveRequest(unittest.TestCase):
    """FeatureRemoveRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test FeatureRemoveRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.feature_remove_request.FeatureRemoveRequest()  # noqa: E501
        if include_optional :
            return FeatureRemoveRequest(
                feature = 'year',
                condition = {"year":"16","end_of_month_revenue":["0","100000"]},
                condition_session = 'session1',
                local_vars_configuration=local_vars_configuration
            )
        else :
            return FeatureRemoveRequest(
                feature = 'year',
                local_vars_configuration=local_vars_configuration
            )

    def testFeatureRemoveRequest(self):
        """Test FeatureRemoveRequest"""
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
