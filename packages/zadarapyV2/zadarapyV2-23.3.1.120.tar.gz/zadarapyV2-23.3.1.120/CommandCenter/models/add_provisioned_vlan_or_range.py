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


class AddProvisionedVlanOrRange(object):
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
        'range_start': 'int',
        'range_end': 'int'
    }

    attribute_map = {
        'range_start': 'range_start',
        'range_end': 'range_end'
    }

    def __init__(self, range_start=None, range_end=None, _configuration=None):  # noqa: E501
        """AddProvisionedVlanOrRange - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._range_start = None
        self._range_end = None
        self.discriminator = None

        self.range_start = range_start
        if range_end is not None:
            self.range_end = range_end

    @property
    def range_start(self):
        """Gets the range_start of this AddProvisionedVlanOrRange.  # noqa: E501


        :return: The range_start of this AddProvisionedVlanOrRange.  # noqa: E501
        :rtype: int
        """
        return self._range_start

    @range_start.setter
    def range_start(self, range_start):
        """Sets the range_start of this AddProvisionedVlanOrRange.


        :param range_start: The range_start of this AddProvisionedVlanOrRange.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and range_start is None:
            raise ValueError("Invalid value for `range_start`, must not be `None`")  # noqa: E501

        self._range_start = range_start

    @property
    def range_end(self):
        """Gets the range_end of this AddProvisionedVlanOrRange.  # noqa: E501

        If not provided, range_start will be added as single vlan  # noqa: E501

        :return: The range_end of this AddProvisionedVlanOrRange.  # noqa: E501
        :rtype: int
        """
        return self._range_end

    @range_end.setter
    def range_end(self, range_end):
        """Sets the range_end of this AddProvisionedVlanOrRange.

        If not provided, range_start will be added as single vlan  # noqa: E501

        :param range_end: The range_end of this AddProvisionedVlanOrRange.  # noqa: E501
        :type: int
        """

        self._range_end = range_end

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
        if issubclass(AddProvisionedVlanOrRange, dict):
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
        if not isinstance(other, AddProvisionedVlanOrRange):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AddProvisionedVlanOrRange):
            return True

        return self.to_dict() != other.to_dict()
