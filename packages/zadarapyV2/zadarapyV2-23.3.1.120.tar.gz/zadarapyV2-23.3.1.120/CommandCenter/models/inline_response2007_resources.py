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


class InlineResponse2007Resources(object):
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
        'used_memory': 'int',
        'total_memory': 'int',
        'used_vcpus': 'int',
        'total_vcpus': 'int',
        'used_drives': 'int',
        'total_drives': 'int',
        'used_capacity': 'int',
        'total_capacity': 'int',
        'used_cache': 'int',
        'total_cache': 'int'
    }

    attribute_map = {
        'used_memory': 'used_memory',
        'total_memory': 'total_memory',
        'used_vcpus': 'used_vcpus',
        'total_vcpus': 'total_vcpus',
        'used_drives': 'used_drives',
        'total_drives': 'total_drives',
        'used_capacity': 'used_capacity',
        'total_capacity': 'total_capacity',
        'used_cache': 'used_cache',
        'total_cache': 'total_cache'
    }

    def __init__(self, used_memory=None, total_memory=None, used_vcpus=None, total_vcpus=None, used_drives=None, total_drives=None, used_capacity=None, total_capacity=None, used_cache=None, total_cache=None, _configuration=None):  # noqa: E501
        """InlineResponse2007Resources - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._used_memory = None
        self._total_memory = None
        self._used_vcpus = None
        self._total_vcpus = None
        self._used_drives = None
        self._total_drives = None
        self._used_capacity = None
        self._total_capacity = None
        self._used_cache = None
        self._total_cache = None
        self.discriminator = None

        if used_memory is not None:
            self.used_memory = used_memory
        if total_memory is not None:
            self.total_memory = total_memory
        if used_vcpus is not None:
            self.used_vcpus = used_vcpus
        if total_vcpus is not None:
            self.total_vcpus = total_vcpus
        if used_drives is not None:
            self.used_drives = used_drives
        if total_drives is not None:
            self.total_drives = total_drives
        if used_capacity is not None:
            self.used_capacity = used_capacity
        if total_capacity is not None:
            self.total_capacity = total_capacity
        if used_cache is not None:
            self.used_cache = used_cache
        if total_cache is not None:
            self.total_cache = total_cache

    @property
    def used_memory(self):
        """Gets the used_memory of this InlineResponse2007Resources.  # noqa: E501


        :return: The used_memory of this InlineResponse2007Resources.  # noqa: E501
        :rtype: int
        """
        return self._used_memory

    @used_memory.setter
    def used_memory(self, used_memory):
        """Sets the used_memory of this InlineResponse2007Resources.


        :param used_memory: The used_memory of this InlineResponse2007Resources.  # noqa: E501
        :type: int
        """

        self._used_memory = used_memory

    @property
    def total_memory(self):
        """Gets the total_memory of this InlineResponse2007Resources.  # noqa: E501


        :return: The total_memory of this InlineResponse2007Resources.  # noqa: E501
        :rtype: int
        """
        return self._total_memory

    @total_memory.setter
    def total_memory(self, total_memory):
        """Sets the total_memory of this InlineResponse2007Resources.


        :param total_memory: The total_memory of this InlineResponse2007Resources.  # noqa: E501
        :type: int
        """

        self._total_memory = total_memory

    @property
    def used_vcpus(self):
        """Gets the used_vcpus of this InlineResponse2007Resources.  # noqa: E501


        :return: The used_vcpus of this InlineResponse2007Resources.  # noqa: E501
        :rtype: int
        """
        return self._used_vcpus

    @used_vcpus.setter
    def used_vcpus(self, used_vcpus):
        """Sets the used_vcpus of this InlineResponse2007Resources.


        :param used_vcpus: The used_vcpus of this InlineResponse2007Resources.  # noqa: E501
        :type: int
        """

        self._used_vcpus = used_vcpus

    @property
    def total_vcpus(self):
        """Gets the total_vcpus of this InlineResponse2007Resources.  # noqa: E501


        :return: The total_vcpus of this InlineResponse2007Resources.  # noqa: E501
        :rtype: int
        """
        return self._total_vcpus

    @total_vcpus.setter
    def total_vcpus(self, total_vcpus):
        """Sets the total_vcpus of this InlineResponse2007Resources.


        :param total_vcpus: The total_vcpus of this InlineResponse2007Resources.  # noqa: E501
        :type: int
        """

        self._total_vcpus = total_vcpus

    @property
    def used_drives(self):
        """Gets the used_drives of this InlineResponse2007Resources.  # noqa: E501


        :return: The used_drives of this InlineResponse2007Resources.  # noqa: E501
        :rtype: int
        """
        return self._used_drives

    @used_drives.setter
    def used_drives(self, used_drives):
        """Sets the used_drives of this InlineResponse2007Resources.


        :param used_drives: The used_drives of this InlineResponse2007Resources.  # noqa: E501
        :type: int
        """

        self._used_drives = used_drives

    @property
    def total_drives(self):
        """Gets the total_drives of this InlineResponse2007Resources.  # noqa: E501


        :return: The total_drives of this InlineResponse2007Resources.  # noqa: E501
        :rtype: int
        """
        return self._total_drives

    @total_drives.setter
    def total_drives(self, total_drives):
        """Sets the total_drives of this InlineResponse2007Resources.


        :param total_drives: The total_drives of this InlineResponse2007Resources.  # noqa: E501
        :type: int
        """

        self._total_drives = total_drives

    @property
    def used_capacity(self):
        """Gets the used_capacity of this InlineResponse2007Resources.  # noqa: E501


        :return: The used_capacity of this InlineResponse2007Resources.  # noqa: E501
        :rtype: int
        """
        return self._used_capacity

    @used_capacity.setter
    def used_capacity(self, used_capacity):
        """Sets the used_capacity of this InlineResponse2007Resources.


        :param used_capacity: The used_capacity of this InlineResponse2007Resources.  # noqa: E501
        :type: int
        """

        self._used_capacity = used_capacity

    @property
    def total_capacity(self):
        """Gets the total_capacity of this InlineResponse2007Resources.  # noqa: E501


        :return: The total_capacity of this InlineResponse2007Resources.  # noqa: E501
        :rtype: int
        """
        return self._total_capacity

    @total_capacity.setter
    def total_capacity(self, total_capacity):
        """Sets the total_capacity of this InlineResponse2007Resources.


        :param total_capacity: The total_capacity of this InlineResponse2007Resources.  # noqa: E501
        :type: int
        """

        self._total_capacity = total_capacity

    @property
    def used_cache(self):
        """Gets the used_cache of this InlineResponse2007Resources.  # noqa: E501


        :return: The used_cache of this InlineResponse2007Resources.  # noqa: E501
        :rtype: int
        """
        return self._used_cache

    @used_cache.setter
    def used_cache(self, used_cache):
        """Sets the used_cache of this InlineResponse2007Resources.


        :param used_cache: The used_cache of this InlineResponse2007Resources.  # noqa: E501
        :type: int
        """

        self._used_cache = used_cache

    @property
    def total_cache(self):
        """Gets the total_cache of this InlineResponse2007Resources.  # noqa: E501


        :return: The total_cache of this InlineResponse2007Resources.  # noqa: E501
        :rtype: int
        """
        return self._total_cache

    @total_cache.setter
    def total_cache(self, total_cache):
        """Sets the total_cache of this InlineResponse2007Resources.


        :param total_cache: The total_cache of this InlineResponse2007Resources.  # noqa: E501
        :type: int
        """

        self._total_cache = total_cache

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
        if issubclass(InlineResponse2007Resources, dict):
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
        if not isinstance(other, InlineResponse2007Resources):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse2007Resources):
            return True

        return self.to_dict() != other.to_dict()
