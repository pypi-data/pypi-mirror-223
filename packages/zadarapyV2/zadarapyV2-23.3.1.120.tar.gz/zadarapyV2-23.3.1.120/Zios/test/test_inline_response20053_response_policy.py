# coding: utf-8

"""
    Zadara VPSA Object Storage REST API

    # Overview  This document outlines the methods available for administrating your VPSA&#174; Object Storage. The API supports form-encoded, JSON, and XML requests, and can return either JSON or XML responses.  ## Usage  The majority of the APIs available require authentication which requires an API token to use. You can retrieve this token through the Users section of your VPSA, or through the API using the \"Return a user's access key\" API in the Users Section below.  ## Authentication Methods  The authentication token can be passed either through the access_key parameter inside of the body of the REST API request, or through the X-Access-Key header. Alternately, you can use the username and password parameters for authentication, but we do not recommend this method for anything other than possibly retrieving an API key.  By default , all operations are allowed only to VPSA Object Storage admin. Some actions are allowed by an account admin and they will be marked on the action's header  ## Timeouts  By default, all operations that don't complete within five seconds will return a message informing you that the action may take some time to complete. When using the API, this can cause some actions, such as adding drives to storage policy, to be undesirably asynchronous. You can specify your own timeout with the timeout parameter, in seconds, and a timeout value of -1 specifies an infinite timeout.  ## Metering API  Metering information can be retrieved using the VPSA Object Storage API for the following components:  - Accounts - Users - Drives - Virtual Controllers - Load Balancer Groups - Storage Policies  Metering information returned by the API is subject to the following constraints:  - 10 seconds interval - 1 hour range - 1 minute interval - 1 day range - 1 hour interval - 30 days range  Values outside the accepted range will be returned as 0.  ## Questions  If you have any questions or need support involving the REST API, please contact for assistance.   # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import Zios
from Zios.models.inline_response20053_response_policy import InlineResponse20053ResponsePolicy  # noqa: E501
from Zios.rest import ApiException


class TestInlineResponse20053ResponsePolicy(unittest.TestCase):
    """InlineResponse20053ResponsePolicy unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testInlineResponse20053ResponsePolicy(self):
        """Test InlineResponse20053ResponsePolicy"""
        # FIXME: construct object with mandatory attributes with example values
        # model = Zios.models.inline_response20053_response_policy.InlineResponse20053ResponsePolicy()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
