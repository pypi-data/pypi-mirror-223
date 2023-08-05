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


class InlineResponse20038InformationMrInfoAdpInfo(object):
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
        'adp_no': 'str',
        'product_name': 'str',
        'target_fw_ver': 'str',
        'upgrade_recommended': 'str',
        'cur_fw_ver': 'str'
    }

    attribute_map = {
        'adp_no': 'adp_no',
        'product_name': 'product_name',
        'target_fw_ver': 'target_fw_ver',
        'upgrade_recommended': 'upgrade_recommended',
        'cur_fw_ver': 'cur_fw_ver'
    }

    def __init__(self, adp_no=None, product_name=None, target_fw_ver=None, upgrade_recommended=None, cur_fw_ver=None, _configuration=None):  # noqa: E501
        """InlineResponse20038InformationMrInfoAdpInfo - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._adp_no = None
        self._product_name = None
        self._target_fw_ver = None
        self._upgrade_recommended = None
        self._cur_fw_ver = None
        self.discriminator = None

        if adp_no is not None:
            self.adp_no = adp_no
        if product_name is not None:
            self.product_name = product_name
        if target_fw_ver is not None:
            self.target_fw_ver = target_fw_ver
        if upgrade_recommended is not None:
            self.upgrade_recommended = upgrade_recommended
        if cur_fw_ver is not None:
            self.cur_fw_ver = cur_fw_ver

    @property
    def adp_no(self):
        """Gets the adp_no of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501


        :return: The adp_no of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501
        :rtype: str
        """
        return self._adp_no

    @adp_no.setter
    def adp_no(self, adp_no):
        """Sets the adp_no of this InlineResponse20038InformationMrInfoAdpInfo.


        :param adp_no: The adp_no of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501
        :type: str
        """

        self._adp_no = adp_no

    @property
    def product_name(self):
        """Gets the product_name of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501


        :return: The product_name of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501
        :rtype: str
        """
        return self._product_name

    @product_name.setter
    def product_name(self, product_name):
        """Sets the product_name of this InlineResponse20038InformationMrInfoAdpInfo.


        :param product_name: The product_name of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501
        :type: str
        """

        self._product_name = product_name

    @property
    def target_fw_ver(self):
        """Gets the target_fw_ver of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501


        :return: The target_fw_ver of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501
        :rtype: str
        """
        return self._target_fw_ver

    @target_fw_ver.setter
    def target_fw_ver(self, target_fw_ver):
        """Sets the target_fw_ver of this InlineResponse20038InformationMrInfoAdpInfo.


        :param target_fw_ver: The target_fw_ver of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501
        :type: str
        """

        self._target_fw_ver = target_fw_ver

    @property
    def upgrade_recommended(self):
        """Gets the upgrade_recommended of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501


        :return: The upgrade_recommended of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501
        :rtype: str
        """
        return self._upgrade_recommended

    @upgrade_recommended.setter
    def upgrade_recommended(self, upgrade_recommended):
        """Sets the upgrade_recommended of this InlineResponse20038InformationMrInfoAdpInfo.


        :param upgrade_recommended: The upgrade_recommended of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501
        :type: str
        """

        self._upgrade_recommended = upgrade_recommended

    @property
    def cur_fw_ver(self):
        """Gets the cur_fw_ver of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501


        :return: The cur_fw_ver of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501
        :rtype: str
        """
        return self._cur_fw_ver

    @cur_fw_ver.setter
    def cur_fw_ver(self, cur_fw_ver):
        """Sets the cur_fw_ver of this InlineResponse20038InformationMrInfoAdpInfo.


        :param cur_fw_ver: The cur_fw_ver of this InlineResponse20038InformationMrInfoAdpInfo.  # noqa: E501
        :type: str
        """

        self._cur_fw_ver = cur_fw_ver

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
        if issubclass(InlineResponse20038InformationMrInfoAdpInfo, dict):
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
        if not isinstance(other, InlineResponse20038InformationMrInfoAdpInfo):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20038InformationMrInfoAdpInfo):
            return True

        return self.to_dict() != other.to_dict()
