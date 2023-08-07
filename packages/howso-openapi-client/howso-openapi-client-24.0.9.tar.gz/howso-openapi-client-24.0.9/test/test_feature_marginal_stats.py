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
from howso.openapi.models.feature_marginal_stats import FeatureMarginalStats  # noqa: E501
from howso.openapi.configuration import Configuration


class TestFeatureMarginalStats(unittest.TestCase):
    """FeatureMarginalStats unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional, local_vars_configuration=None):
        """Test FeatureMarginalStats
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = howso.openapi.models.feature_marginal_stats.FeatureMarginalStats()  # noqa: E501
        if include_optional :
            return FeatureMarginalStats(
                warnings = [
                    {"detail":"Results may be inaccurate because trainee has not been analyzed with case weights."}
                    ],
                content = {
                    'key' : howso.openapi.models.marginal_stats.MarginalStats(
                        count = 0.5, 
                        kurtosis = 0.5, 
                        mean = 0.5, 
                        mean_absdev = 0.5, 
                        median = 0.5, 
                        mode = 0.5, 
                        min = 0.5, 
                        max = 0.5, 
                        percentile_25 = 0.5, 
                        percentile_75 = 0.5, 
                        skew = 0.5, 
                        stddev = 0.5, 
                        uniques = 0.5, 
                        variance = 0.5, )
                    },
                local_vars_configuration=local_vars_configuration
            )
        else :
            return FeatureMarginalStats(
                local_vars_configuration=local_vars_configuration
            )

    def testFeatureMarginalStats(self):
        """Test FeatureMarginalStats"""
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
