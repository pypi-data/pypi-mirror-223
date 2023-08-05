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


class InlineResponse20054CacheOrAfaMetaDrivesSettings(object):
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
        'ssd_cache_max_usable_capacity_gb': 'int',
        'allow_temporarily_set_ssds_as_afa_meta': 'str'
    }

    attribute_map = {
        'ssd_cache_max_usable_capacity_gb': 'ssd_cache_max_usable_capacity_gb',
        'allow_temporarily_set_ssds_as_afa_meta': 'allow_temporarily_set_ssds_as_afa_meta'
    }

    def __init__(self, ssd_cache_max_usable_capacity_gb=None, allow_temporarily_set_ssds_as_afa_meta=None, _configuration=None):  # noqa: E501
        """InlineResponse20054CacheOrAfaMetaDrivesSettings - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._ssd_cache_max_usable_capacity_gb = None
        self._allow_temporarily_set_ssds_as_afa_meta = None
        self.discriminator = None

        if ssd_cache_max_usable_capacity_gb is not None:
            self.ssd_cache_max_usable_capacity_gb = ssd_cache_max_usable_capacity_gb
        if allow_temporarily_set_ssds_as_afa_meta is not None:
            self.allow_temporarily_set_ssds_as_afa_meta = allow_temporarily_set_ssds_as_afa_meta

    @property
    def ssd_cache_max_usable_capacity_gb(self):
        """Gets the ssd_cache_max_usable_capacity_gb of this InlineResponse20054CacheOrAfaMetaDrivesSettings.  # noqa: E501


        :return: The ssd_cache_max_usable_capacity_gb of this InlineResponse20054CacheOrAfaMetaDrivesSettings.  # noqa: E501
        :rtype: int
        """
        return self._ssd_cache_max_usable_capacity_gb

    @ssd_cache_max_usable_capacity_gb.setter
    def ssd_cache_max_usable_capacity_gb(self, ssd_cache_max_usable_capacity_gb):
        """Sets the ssd_cache_max_usable_capacity_gb of this InlineResponse20054CacheOrAfaMetaDrivesSettings.


        :param ssd_cache_max_usable_capacity_gb: The ssd_cache_max_usable_capacity_gb of this InlineResponse20054CacheOrAfaMetaDrivesSettings.  # noqa: E501
        :type: int
        """

        self._ssd_cache_max_usable_capacity_gb = ssd_cache_max_usable_capacity_gb

    @property
    def allow_temporarily_set_ssds_as_afa_meta(self):
        """Gets the allow_temporarily_set_ssds_as_afa_meta of this InlineResponse20054CacheOrAfaMetaDrivesSettings.  # noqa: E501


        :return: The allow_temporarily_set_ssds_as_afa_meta of this InlineResponse20054CacheOrAfaMetaDrivesSettings.  # noqa: E501
        :rtype: str
        """
        return self._allow_temporarily_set_ssds_as_afa_meta

    @allow_temporarily_set_ssds_as_afa_meta.setter
    def allow_temporarily_set_ssds_as_afa_meta(self, allow_temporarily_set_ssds_as_afa_meta):
        """Sets the allow_temporarily_set_ssds_as_afa_meta of this InlineResponse20054CacheOrAfaMetaDrivesSettings.


        :param allow_temporarily_set_ssds_as_afa_meta: The allow_temporarily_set_ssds_as_afa_meta of this InlineResponse20054CacheOrAfaMetaDrivesSettings.  # noqa: E501
        :type: str
        """

        self._allow_temporarily_set_ssds_as_afa_meta = allow_temporarily_set_ssds_as_afa_meta

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
        if issubclass(InlineResponse20054CacheOrAfaMetaDrivesSettings, dict):
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
        if not isinstance(other, InlineResponse20054CacheOrAfaMetaDrivesSettings):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20054CacheOrAfaMetaDrivesSettings):
            return True

        return self.to_dict() != other.to_dict()
