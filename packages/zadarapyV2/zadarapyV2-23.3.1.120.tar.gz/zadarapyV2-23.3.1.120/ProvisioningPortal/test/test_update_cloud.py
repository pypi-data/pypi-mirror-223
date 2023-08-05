# coding: utf-8

"""
    Zadara Provisioning Portal API

     # Overview  This document outlines the methods available for creation and high-level administration of Zadara Storage VPSAs via a Zadara Storage Provisioning Portal. This API supports form-encoded requests, and can return either JSON or XML responses.  ## Endpoint  The base URL for the requests is the Provisioning Portal URL you created your VPSA through - for example: https://manage.zadarastorage.com/, and all APIs will be prefixed with /api as noted in the documentation below.  ## Authentication  To use this API, an authentication token is required. The API for retrieving this token can be found below in the Authentication section. You may pass this token in requests either via the the X-Token header or via basic authentication (base64 encoded) in Authorization header.  ## Questions  If you have any questions or need support involving the REST API, please contact for assistance.   # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import ProvisioningPortal
from ProvisioningPortal.models.update_cloud import UpdateCloud  # noqa: E501
from ProvisioningPortal.rest import ApiException


class TestUpdateCloud(unittest.TestCase):
    """UpdateCloud unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testUpdateCloud(self):
        """Test UpdateCloud"""
        # FIXME: construct object with mandatory attributes with example values
        # model = ProvisioningPortal.models.update_cloud.UpdateCloud()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
