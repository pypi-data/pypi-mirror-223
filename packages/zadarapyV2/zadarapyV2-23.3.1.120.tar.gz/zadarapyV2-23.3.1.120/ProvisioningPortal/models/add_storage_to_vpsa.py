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


class AddStorageToVpsa(object):
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
        'drives': 'VpsasvpsaIddrivesJsonDrives',
        'storage_policy': 'str'
    }

    attribute_map = {
        'drives': 'drives',
        'storage_policy': 'storage_policy'
    }

    def __init__(self, drives=None, storage_policy=None, _configuration=None):  # noqa: E501
        """AddStorageToVpsa - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._drives = None
        self._storage_policy = None
        self.discriminator = None

        self.drives = drives
        if storage_policy is not None:
            self.storage_policy = storage_policy

    @property
    def drives(self):
        """Gets the drives of this AddStorageToVpsa.  # noqa: E501


        :return: The drives of this AddStorageToVpsa.  # noqa: E501
        :rtype: VpsasvpsaIddrivesJsonDrives
        """
        return self._drives

    @drives.setter
    def drives(self, drives):
        """Sets the drives of this AddStorageToVpsa.


        :param drives: The drives of this AddStorageToVpsa.  # noqa: E501
        :type: VpsasvpsaIddrivesJsonDrives
        """
        if self._configuration.client_side_validation and drives is None:
            raise ValueError("Invalid value for `drives`, must not be `None`")  # noqa: E501

        self._drives = drives

    @property
    def storage_policy(self):
        """Gets the storage_policy of this AddStorageToVpsa.  # noqa: E501

        Storage Policy Name. (Only for VPSA Object Storage)  # noqa: E501

        :return: The storage_policy of this AddStorageToVpsa.  # noqa: E501
        :rtype: str
        """
        return self._storage_policy

    @storage_policy.setter
    def storage_policy(self, storage_policy):
        """Sets the storage_policy of this AddStorageToVpsa.

        Storage Policy Name. (Only for VPSA Object Storage)  # noqa: E501

        :param storage_policy: The storage_policy of this AddStorageToVpsa.  # noqa: E501
        :type: str
        """

        self._storage_policy = storage_policy

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
        if issubclass(AddStorageToVpsa, dict):
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
        if not isinstance(other, AddStorageToVpsa):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AddStorageToVpsa):
            return True

        return self.to_dict() != other.to_dict()
