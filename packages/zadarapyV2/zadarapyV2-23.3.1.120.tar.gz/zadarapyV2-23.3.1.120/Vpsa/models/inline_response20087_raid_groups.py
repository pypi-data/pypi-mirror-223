# coding: utf-8

"""
    Zadara VPSA Storage Array REST API

     # Overview  This document outlines the methods available for administrating your Zadara Storage VPSA&#8482;. The Zadara Storage Array REST API   supports form-encoded, JSON, and XML requests, and can return either JSON or XML responses.  ## Usage  The majority of the APIs available require authentication which requires an API token to use. You can retrieve this token through the   Users section of your VPSA, or through the API using the \"Return a user's access key\" API in the Users Section below.  ## Authentication Methods  The authentication token can be passed either through the access_key parameter inside of the body of the REST API request, or   through the X-Access-Key header.  ## Timeouts  By default, all operations that don't complete within five seconds will return a message informing you that the action may take some  time to complete. When using the API, this can cause some actions, such as large volume creation, to be undesirably asynchronous.  You can specify your own timeout with the timeout parameter, in seconds, and a timeout value of -1 specifies an infinite timeout.  ## Specific Fields For Product  Some of the fields/actions used in the API should be used only for a specific product. The following tags are used to mark which   product responds to the fields/actions  VPSA Flash Array  VPSA Storage Array - Hybrid VPSA  ## Questions  If you have any questions or need support involving the REST API, please contact for assistance.   # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from Vpsa.configuration import Configuration


class InlineResponse20087RaidGroups(object):
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
        'name': 'str',
        'display_name': 'str',
        'protection': 'str',
        'mirror_num': 'int',
        'stripe_size': 'int',
        'protection_width': 'int',
        'capacity': 'int',
        'available': 'int',
        'status': 'str',
        'ssd': 'str',
        'mismatch_count': 'int',
        'resync_speed': 'int',
        'min_resync_speed': 'int',
        'max_resync_speed': 'int',
        'created_at': 'str',
        'modified_at': 'str'
    }

    attribute_map = {
        'name': 'name',
        'display_name': 'display_name',
        'protection': 'protection',
        'mirror_num': 'mirror_num',
        'stripe_size': 'stripe_size',
        'protection_width': 'protection_width',
        'capacity': 'capacity',
        'available': 'available',
        'status': 'status',
        'ssd': 'ssd',
        'mismatch_count': 'mismatch_count',
        'resync_speed': 'resync_speed',
        'min_resync_speed': 'min_resync_speed',
        'max_resync_speed': 'max_resync_speed',
        'created_at': 'created_at',
        'modified_at': 'modified_at'
    }

    def __init__(self, name=None, display_name=None, protection=None, mirror_num=None, stripe_size=None, protection_width=None, capacity=None, available=None, status=None, ssd=None, mismatch_count=None, resync_speed=None, min_resync_speed=None, max_resync_speed=None, created_at=None, modified_at=None, _configuration=None):  # noqa: E501
        """InlineResponse20087RaidGroups - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._display_name = None
        self._protection = None
        self._mirror_num = None
        self._stripe_size = None
        self._protection_width = None
        self._capacity = None
        self._available = None
        self._status = None
        self._ssd = None
        self._mismatch_count = None
        self._resync_speed = None
        self._min_resync_speed = None
        self._max_resync_speed = None
        self._created_at = None
        self._modified_at = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if display_name is not None:
            self.display_name = display_name
        if protection is not None:
            self.protection = protection
        if mirror_num is not None:
            self.mirror_num = mirror_num
        if stripe_size is not None:
            self.stripe_size = stripe_size
        if protection_width is not None:
            self.protection_width = protection_width
        if capacity is not None:
            self.capacity = capacity
        if available is not None:
            self.available = available
        if status is not None:
            self.status = status
        if ssd is not None:
            self.ssd = ssd
        if mismatch_count is not None:
            self.mismatch_count = mismatch_count
        if resync_speed is not None:
            self.resync_speed = resync_speed
        if min_resync_speed is not None:
            self.min_resync_speed = min_resync_speed
        if max_resync_speed is not None:
            self.max_resync_speed = max_resync_speed
        if created_at is not None:
            self.created_at = created_at
        if modified_at is not None:
            self.modified_at = modified_at

    @property
    def name(self):
        """Gets the name of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The name of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse20087RaidGroups.


        :param name: The name of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def display_name(self):
        """Gets the display_name of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The display_name of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this InlineResponse20087RaidGroups.


        :param display_name: The display_name of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def protection(self):
        """Gets the protection of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The protection of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: str
        """
        return self._protection

    @protection.setter
    def protection(self, protection):
        """Sets the protection of this InlineResponse20087RaidGroups.


        :param protection: The protection of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: str
        """

        self._protection = protection

    @property
    def mirror_num(self):
        """Gets the mirror_num of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The mirror_num of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: int
        """
        return self._mirror_num

    @mirror_num.setter
    def mirror_num(self, mirror_num):
        """Sets the mirror_num of this InlineResponse20087RaidGroups.


        :param mirror_num: The mirror_num of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: int
        """

        self._mirror_num = mirror_num

    @property
    def stripe_size(self):
        """Gets the stripe_size of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The stripe_size of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: int
        """
        return self._stripe_size

    @stripe_size.setter
    def stripe_size(self, stripe_size):
        """Sets the stripe_size of this InlineResponse20087RaidGroups.


        :param stripe_size: The stripe_size of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: int
        """

        self._stripe_size = stripe_size

    @property
    def protection_width(self):
        """Gets the protection_width of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The protection_width of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: int
        """
        return self._protection_width

    @protection_width.setter
    def protection_width(self, protection_width):
        """Sets the protection_width of this InlineResponse20087RaidGroups.


        :param protection_width: The protection_width of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: int
        """

        self._protection_width = protection_width

    @property
    def capacity(self):
        """Gets the capacity of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The capacity of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: int
        """
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        """Sets the capacity of this InlineResponse20087RaidGroups.


        :param capacity: The capacity of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: int
        """

        self._capacity = capacity

    @property
    def available(self):
        """Gets the available of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The available of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: int
        """
        return self._available

    @available.setter
    def available(self, available):
        """Sets the available of this InlineResponse20087RaidGroups.


        :param available: The available of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: int
        """

        self._available = available

    @property
    def status(self):
        """Gets the status of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The status of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InlineResponse20087RaidGroups.


        :param status: The status of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def ssd(self):
        """Gets the ssd of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The ssd of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: str
        """
        return self._ssd

    @ssd.setter
    def ssd(self, ssd):
        """Sets the ssd of this InlineResponse20087RaidGroups.


        :param ssd: The ssd of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: str
        """

        self._ssd = ssd

    @property
    def mismatch_count(self):
        """Gets the mismatch_count of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The mismatch_count of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: int
        """
        return self._mismatch_count

    @mismatch_count.setter
    def mismatch_count(self, mismatch_count):
        """Sets the mismatch_count of this InlineResponse20087RaidGroups.


        :param mismatch_count: The mismatch_count of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: int
        """

        self._mismatch_count = mismatch_count

    @property
    def resync_speed(self):
        """Gets the resync_speed of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The resync_speed of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: int
        """
        return self._resync_speed

    @resync_speed.setter
    def resync_speed(self, resync_speed):
        """Sets the resync_speed of this InlineResponse20087RaidGroups.


        :param resync_speed: The resync_speed of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: int
        """

        self._resync_speed = resync_speed

    @property
    def min_resync_speed(self):
        """Gets the min_resync_speed of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The min_resync_speed of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: int
        """
        return self._min_resync_speed

    @min_resync_speed.setter
    def min_resync_speed(self, min_resync_speed):
        """Sets the min_resync_speed of this InlineResponse20087RaidGroups.


        :param min_resync_speed: The min_resync_speed of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: int
        """

        self._min_resync_speed = min_resync_speed

    @property
    def max_resync_speed(self):
        """Gets the max_resync_speed of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The max_resync_speed of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: int
        """
        return self._max_resync_speed

    @max_resync_speed.setter
    def max_resync_speed(self, max_resync_speed):
        """Sets the max_resync_speed of this InlineResponse20087RaidGroups.


        :param max_resync_speed: The max_resync_speed of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: int
        """

        self._max_resync_speed = max_resync_speed

    @property
    def created_at(self):
        """Gets the created_at of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The created_at of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InlineResponse20087RaidGroups.


        :param created_at: The created_at of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def modified_at(self):
        """Gets the modified_at of this InlineResponse20087RaidGroups.  # noqa: E501


        :return: The modified_at of this InlineResponse20087RaidGroups.  # noqa: E501
        :rtype: str
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this InlineResponse20087RaidGroups.


        :param modified_at: The modified_at of this InlineResponse20087RaidGroups.  # noqa: E501
        :type: str
        """

        self._modified_at = modified_at

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
        if issubclass(InlineResponse20087RaidGroups, dict):
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
        if not isinstance(other, InlineResponse20087RaidGroups):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20087RaidGroups):
            return True

        return self.to_dict() != other.to_dict()
