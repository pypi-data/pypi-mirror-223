# coding: utf-8

"""
    Command Center operations

    Command Center operations  # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from CommandCenter.configuration import Configuration


class CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'ip_or_cidr': 'str',
        'app_access': 'str',
        'comment': 'str'
    }

    attribute_map = {
        'ip_or_cidr': 'ip_or_cidr',
        'app_access': 'app_access',
        'comment': 'comment'
    }

    def __init__(self, ip_or_cidr=None, app_access=None, comment=None, _configuration=None):  # noqa: E501
        """CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._ip_or_cidr = None
        self._app_access = None
        self._comment = None
        self.discriminator = None

        if ip_or_cidr is not None:
            self.ip_or_cidr = ip_or_cidr
        if app_access is not None:
            self.app_access = app_access
        if comment is not None:
            self.comment = comment

    @property
    def ip_or_cidr(self):
        """Gets the ip_or_cidr of this CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries.  # noqa: E501


        :return: The ip_or_cidr of this CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries.  # noqa: E501
        :rtype: str
        """
        return self._ip_or_cidr

    @ip_or_cidr.setter
    def ip_or_cidr(self, ip_or_cidr):
        """Sets the ip_or_cidr of this CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries.


        :param ip_or_cidr: The ip_or_cidr of this CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries.  # noqa: E501
        :type: str
        """

        self._ip_or_cidr = ip_or_cidr

    @property
    def app_access(self):
        """Gets the app_access of this CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries.  # noqa: E501


        :return: The app_access of this CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries.  # noqa: E501
        :rtype: str
        """
        return self._app_access

    @app_access.setter
    def app_access(self, app_access):
        """Sets the app_access of this CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries.


        :param app_access: The app_access of this CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries.  # noqa: E501
        :type: str
        """

        self._app_access = app_access

    @property
    def comment(self):
        """Gets the comment of this CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries.  # noqa: E501


        :return: The comment of this CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries.  # noqa: E501
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries.


        :param comment: The comment of this CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries.  # noqa: E501
        :type: str
        """

        self._comment = comment

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CloudscloudNamesettingsaddCloudControlIpWhitelistingEntriesJsonEntries):
            return True

        return self.to_dict() != other.to_dict()
