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


class EvacoateVcFromSn(object):
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
        'force': 'bool'
    }

    attribute_map = {
        'force': 'force'
    }

    def __init__(self, force=None, _configuration=None):  # noqa: E501
        """EvacoateVcFromSn - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._force = None
        self.discriminator = None

        if force is not None:
            self.force = force

    @property
    def force(self):
        """Gets the force of this EvacoateVcFromSn.  # noqa: E501

        In case the Storage Node that hosts the VC is offline and marked for decommission, use the force flag to allow the VC relocation.  # noqa: E501

        :return: The force of this EvacoateVcFromSn.  # noqa: E501
        :rtype: bool
        """
        return self._force

    @force.setter
    def force(self, force):
        """Sets the force of this EvacoateVcFromSn.

        In case the Storage Node that hosts the VC is offline and marked for decommission, use the force flag to allow the VC relocation.  # noqa: E501

        :param force: The force of this EvacoateVcFromSn.  # noqa: E501
        :type: bool
        """

        self._force = force

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
        if issubclass(EvacoateVcFromSn, dict):
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
        if not isinstance(other, EvacoateVcFromSn):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, EvacoateVcFromSn):
            return True

        return self.to_dict() != other.to_dict()
