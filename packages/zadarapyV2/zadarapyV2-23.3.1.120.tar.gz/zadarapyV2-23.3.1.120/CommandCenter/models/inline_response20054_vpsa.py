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


class InlineResponse20054Vpsa(object):
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
        'domain_name': 'str',
        'recycle_bin': 'InlineResponse20054RecycleBin'
    }

    attribute_map = {
        'domain_name': 'domain_name',
        'recycle_bin': 'recycle_bin'
    }

    def __init__(self, domain_name=None, recycle_bin=None, _configuration=None):  # noqa: E501
        """InlineResponse20054Vpsa - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._domain_name = None
        self._recycle_bin = None
        self.discriminator = None

        if domain_name is not None:
            self.domain_name = domain_name
        if recycle_bin is not None:
            self.recycle_bin = recycle_bin

    @property
    def domain_name(self):
        """Gets the domain_name of this InlineResponse20054Vpsa.  # noqa: E501


        :return: The domain_name of this InlineResponse20054Vpsa.  # noqa: E501
        :rtype: str
        """
        return self._domain_name

    @domain_name.setter
    def domain_name(self, domain_name):
        """Sets the domain_name of this InlineResponse20054Vpsa.


        :param domain_name: The domain_name of this InlineResponse20054Vpsa.  # noqa: E501
        :type: str
        """

        self._domain_name = domain_name

    @property
    def recycle_bin(self):
        """Gets the recycle_bin of this InlineResponse20054Vpsa.  # noqa: E501


        :return: The recycle_bin of this InlineResponse20054Vpsa.  # noqa: E501
        :rtype: InlineResponse20054RecycleBin
        """
        return self._recycle_bin

    @recycle_bin.setter
    def recycle_bin(self, recycle_bin):
        """Sets the recycle_bin of this InlineResponse20054Vpsa.


        :param recycle_bin: The recycle_bin of this InlineResponse20054Vpsa.  # noqa: E501
        :type: InlineResponse20054RecycleBin
        """

        self._recycle_bin = recycle_bin

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
        if issubclass(InlineResponse20054Vpsa, dict):
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
        if not isinstance(other, InlineResponse20054Vpsa):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20054Vpsa):
            return True

        return self.to_dict() != other.to_dict()
