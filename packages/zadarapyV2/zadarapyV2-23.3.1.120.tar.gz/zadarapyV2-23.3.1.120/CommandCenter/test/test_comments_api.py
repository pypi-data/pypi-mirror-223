# coding: utf-8

"""
    Command Center operations

    Command Center operations  # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import unittest

import CommandCenter
from CommandCenter.api.comments_api import CommentsApi  # noqa: E501
from CommandCenter.rest import ApiException


class TestCommentsApi(unittest.TestCase):
    """CommentsApi unit test stubs"""

    def setUp(self):
        self.api = CommandCenter.api.comments_api.CommentsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_comment(self):
        """Test case for create_comment

        """
        pass

    def test_delete_comment(self):
        """Test case for delete_comment

        """
        pass

    def test_edit_comment(self):
        """Test case for edit_comment

        """
        pass

    def test_get_comment_details(self):
        """Test case for get_comment_details

        """
        pass

    def test_list_type_comments(self):
        """Test case for list_type_comments

        """
        pass


if __name__ == '__main__':
    unittest.main()
