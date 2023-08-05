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


class InlineResponse20080Message(object):
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
        'actions': 'list[InlineResponse20080MessageActions]'
    }

    attribute_map = {
        'actions': 'actions'
    }

    def __init__(self, actions=None, _configuration=None):  # noqa: E501
        """InlineResponse20080Message - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._actions = None
        self.discriminator = None

        if actions is not None:
            self.actions = actions

    @property
    def actions(self):
        """Gets the actions of this InlineResponse20080Message.  # noqa: E501


        :return: The actions of this InlineResponse20080Message.  # noqa: E501
        :rtype: list[InlineResponse20080MessageActions]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """Sets the actions of this InlineResponse20080Message.


        :param actions: The actions of this InlineResponse20080Message.  # noqa: E501
        :type: list[InlineResponse20080MessageActions]
        """

        self._actions = actions

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
        if issubclass(InlineResponse20080Message, dict):
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
        if not isinstance(other, InlineResponse20080Message):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20080Message):
            return True

        return self.to_dict() != other.to_dict()
