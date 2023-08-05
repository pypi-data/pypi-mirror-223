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


class DeleteVirtualNetworks(object):
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
        'provider_id': 'int',
        'vlan': 'int'
    }

    attribute_map = {
        'provider_id': 'provider_id',
        'vlan': 'vlan'
    }

    def __init__(self, provider_id=None, vlan=None, _configuration=None):  # noqa: E501
        """DeleteVirtualNetworks - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._provider_id = None
        self._vlan = None
        self.discriminator = None

        self.provider_id = provider_id
        self.vlan = vlan

    @property
    def provider_id(self):
        """Gets the provider_id of this DeleteVirtualNetworks.  # noqa: E501


        :return: The provider_id of this DeleteVirtualNetworks.  # noqa: E501
        :rtype: int
        """
        return self._provider_id

    @provider_id.setter
    def provider_id(self, provider_id):
        """Sets the provider_id of this DeleteVirtualNetworks.


        :param provider_id: The provider_id of this DeleteVirtualNetworks.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and provider_id is None:
            raise ValueError("Invalid value for `provider_id`, must not be `None`")  # noqa: E501

        self._provider_id = provider_id

    @property
    def vlan(self):
        """Gets the vlan of this DeleteVirtualNetworks.  # noqa: E501


        :return: The vlan of this DeleteVirtualNetworks.  # noqa: E501
        :rtype: int
        """
        return self._vlan

    @vlan.setter
    def vlan(self, vlan):
        """Sets the vlan of this DeleteVirtualNetworks.


        :param vlan: The vlan of this DeleteVirtualNetworks.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and vlan is None:
            raise ValueError("Invalid value for `vlan`, must not be `None`")  # noqa: E501

        self._vlan = vlan

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
        if issubclass(DeleteVirtualNetworks, dict):
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
        if not isinstance(other, DeleteVirtualNetworks):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DeleteVirtualNetworks):
            return True

        return self.to_dict() != other.to_dict()
