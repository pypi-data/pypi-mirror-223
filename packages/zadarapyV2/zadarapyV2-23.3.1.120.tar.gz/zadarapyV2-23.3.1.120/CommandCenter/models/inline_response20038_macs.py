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


class InlineResponse20038Macs(object):
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
        'febond': 'str',
        'extmgmt': 'str',
        'bebond': 'str',
        'novabridge': 'str'
    }

    attribute_map = {
        'febond': 'febond',
        'extmgmt': 'extmgmt',
        'bebond': 'bebond',
        'novabridge': 'novabridge'
    }

    def __init__(self, febond=None, extmgmt=None, bebond=None, novabridge=None, _configuration=None):  # noqa: E501
        """InlineResponse20038Macs - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._febond = None
        self._extmgmt = None
        self._bebond = None
        self._novabridge = None
        self.discriminator = None

        if febond is not None:
            self.febond = febond
        if extmgmt is not None:
            self.extmgmt = extmgmt
        if bebond is not None:
            self.bebond = bebond
        if novabridge is not None:
            self.novabridge = novabridge

    @property
    def febond(self):
        """Gets the febond of this InlineResponse20038Macs.  # noqa: E501


        :return: The febond of this InlineResponse20038Macs.  # noqa: E501
        :rtype: str
        """
        return self._febond

    @febond.setter
    def febond(self, febond):
        """Sets the febond of this InlineResponse20038Macs.


        :param febond: The febond of this InlineResponse20038Macs.  # noqa: E501
        :type: str
        """

        self._febond = febond

    @property
    def extmgmt(self):
        """Gets the extmgmt of this InlineResponse20038Macs.  # noqa: E501


        :return: The extmgmt of this InlineResponse20038Macs.  # noqa: E501
        :rtype: str
        """
        return self._extmgmt

    @extmgmt.setter
    def extmgmt(self, extmgmt):
        """Sets the extmgmt of this InlineResponse20038Macs.


        :param extmgmt: The extmgmt of this InlineResponse20038Macs.  # noqa: E501
        :type: str
        """

        self._extmgmt = extmgmt

    @property
    def bebond(self):
        """Gets the bebond of this InlineResponse20038Macs.  # noqa: E501


        :return: The bebond of this InlineResponse20038Macs.  # noqa: E501
        :rtype: str
        """
        return self._bebond

    @bebond.setter
    def bebond(self, bebond):
        """Sets the bebond of this InlineResponse20038Macs.


        :param bebond: The bebond of this InlineResponse20038Macs.  # noqa: E501
        :type: str
        """

        self._bebond = bebond

    @property
    def novabridge(self):
        """Gets the novabridge of this InlineResponse20038Macs.  # noqa: E501


        :return: The novabridge of this InlineResponse20038Macs.  # noqa: E501
        :rtype: str
        """
        return self._novabridge

    @novabridge.setter
    def novabridge(self, novabridge):
        """Sets the novabridge of this InlineResponse20038Macs.


        :param novabridge: The novabridge of this InlineResponse20038Macs.  # noqa: E501
        :type: str
        """

        self._novabridge = novabridge

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
        if issubclass(InlineResponse20038Macs, dict):
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
        if not isinstance(other, InlineResponse20038Macs):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20038Macs):
            return True

        return self.to_dict() != other.to_dict()
