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
from Vpsa.api.users_api import UsersApi  # noqa: E501
from Vpsa.rest import ApiException


class TestUsersApi(unittest.TestCase):
    """UsersApi unit test stubs"""

    def setUp(self):
        self.api = Vpsa.api.users_api.UsersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_add_user(self):
        """Test case for add_user

        """
        pass

    def test_change_user_pass(self):
        """Test case for change_user_pass

        """
        pass

    def test_change_user_pass_by_temp_code(self):
        """Test case for change_user_pass_by_temp_code

        """
        pass

    def test_delete_user(self):
        """Test case for delete_user

        """
        pass

    def test_disable_cloud_admin_access(self):
        """Test case for disable_cloud_admin_access

        """
        pass

    def test_enable_cloud_admin_access(self):
        """Test case for enable_cloud_admin_access

        """
        pass

    def test_get_pass_requirements(self):
        """Test case for get_pass_requirements

        """
        pass

    def test_get_user_details(self):
        """Test case for get_user_details

        """
        pass

    def test_issue_user_temp_code(self):
        """Test case for issue_user_temp_code

        """
        pass

    def test_list_users(self):
        """Test case for list_users

        """
        pass

    def test_reset_user_access_key(self):
        """Test case for reset_user_access_key

        """
        pass

    def test_update_user_info(self):
        """Test case for update_user_info

        """
        pass

    def test_update_user_roles(self):
        """Test case for update_user_roles

        """
        pass


if __name__ == '__main__':
    unittest.main()
