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


class InlineResponse20021(object):
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
        'status': 'str',
        'drive': 'InlineResponse20020Drives'
    }

    attribute_map = {
        'status': 'status',
        'drive': 'drive'
    }

    def __init__(self, status=None, drive=None, _configuration=None):  # noqa: E501
        """InlineResponse20021 - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._status = None
        self._drive = None
        self.discriminator = None

        if status is not None:
            self.status = status
        if drive is not None:
            self.drive = drive

    @property
    def status(self):
        """Gets the status of this InlineResponse20021.  # noqa: E501


        :return: The status of this InlineResponse20021.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InlineResponse20021.


        :param status: The status of this InlineResponse20021.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def drive(self):
        """Gets the drive of this InlineResponse20021.  # noqa: E501


        :return: The drive of this InlineResponse20021.  # noqa: E501
        :rtype: InlineResponse20020Drives
        """
        return self._drive

    @drive.setter
    def drive(self, drive):
        """Sets the drive of this InlineResponse20021.


        :param drive: The drive of this InlineResponse20021.  # noqa: E501
        :type: InlineResponse20020Drives
        """

        self._drive = drive

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
        if issubclass(InlineResponse20021, dict):
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
        if not isinstance(other, InlineResponse20021):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20021):
            return True

        return self.to_dict() != other.to_dict()
