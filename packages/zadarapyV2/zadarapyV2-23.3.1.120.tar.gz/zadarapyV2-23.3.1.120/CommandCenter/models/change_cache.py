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


class ChangeCache(object):
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
        'cache': 'int'
    }

    attribute_map = {
        'cache': 'cache'
    }

    def __init__(self, cache=None, _configuration=None):  # noqa: E501
        """ChangeCache - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._cache = None
        self.discriminator = None

        self.cache = cache

    @property
    def cache(self):
        """Gets the cache of this ChangeCache.  # noqa: E501

        New cache size  # noqa: E501

        :return: The cache of this ChangeCache.  # noqa: E501
        :rtype: int
        """
        return self._cache

    @cache.setter
    def cache(self, cache):
        """Sets the cache of this ChangeCache.

        New cache size  # noqa: E501

        :param cache: The cache of this ChangeCache.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and cache is None:
            raise ValueError("Invalid value for `cache`, must not be `None`")  # noqa: E501

        self._cache = cache

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
        if issubclass(ChangeCache, dict):
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
        if not isinstance(other, ChangeCache):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChangeCache):
            return True

        return self.to_dict() != other.to_dict()
