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


class InlineResponse20097RaidGroups(object):
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
        'raid_group': 'InlineResponse20097RaidGroupsRaidGroup'
    }

    attribute_map = {
        'raid_group': 'raid_group'
    }

    def __init__(self, raid_group=None, _configuration=None):  # noqa: E501
        """InlineResponse20097RaidGroups - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._raid_group = None
        self.discriminator = None

        if raid_group is not None:
            self.raid_group = raid_group

    @property
    def raid_group(self):
        """Gets the raid_group of this InlineResponse20097RaidGroups.  # noqa: E501


        :return: The raid_group of this InlineResponse20097RaidGroups.  # noqa: E501
        :rtype: InlineResponse20097RaidGroupsRaidGroup
        """
        return self._raid_group

    @raid_group.setter
    def raid_group(self, raid_group):
        """Sets the raid_group of this InlineResponse20097RaidGroups.


        :param raid_group: The raid_group of this InlineResponse20097RaidGroups.  # noqa: E501
        :type: InlineResponse20097RaidGroupsRaidGroup
        """

        self._raid_group = raid_group

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
        if issubclass(InlineResponse20097RaidGroups, dict):
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
        if not isinstance(other, InlineResponse20097RaidGroups):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20097RaidGroups):
            return True

        return self.to_dict() != other.to_dict()
