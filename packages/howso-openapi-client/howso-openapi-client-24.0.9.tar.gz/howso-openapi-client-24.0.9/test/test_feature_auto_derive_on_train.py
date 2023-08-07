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
from howso.openapi.models.feature_auto_derive_on_train import FeatureAutoDeriveOnTrain  # noqa: E501
from howso.openapi.configuration import Configuration


class TestFeatureAutoDeriveOnTrain(unittest.TestCase):
    """FeatureAutoDeriveOnTrain unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test FeatureAutoDeriveOnTrain
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.feature_auto_derive_on_train.FeatureAutoDeriveOnTrain()  # noqa: E501
        if include_optional :
            return FeatureAutoDeriveOnTrain(
                derive_type = 'progress',
                code = '(- #y 0 #x 1)',
                series_id_features = ["x","y"],
                ordered_by_features = ["y","x"],
                local_vars_configuration=local_vars_configuration
            )
        else :
            return FeatureAutoDeriveOnTrain(
                derive_type = 'progress',
                code = '(- #y 0 #x 1)',
                series_id_features = ["x","y"],
                local_vars_configuration=local_vars_configuration
            )

    def testFeatureAutoDeriveOnTrain(self):
        """Test FeatureAutoDeriveOnTrain"""
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
