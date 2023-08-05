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


class SetRemoteRegionBackendProtocol1(object):
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
        'threshold': 'int'
    }

    attribute_map = {
        'threshold': 'threshold'
    }

    def __init__(self, threshold=None, _configuration=None):  # noqa: E501
        """SetRemoteRegionBackendProtocol1 - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._threshold = None
        self.discriminator = None

        self.threshold = threshold

    @property
    def threshold(self):
        """Gets the threshold of this SetRemoteRegionBackendProtocol1.  # noqa: E501


        :return: The threshold of this SetRemoteRegionBackendProtocol1.  # noqa: E501
        :rtype: int
        """
        return self._threshold

    @threshold.setter
    def threshold(self, threshold):
        """Sets the threshold of this SetRemoteRegionBackendProtocol1.


        :param threshold: The threshold of this SetRemoteRegionBackendProtocol1.  # noqa: E501
        :type: int
        """
        if self._configuration.client_side_validation and threshold is None:
            raise ValueError("Invalid value for `threshold`, must not be `None`")  # noqa: E501

        self._threshold = threshold

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
        if issubclass(SetRemoteRegionBackendProtocol1, dict):
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
        if not isinstance(other, SetRemoteRegionBackendProtocol1):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SetRemoteRegionBackendProtocol1):
            return True

        return self.to_dict() != other.to_dict()
