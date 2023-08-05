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


class InlineResponse2007Data(object):
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
        'id': 'str',
        'name': 'str',
        'key': 'str',
        'provider_group_id': 'str',
        'cloud_id': 'str',
        'enabled': 'str',
        'hidden': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'key': 'key',
        'provider_group_id': 'provider_group_id',
        'cloud_id': 'cloud_id',
        'enabled': 'enabled',
        'hidden': 'hidden'
    }

    def __init__(self, id=None, name=None, key=None, provider_group_id=None, cloud_id=None, enabled=None, hidden=None, _configuration=None):  # noqa: E501
        """InlineResponse2007Data - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._id = None
        self._name = None
        self._key = None
        self._provider_group_id = None
        self._cloud_id = None
        self._enabled = None
        self._hidden = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if key is not None:
            self.key = key
        if provider_group_id is not None:
            self.provider_group_id = provider_group_id
        if cloud_id is not None:
            self.cloud_id = cloud_id
        if enabled is not None:
            self.enabled = enabled
        if hidden is not None:
            self.hidden = hidden

    @property
    def id(self):
        """Gets the id of this InlineResponse2007Data.  # noqa: E501


        :return: The id of this InlineResponse2007Data.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InlineResponse2007Data.


        :param id: The id of this InlineResponse2007Data.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this InlineResponse2007Data.  # noqa: E501


        :return: The name of this InlineResponse2007Data.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse2007Data.


        :param name: The name of this InlineResponse2007Data.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def key(self):
        """Gets the key of this InlineResponse2007Data.  # noqa: E501


        :return: The key of this InlineResponse2007Data.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this InlineResponse2007Data.


        :param key: The key of this InlineResponse2007Data.  # noqa: E501
        :type: str
        """

        self._key = key

    @property
    def provider_group_id(self):
        """Gets the provider_group_id of this InlineResponse2007Data.  # noqa: E501


        :return: The provider_group_id of this InlineResponse2007Data.  # noqa: E501
        :rtype: str
        """
        return self._provider_group_id

    @provider_group_id.setter
    def provider_group_id(self, provider_group_id):
        """Sets the provider_group_id of this InlineResponse2007Data.


        :param provider_group_id: The provider_group_id of this InlineResponse2007Data.  # noqa: E501
        :type: str
        """

        self._provider_group_id = provider_group_id

    @property
    def cloud_id(self):
        """Gets the cloud_id of this InlineResponse2007Data.  # noqa: E501


        :return: The cloud_id of this InlineResponse2007Data.  # noqa: E501
        :rtype: str
        """
        return self._cloud_id

    @cloud_id.setter
    def cloud_id(self, cloud_id):
        """Sets the cloud_id of this InlineResponse2007Data.


        :param cloud_id: The cloud_id of this InlineResponse2007Data.  # noqa: E501
        :type: str
        """

        self._cloud_id = cloud_id

    @property
    def enabled(self):
        """Gets the enabled of this InlineResponse2007Data.  # noqa: E501


        :return: The enabled of this InlineResponse2007Data.  # noqa: E501
        :rtype: str
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this InlineResponse2007Data.


        :param enabled: The enabled of this InlineResponse2007Data.  # noqa: E501
        :type: str
        """

        self._enabled = enabled

    @property
    def hidden(self):
        """Gets the hidden of this InlineResponse2007Data.  # noqa: E501


        :return: The hidden of this InlineResponse2007Data.  # noqa: E501
        :rtype: str
        """
        return self._hidden

    @hidden.setter
    def hidden(self, hidden):
        """Sets the hidden of this InlineResponse2007Data.


        :param hidden: The hidden of this InlineResponse2007Data.  # noqa: E501
        :type: str
        """

        self._hidden = hidden

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
        if issubclass(InlineResponse2007Data, dict):
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
        if not isinstance(other, InlineResponse2007Data):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse2007Data):
            return True

        return self.to_dict() != other.to_dict()
