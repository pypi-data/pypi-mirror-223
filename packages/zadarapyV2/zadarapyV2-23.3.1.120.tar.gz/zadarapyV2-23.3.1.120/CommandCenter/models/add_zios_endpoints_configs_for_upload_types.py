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


class AddZiosEndpointsConfigsForUploadTypes(object):
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
        'type': 'str',
        'endpoints_config': 'list[str]'
    }

    attribute_map = {
        'type': 'type',
        'endpoints_config': 'endpoints_config'
    }

    def __init__(self, type=None, endpoints_config=None, _configuration=None):  # noqa: E501
        """AddZiosEndpointsConfigsForUploadTypes - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._type = None
        self._endpoints_config = None
        self.discriminator = None

        self.type = type
        self.endpoints_config = endpoints_config

    @property
    def type(self):
        """Gets the type of this AddZiosEndpointsConfigsForUploadTypes.  # noqa: E501

        Upload type  # noqa: E501

        :return: The type of this AddZiosEndpointsConfigsForUploadTypes.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this AddZiosEndpointsConfigsForUploadTypes.

        Upload type  # noqa: E501

        :param type: The type of this AddZiosEndpointsConfigsForUploadTypes.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["mag", "config"]  # noqa: E501
        if (self._configuration.client_side_validation and
                type not in allowed_values):
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def endpoints_config(self):
        """Gets the endpoints_config of this AddZiosEndpointsConfigsForUploadTypes.  # noqa: E501

        Endpoints configurations to be added to the existing endpoints configurations for the upload type. Each configuration must specify endpoint name. S3 endpoints configurations must also specify bucket name. Maximum 2 endpoints to add. Cloud endpoints can also be specified (see 'Get cloud settings' api).  # noqa: E501

        :return: The endpoints_config of this AddZiosEndpointsConfigsForUploadTypes.  # noqa: E501
        :rtype: list[str]
        """
        return self._endpoints_config

    @endpoints_config.setter
    def endpoints_config(self, endpoints_config):
        """Sets the endpoints_config of this AddZiosEndpointsConfigsForUploadTypes.

        Endpoints configurations to be added to the existing endpoints configurations for the upload type. Each configuration must specify endpoint name. S3 endpoints configurations must also specify bucket name. Maximum 2 endpoints to add. Cloud endpoints can also be specified (see 'Get cloud settings' api).  # noqa: E501

        :param endpoints_config: The endpoints_config of this AddZiosEndpointsConfigsForUploadTypes.  # noqa: E501
        :type: list[str]
        """
        if self._configuration.client_side_validation and endpoints_config is None:
            raise ValueError("Invalid value for `endpoints_config`, must not be `None`")  # noqa: E501

        self._endpoints_config = endpoints_config

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
        if issubclass(AddZiosEndpointsConfigsForUploadTypes, dict):
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
        if not isinstance(other, AddZiosEndpointsConfigsForUploadTypes):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AddZiosEndpointsConfigsForUploadTypes):
            return True

        return self.to_dict() != other.to_dict()
