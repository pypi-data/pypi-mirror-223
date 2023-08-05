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


class InlineResponse200228ResponseServers(object):
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
        'iqn': 'str',
        'iscsi_ip': 'str',
        'ipsec': 'str',
        'status': 'str',
        'os': 'str',
        'registered': 'str',
        'created_at': 'str',
        'modified_at': 'str',
        'pm_status': 'str',
        'target': 'str',
        'access_type': 'str',
        'read_only': 'str',
        'lun': 'str'
    }

    attribute_map = {
        'name': 'name',
        'display_name': 'display_name',
        'iqn': 'iqn',
        'iscsi_ip': 'iscsi_ip',
        'ipsec': 'ipsec',
        'status': 'status',
        'os': 'os',
        'registered': 'registered',
        'created_at': 'created_at',
        'modified_at': 'modified_at',
        'pm_status': 'pm_status',
        'target': 'target',
        'access_type': 'access_type',
        'read_only': 'read_only',
        'lun': 'lun'
    }

    def __init__(self, name=None, display_name=None, iqn=None, iscsi_ip=None, ipsec=None, status=None, os=None, registered=None, created_at=None, modified_at=None, pm_status=None, target=None, access_type=None, read_only=None, lun=None, _configuration=None):  # noqa: E501
        """InlineResponse200228ResponseServers - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._display_name = None
        self._iqn = None
        self._iscsi_ip = None
        self._ipsec = None
        self._status = None
        self._os = None
        self._registered = None
        self._created_at = None
        self._modified_at = None
        self._pm_status = None
        self._target = None
        self._access_type = None
        self._read_only = None
        self._lun = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if display_name is not None:
            self.display_name = display_name
        if iqn is not None:
            self.iqn = iqn
        if iscsi_ip is not None:
            self.iscsi_ip = iscsi_ip
        if ipsec is not None:
            self.ipsec = ipsec
        if status is not None:
            self.status = status
        if os is not None:
            self.os = os
        if registered is not None:
            self.registered = registered
        if created_at is not None:
            self.created_at = created_at
        if modified_at is not None:
            self.modified_at = modified_at
        if pm_status is not None:
            self.pm_status = pm_status
        if target is not None:
            self.target = target
        if access_type is not None:
            self.access_type = access_type
        if read_only is not None:
            self.read_only = read_only
        if lun is not None:
            self.lun = lun

    @property
    def name(self):
        """Gets the name of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The name of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse200228ResponseServers.


        :param name: The name of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def display_name(self):
        """Gets the display_name of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The display_name of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this InlineResponse200228ResponseServers.


        :param display_name: The display_name of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def iqn(self):
        """Gets the iqn of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The iqn of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._iqn

    @iqn.setter
    def iqn(self, iqn):
        """Sets the iqn of this InlineResponse200228ResponseServers.


        :param iqn: The iqn of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._iqn = iqn

    @property
    def iscsi_ip(self):
        """Gets the iscsi_ip of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The iscsi_ip of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._iscsi_ip

    @iscsi_ip.setter
    def iscsi_ip(self, iscsi_ip):
        """Sets the iscsi_ip of this InlineResponse200228ResponseServers.


        :param iscsi_ip: The iscsi_ip of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._iscsi_ip = iscsi_ip

    @property
    def ipsec(self):
        """Gets the ipsec of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The ipsec of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._ipsec

    @ipsec.setter
    def ipsec(self, ipsec):
        """Sets the ipsec of this InlineResponse200228ResponseServers.


        :param ipsec: The ipsec of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._ipsec = ipsec

    @property
    def status(self):
        """Gets the status of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The status of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InlineResponse200228ResponseServers.


        :param status: The status of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def os(self):
        """Gets the os of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The os of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._os

    @os.setter
    def os(self, os):
        """Sets the os of this InlineResponse200228ResponseServers.


        :param os: The os of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._os = os

    @property
    def registered(self):
        """Gets the registered of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The registered of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._registered

    @registered.setter
    def registered(self, registered):
        """Sets the registered of this InlineResponse200228ResponseServers.


        :param registered: The registered of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._registered = registered

    @property
    def created_at(self):
        """Gets the created_at of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The created_at of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InlineResponse200228ResponseServers.


        :param created_at: The created_at of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def modified_at(self):
        """Gets the modified_at of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The modified_at of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this InlineResponse200228ResponseServers.


        :param modified_at: The modified_at of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._modified_at = modified_at

    @property
    def pm_status(self):
        """Gets the pm_status of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The pm_status of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._pm_status

    @pm_status.setter
    def pm_status(self, pm_status):
        """Sets the pm_status of this InlineResponse200228ResponseServers.


        :param pm_status: The pm_status of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._pm_status = pm_status

    @property
    def target(self):
        """Gets the target of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The target of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """Sets the target of this InlineResponse200228ResponseServers.


        :param target: The target of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._target = target

    @property
    def access_type(self):
        """Gets the access_type of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The access_type of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._access_type

    @access_type.setter
    def access_type(self, access_type):
        """Sets the access_type of this InlineResponse200228ResponseServers.


        :param access_type: The access_type of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._access_type = access_type

    @property
    def read_only(self):
        """Gets the read_only of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The read_only of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._read_only

    @read_only.setter
    def read_only(self, read_only):
        """Sets the read_only of this InlineResponse200228ResponseServers.


        :param read_only: The read_only of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._read_only = read_only

    @property
    def lun(self):
        """Gets the lun of this InlineResponse200228ResponseServers.  # noqa: E501


        :return: The lun of this InlineResponse200228ResponseServers.  # noqa: E501
        :rtype: str
        """
        return self._lun

    @lun.setter
    def lun(self, lun):
        """Sets the lun of this InlineResponse200228ResponseServers.


        :param lun: The lun of this InlineResponse200228ResponseServers.  # noqa: E501
        :type: str
        """

        self._lun = lun

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
        if issubclass(InlineResponse200228ResponseServers, dict):
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
        if not isinstance(other, InlineResponse200228ResponseServers):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse200228ResponseServers):
            return True

        return self.to_dict() != other.to_dict()
