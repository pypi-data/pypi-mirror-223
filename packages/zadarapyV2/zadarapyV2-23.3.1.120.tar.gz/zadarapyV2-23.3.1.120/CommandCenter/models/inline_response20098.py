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


class InlineResponse20098(object):
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
        'pools': 'InlineResponse20098Pools',
        'count': 'int'
    }

    attribute_map = {
        'status': 'status',
        'pools': 'pools',
        'count': 'count'
    }

    def __init__(self, status=None, pools=None, count=None, _configuration=None):  # noqa: E501
        """InlineResponse20098 - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._status = None
        self._pools = None
        self._count = None
        self.discriminator = None

        if status is not None:
            self.status = status
        if pools is not None:
            self.pools = pools
        if count is not None:
            self.count = count

    @property
    def status(self):
        """Gets the status of this InlineResponse20098.  # noqa: E501


        :return: The status of this InlineResponse20098.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InlineResponse20098.


        :param status: The status of this InlineResponse20098.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def pools(self):
        """Gets the pools of this InlineResponse20098.  # noqa: E501


        :return: The pools of this InlineResponse20098.  # noqa: E501
        :rtype: InlineResponse20098Pools
        """
        return self._pools

    @pools.setter
    def pools(self, pools):
        """Sets the pools of this InlineResponse20098.


        :param pools: The pools of this InlineResponse20098.  # noqa: E501
        :type: InlineResponse20098Pools
        """

        self._pools = pools

    @property
    def count(self):
        """Gets the count of this InlineResponse20098.  # noqa: E501


        :return: The count of this InlineResponse20098.  # noqa: E501
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this InlineResponse20098.


        :param count: The count of this InlineResponse20098.  # noqa: E501
        :type: int
        """

        self._count = count

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
        if issubclass(InlineResponse20098, dict):
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
        if not isinstance(other, InlineResponse20098):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20098):
            return True

        return self.to_dict() != other.to_dict()
