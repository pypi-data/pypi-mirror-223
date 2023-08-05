# coding: utf-8

"""
    Zadara VPSA Storage Array REST API

     # Overview  This document outlines the methods available for administrating your Zadara Storage VPSA&#8482;. The Zadara Storage Array REST API   supports form-encoded, JSON, and XML requests, and can return either JSON or XML responses.  ## Usage  The majority of the APIs available require authentication which requires an API token to use. You can retrieve this token through the   Users section of your VPSA, or through the API using the \"Return a user's access key\" API in the Users Section below.  ## Authentication Methods  The authentication token can be passed either through the access_key parameter inside of the body of the REST API request, or   through the X-Access-Key header.  ## Timeouts  By default, all operations that don't complete within five seconds will return a message informing you that the action may take some  time to complete. When using the API, this can cause some actions, such as large volume creation, to be undesirably asynchronous.  You can specify your own timeout with the timeout parameter, in seconds, and a timeout value of -1 specifies an infinite timeout.  ## Specific Fields For Product  Some of the fields/actions used in the API should be used only for a specific product. The following tags are used to mark which   product responds to the fields/actions  VPSA Flash Array  VPSA Storage Array - Hybrid VPSA  ## Questions  If you have any questions or need support involving the REST API, please contact for assistance.   # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import Vpsa
from Vpsa.api.consistency_groups_api import ConsistencyGroupsApi  # noqa: E501
from Vpsa.rest import ApiException


class TestConsistencyGroupsApi(unittest.TestCase):
    """ConsistencyGroupsApi unit test stubs"""

    def setUp(self):
        self.api = Vpsa.api.consistency_groups_api.ConsistencyGroupsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_cancel_suspend_for_snapshot_set(self):
        """Test case for cancel_suspend_for_snapshot_set

        """
        pass

    def test_clone_snapshot_set(self):
        """Test case for clone_snapshot_set

        """
        pass

    def test_create_snapshot_set_and_resume(self):
        """Test case for create_snapshot_set_and_resume

        """
        pass

    def test_delete_clone_snapshot_set(self):
        """Test case for delete_clone_snapshot_set

        """
        pass

    def test_delete_snapshot_set(self):
        """Test case for delete_snapshot_set

        """
        pass

    def test_suspend_cgs_for_snapshot_set(self):
        """Test case for suspend_cgs_for_snapshot_set

        """
        pass


if __name__ == '__main__':
    unittest.main()
