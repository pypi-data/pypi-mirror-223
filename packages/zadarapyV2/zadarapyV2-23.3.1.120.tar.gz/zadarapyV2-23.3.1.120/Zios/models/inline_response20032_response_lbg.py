# coding: utf-8

"""
    Zadara VPSA Object Storage REST API

    # Overview  This document outlines the methods available for administrating your VPSA&#174; Object Storage. The API supports form-encoded, JSON, and XML requests, and can return either JSON or XML responses.  ## Usage  The majority of the APIs available require authentication which requires an API token to use. You can retrieve this token through the Users section of your VPSA, or through the API using the \"Return a user's access key\" API in the Users Section below.  ## Authentication Methods  The authentication token can be passed either through the access_key parameter inside of the body of the REST API request, or through the X-Access-Key header. Alternately, you can use the username and password parameters for authentication, but we do not recommend this method for anything other than possibly retrieving an API key.  By default , all operations are allowed only to VPSA Object Storage admin. Some actions are allowed by an account admin and they will be marked on the action's header  ## Timeouts  By default, all operations that don't complete within five seconds will return a message informing you that the action may take some time to complete. When using the API, this can cause some actions, such as adding drives to storage policy, to be undesirably asynchronous. You can specify your own timeout with the timeout parameter, in seconds, and a timeout value of -1 specifies an infinite timeout.  ## Metering API  Metering information can be retrieved using the VPSA Object Storage API for the following components:  - Accounts - Users - Drives - Virtual Controllers - Load Balancer Groups - Storage Policies  Metering information returned by the API is subject to the following constraints:  - 10 seconds interval - 1 hour range - 1 minute interval - 1 day range - 1 hour interval - 30 days range  Values outside the accepted range will be returned as 0.  ## Questions  If you have any questions or need support involving the REST API, please contact for assistance.   # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from Zios.configuration import Configuration


class InlineResponse20032ResponseLbg(object):
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
        'vrid': 'int',
        'ip_v4': 'str',
        'ip_v6': 'str',
        'region_id': 'int',
        'allocation_zone': 'str',
        'allocation_zone_display_name': 'str',
        'vcs': 'str',
        'master_vc': 'str',
        'created_at': 'str',
        'modified_at': 'str'
    }

    attribute_map = {
        'name': 'name',
        'vrid': 'vrid',
        'ip_v4': 'ip_v4',
        'ip_v6': 'ip_v6',
        'region_id': 'region_id',
        'allocation_zone': 'allocation-zone',
        'allocation_zone_display_name': 'allocation-zone_display_name',
        'vcs': 'vcs',
        'master_vc': 'master_vc',
        'created_at': 'created_at',
        'modified_at': 'modified_at'
    }

    def __init__(self, name=None, vrid=None, ip_v4=None, ip_v6=None, region_id=None, allocation_zone=None, allocation_zone_display_name=None, vcs=None, master_vc=None, created_at=None, modified_at=None, _configuration=None):  # noqa: E501
        """InlineResponse20032ResponseLbg - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._vrid = None
        self._ip_v4 = None
        self._ip_v6 = None
        self._region_id = None
        self._allocation_zone = None
        self._allocation_zone_display_name = None
        self._vcs = None
        self._master_vc = None
        self._created_at = None
        self._modified_at = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if vrid is not None:
            self.vrid = vrid
        if ip_v4 is not None:
            self.ip_v4 = ip_v4
        if ip_v6 is not None:
            self.ip_v6 = ip_v6
        if region_id is not None:
            self.region_id = region_id
        if allocation_zone is not None:
            self.allocation_zone = allocation_zone
        if allocation_zone_display_name is not None:
            self.allocation_zone_display_name = allocation_zone_display_name
        if vcs is not None:
            self.vcs = vcs
        if master_vc is not None:
            self.master_vc = master_vc
        if created_at is not None:
            self.created_at = created_at
        if modified_at is not None:
            self.modified_at = modified_at

    @property
    def name(self):
        """Gets the name of this InlineResponse20032ResponseLbg.  # noqa: E501


        :return: The name of this InlineResponse20032ResponseLbg.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse20032ResponseLbg.


        :param name: The name of this InlineResponse20032ResponseLbg.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def vrid(self):
        """Gets the vrid of this InlineResponse20032ResponseLbg.  # noqa: E501


        :return: The vrid of this InlineResponse20032ResponseLbg.  # noqa: E501
        :rtype: int
        """
        return self._vrid

    @vrid.setter
    def vrid(self, vrid):
        """Sets the vrid of this InlineResponse20032ResponseLbg.


        :param vrid: The vrid of this InlineResponse20032ResponseLbg.  # noqa: E501
        :type: int
        """

        self._vrid = vrid

    @property
    def ip_v4(self):
        """Gets the ip_v4 of this InlineResponse20032ResponseLbg.  # noqa: E501


        :return: The ip_v4 of this InlineResponse20032ResponseLbg.  # noqa: E501
        :rtype: str
        """
        return self._ip_v4

    @ip_v4.setter
    def ip_v4(self, ip_v4):
        """Sets the ip_v4 of this InlineResponse20032ResponseLbg.


        :param ip_v4: The ip_v4 of this InlineResponse20032ResponseLbg.  # noqa: E501
        :type: str
        """

        self._ip_v4 = ip_v4

    @property
    def ip_v6(self):
        """Gets the ip_v6 of this InlineResponse20032ResponseLbg.  # noqa: E501


        :return: The ip_v6 of this InlineResponse20032ResponseLbg.  # noqa: E501
        :rtype: str
        """
        return self._ip_v6

    @ip_v6.setter
    def ip_v6(self, ip_v6):
        """Sets the ip_v6 of this InlineResponse20032ResponseLbg.


        :param ip_v6: The ip_v6 of this InlineResponse20032ResponseLbg.  # noqa: E501
        :type: str
        """

        self._ip_v6 = ip_v6

    @property
    def region_id(self):
        """Gets the region_id of this InlineResponse20032ResponseLbg.  # noqa: E501


        :return: The region_id of this InlineResponse20032ResponseLbg.  # noqa: E501
        :rtype: int
        """
        return self._region_id

    @region_id.setter
    def region_id(self, region_id):
        """Sets the region_id of this InlineResponse20032ResponseLbg.


        :param region_id: The region_id of this InlineResponse20032ResponseLbg.  # noqa: E501
        :type: int
        """

        self._region_id = region_id

    @property
    def allocation_zone(self):
        """Gets the allocation_zone of this InlineResponse20032ResponseLbg.  # noqa: E501


        :return: The allocation_zone of this InlineResponse20032ResponseLbg.  # noqa: E501
        :rtype: str
        """
        return self._allocation_zone

    @allocation_zone.setter
    def allocation_zone(self, allocation_zone):
        """Sets the allocation_zone of this InlineResponse20032ResponseLbg.


        :param allocation_zone: The allocation_zone of this InlineResponse20032ResponseLbg.  # noqa: E501
        :type: str
        """

        self._allocation_zone = allocation_zone

    @property
    def allocation_zone_display_name(self):
        """Gets the allocation_zone_display_name of this InlineResponse20032ResponseLbg.  # noqa: E501


        :return: The allocation_zone_display_name of this InlineResponse20032ResponseLbg.  # noqa: E501
        :rtype: str
        """
        return self._allocation_zone_display_name

    @allocation_zone_display_name.setter
    def allocation_zone_display_name(self, allocation_zone_display_name):
        """Sets the allocation_zone_display_name of this InlineResponse20032ResponseLbg.


        :param allocation_zone_display_name: The allocation_zone_display_name of this InlineResponse20032ResponseLbg.  # noqa: E501
        :type: str
        """

        self._allocation_zone_display_name = allocation_zone_display_name

    @property
    def vcs(self):
        """Gets the vcs of this InlineResponse20032ResponseLbg.  # noqa: E501


        :return: The vcs of this InlineResponse20032ResponseLbg.  # noqa: E501
        :rtype: str
        """
        return self._vcs

    @vcs.setter
    def vcs(self, vcs):
        """Sets the vcs of this InlineResponse20032ResponseLbg.


        :param vcs: The vcs of this InlineResponse20032ResponseLbg.  # noqa: E501
        :type: str
        """

        self._vcs = vcs

    @property
    def master_vc(self):
        """Gets the master_vc of this InlineResponse20032ResponseLbg.  # noqa: E501


        :return: The master_vc of this InlineResponse20032ResponseLbg.  # noqa: E501
        :rtype: str
        """
        return self._master_vc

    @master_vc.setter
    def master_vc(self, master_vc):
        """Sets the master_vc of this InlineResponse20032ResponseLbg.


        :param master_vc: The master_vc of this InlineResponse20032ResponseLbg.  # noqa: E501
        :type: str
        """

        self._master_vc = master_vc

    @property
    def created_at(self):
        """Gets the created_at of this InlineResponse20032ResponseLbg.  # noqa: E501


        :return: The created_at of this InlineResponse20032ResponseLbg.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InlineResponse20032ResponseLbg.


        :param created_at: The created_at of this InlineResponse20032ResponseLbg.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def modified_at(self):
        """Gets the modified_at of this InlineResponse20032ResponseLbg.  # noqa: E501


        :return: The modified_at of this InlineResponse20032ResponseLbg.  # noqa: E501
        :rtype: str
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this InlineResponse20032ResponseLbg.


        :param modified_at: The modified_at of this InlineResponse20032ResponseLbg.  # noqa: E501
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
        if issubclass(InlineResponse20032ResponseLbg, dict):
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
        if not isinstance(other, InlineResponse20032ResponseLbg):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20032ResponseLbg):
            return True

        return self.to_dict() != other.to_dict()
