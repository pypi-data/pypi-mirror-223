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


class GetZiosUploadEndpoints(object):
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
        'methods_requested': 'list[str]'
    }

    attribute_map = {
        'methods_requested': 'methods_requested'
    }

    def __init__(self, methods_requested=None, _configuration=None):  # noqa: E501
        """GetZiosUploadEndpoints - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._methods_requested = None
        self.discriminator = None

        if methods_requested is not None:
            self.methods_requested = methods_requested

    @property
    def methods_requested(self):
        """Gets the methods_requested of this GetZiosUploadEndpoints.  # noqa: E501

        Uploaded methods requested  # noqa: E501

        :return: The methods_requested of this GetZiosUploadEndpoints.  # noqa: E501
        :rtype: list[str]
        """
        return self._methods_requested

    @methods_requested.setter
    def methods_requested(self, methods_requested):
        """Sets the methods_requested of this GetZiosUploadEndpoints.

        Uploaded methods requested  # noqa: E501

        :param methods_requested: The methods_requested of this GetZiosUploadEndpoints.  # noqa: E501
        :type: list[str]
        """

        self._methods_requested = methods_requested

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
        if issubclass(GetZiosUploadEndpoints, dict):
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
        if not isinstance(other, GetZiosUploadEndpoints):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GetZiosUploadEndpoints):
            return True

        return self.to_dict() != other.to_dict()
