# coding: utf-8

"""
    Zadara Provisioning Portal API

     # Overview  This document outlines the methods available for creation and high-level administration of Zadara Storage VPSAs via a Zadara Storage Provisioning Portal. This API supports form-encoded requests, and can return either JSON or XML responses.  ## Endpoint  The base URL for the requests is the Provisioning Portal URL you created your VPSA through - for example: https://manage.zadarastorage.com/, and all APIs will be prefixed with /api as noted in the documentation below.  ## Authentication  To use this API, an authentication token is required. The API for retrieving this token can be found below in the Authentication section. You may pass this token in requests either via the the X-Token header or via basic authentication (base64 encoded) in Authorization header.  ## Questions  If you have any questions or need support involving the REST API, please contact for assistance.   # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from ProvisioningPortal.configuration import Configuration


class InlineResponse20024DataPubliczios(object):
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
        'id': 'int',
        'vpsa_id': 'int',
        'account_name': 'str',
        'username': 'str',
        'ip': 'str',
        'host': 'str',
        'auto_approve': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'vpsa_id': 'vpsa_id',
        'account_name': 'account_name',
        'username': 'username',
        'ip': 'ip',
        'host': 'host',
        'auto_approve': 'auto_approve'
    }

    def __init__(self, id=None, vpsa_id=None, account_name=None, username=None, ip=None, host=None, auto_approve=None, _configuration=None):  # noqa: E501
        """InlineResponse20024DataPubliczios - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._id = None
        self._vpsa_id = None
        self._account_name = None
        self._username = None
        self._ip = None
        self._host = None
        self._auto_approve = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if vpsa_id is not None:
            self.vpsa_id = vpsa_id
        if account_name is not None:
            self.account_name = account_name
        if username is not None:
            self.username = username
        if ip is not None:
            self.ip = ip
        if host is not None:
            self.host = host
        if auto_approve is not None:
            self.auto_approve = auto_approve

    @property
    def id(self):
        """Gets the id of this InlineResponse20024DataPubliczios.  # noqa: E501


        :return: The id of this InlineResponse20024DataPubliczios.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InlineResponse20024DataPubliczios.


        :param id: The id of this InlineResponse20024DataPubliczios.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def vpsa_id(self):
        """Gets the vpsa_id of this InlineResponse20024DataPubliczios.  # noqa: E501


        :return: The vpsa_id of this InlineResponse20024DataPubliczios.  # noqa: E501
        :rtype: int
        """
        return self._vpsa_id

    @vpsa_id.setter
    def vpsa_id(self, vpsa_id):
        """Sets the vpsa_id of this InlineResponse20024DataPubliczios.


        :param vpsa_id: The vpsa_id of this InlineResponse20024DataPubliczios.  # noqa: E501
        :type: int
        """

        self._vpsa_id = vpsa_id

    @property
    def account_name(self):
        """Gets the account_name of this InlineResponse20024DataPubliczios.  # noqa: E501


        :return: The account_name of this InlineResponse20024DataPubliczios.  # noqa: E501
        :rtype: str
        """
        return self._account_name

    @account_name.setter
    def account_name(self, account_name):
        """Sets the account_name of this InlineResponse20024DataPubliczios.


        :param account_name: The account_name of this InlineResponse20024DataPubliczios.  # noqa: E501
        :type: str
        """

        self._account_name = account_name

    @property
    def username(self):
        """Gets the username of this InlineResponse20024DataPubliczios.  # noqa: E501


        :return: The username of this InlineResponse20024DataPubliczios.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this InlineResponse20024DataPubliczios.


        :param username: The username of this InlineResponse20024DataPubliczios.  # noqa: E501
        :type: str
        """

        self._username = username

    @property
    def ip(self):
        """Gets the ip of this InlineResponse20024DataPubliczios.  # noqa: E501


        :return: The ip of this InlineResponse20024DataPubliczios.  # noqa: E501
        :rtype: str
        """
        return self._ip

    @ip.setter
    def ip(self, ip):
        """Sets the ip of this InlineResponse20024DataPubliczios.


        :param ip: The ip of this InlineResponse20024DataPubliczios.  # noqa: E501
        :type: str
        """

        self._ip = ip

    @property
    def host(self):
        """Gets the host of this InlineResponse20024DataPubliczios.  # noqa: E501


        :return: The host of this InlineResponse20024DataPubliczios.  # noqa: E501
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """Sets the host of this InlineResponse20024DataPubliczios.


        :param host: The host of this InlineResponse20024DataPubliczios.  # noqa: E501
        :type: str
        """

        self._host = host

    @property
    def auto_approve(self):
        """Gets the auto_approve of this InlineResponse20024DataPubliczios.  # noqa: E501


        :return: The auto_approve of this InlineResponse20024DataPubliczios.  # noqa: E501
        :rtype: bool
        """
        return self._auto_approve

    @auto_approve.setter
    def auto_approve(self, auto_approve):
        """Sets the auto_approve of this InlineResponse20024DataPubliczios.


        :param auto_approve: The auto_approve of this InlineResponse20024DataPubliczios.  # noqa: E501
        :type: bool
        """

        self._auto_approve = auto_approve

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
        if issubclass(InlineResponse20024DataPubliczios, dict):
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
        if not isinstance(other, InlineResponse20024DataPubliczios):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20024DataPubliczios):
            return True

        return self.to_dict() != other.to_dict()
