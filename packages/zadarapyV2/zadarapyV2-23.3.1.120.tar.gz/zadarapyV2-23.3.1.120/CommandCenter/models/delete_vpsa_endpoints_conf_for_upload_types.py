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


class DeleteVpsaEndpointsConfForUploadTypes(object):
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
        'endpoint_name': 'str'
    }

    attribute_map = {
        'type': 'type',
        'endpoint_name': 'endpoint_name'
    }

    def __init__(self, type=None, endpoint_name=None, _configuration=None):  # noqa: E501
        """DeleteVpsaEndpointsConfForUploadTypes - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._type = None
        self._endpoint_name = None
        self.discriminator = None

        self.type = type
        self.endpoint_name = endpoint_name

    @property
    def type(self):
        """Gets the type of this DeleteVpsaEndpointsConfForUploadTypes.  # noqa: E501

        Upload type  # noqa: E501

        :return: The type of this DeleteVpsaEndpointsConfForUploadTypes.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this DeleteVpsaEndpointsConfForUploadTypes.

        Upload type  # noqa: E501

        :param type: The type of this DeleteVpsaEndpointsConfForUploadTypes.  # noqa: E501
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
    def endpoint_name(self):
        """Gets the endpoint_name of this DeleteVpsaEndpointsConfForUploadTypes.  # noqa: E501

        Endpoint name  # noqa: E501

        :return: The endpoint_name of this DeleteVpsaEndpointsConfForUploadTypes.  # noqa: E501
        :rtype: str
        """
        return self._endpoint_name

    @endpoint_name.setter
    def endpoint_name(self, endpoint_name):
        """Sets the endpoint_name of this DeleteVpsaEndpointsConfForUploadTypes.

        Endpoint name  # noqa: E501

        :param endpoint_name: The endpoint_name of this DeleteVpsaEndpointsConfForUploadTypes.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and endpoint_name is None:
            raise ValueError("Invalid value for `endpoint_name`, must not be `None`")  # noqa: E501

        self._endpoint_name = endpoint_name

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
        if issubclass(DeleteVpsaEndpointsConfForUploadTypes, dict):
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
        if not isinstance(other, DeleteVpsaEndpointsConfForUploadTypes):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DeleteVpsaEndpointsConfForUploadTypes):
            return True

        return self.to_dict() != other.to_dict()
