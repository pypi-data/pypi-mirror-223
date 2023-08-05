# coding: utf-8

"""
    Zadara Provisioning Portal API

     # Overview  This document outlines the methods available for creation and high-level administration of Zadara Storage VPSAs via a Zadara Storage Provisioning Portal. This API supports form-encoded requests, and can return either JSON or XML responses.  ## Endpoint  The base URL for the requests is the Provisioning Portal URL you created your VPSA through - for example: https://manage.zadarastorage.com/, and all APIs will be prefixed with /api as noted in the documentation below.  ## Authentication  To use this API, an authentication token is required. The API for retrieving this token can be found below in the Authentication section. You may pass this token in requests either via the the X-Token header or via basic authentication (base64 encoded) in Authorization header.  ## Questions  If you have any questions or need support involving the REST API, please contact for assistance.   # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from ProvisioningPortal.configuration import Configuration


class ChangeVpsaFlashCacheCapacity(object):
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
        'flash_cache_capacity': 'int'
    }

    attribute_map = {
        'flash_cache_capacity': 'flash_cache_capacity'
    }

    def __init__(self, flash_cache_capacity=None, _configuration=None):  # noqa: E501
        """ChangeVpsaFlashCacheCapacity - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._flash_cache_capacity = None
        self.discriminator = None

        self.flash_cache_capacity = flash_cache_capacity

    @property
    def flash_cache_capacity(self):
        """Gets the flash_cache_capacity of this ChangeVpsaFlashCacheCapacity.  # noqa: E501

        Amount of extended flash (in 200GB steps).  # noqa: E501

        :return: The flash_cache_capacity of this ChangeVpsaFlashCacheCapacity.  # noqa: E501
        :rtype: int
        """
        return self._flash_cache_capacity

    @flash_cache_capacity.setter
    def flash_cache_capacity(self, flash_cache_capacity):
        """Sets the flash_cache_capacity of this ChangeVpsaFlashCacheCapacity.

        Amount of extended flash (in 200GB steps).  # noqa: E501

        :param flash_cache_capacity: The flash_cache_capacity of this ChangeVpsaFlashCacheCapacity.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and flash_cache_capacity is None:
            raise ValueError("Invalid value for `flash_cache_capacity`, must not be `None`")  # noqa: E501

        self._flash_cache_capacity = flash_cache_capacity

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
        if issubclass(ChangeVpsaFlashCacheCapacity, dict):
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
        if not isinstance(other, ChangeVpsaFlashCacheCapacity):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChangeVpsaFlashCacheCapacity):
            return True

        return self.to_dict() != other.to_dict()
