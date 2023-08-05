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


class InlineResponse200213User(object):
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
        'username': 'str',
        'email': 'str',
        'permissions': 'list[str]',
        'locked': 'bool',
        'roles': 'list[InlineResponse200208ResponseRoles]',
        'display_timezone': 'str'
    }

    attribute_map = {
        'id': 'id',
        'username': 'username',
        'email': 'email',
        'permissions': 'permissions',
        'locked': 'locked',
        'roles': 'roles',
        'display_timezone': 'display_timezone'
    }

    def __init__(self, id=None, username=None, email=None, permissions=None, locked=None, roles=None, display_timezone=None, _configuration=None):  # noqa: E501
        """InlineResponse200213User - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._id = None
        self._username = None
        self._email = None
        self._permissions = None
        self._locked = None
        self._roles = None
        self._display_timezone = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if username is not None:
            self.username = username
        if email is not None:
            self.email = email
        if permissions is not None:
            self.permissions = permissions
        if locked is not None:
            self.locked = locked
        if roles is not None:
            self.roles = roles
        if display_timezone is not None:
            self.display_timezone = display_timezone

    @property
    def id(self):
        """Gets the id of this InlineResponse200213User.  # noqa: E501


        :return: The id of this InlineResponse200213User.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InlineResponse200213User.


        :param id: The id of this InlineResponse200213User.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def username(self):
        """Gets the username of this InlineResponse200213User.  # noqa: E501


        :return: The username of this InlineResponse200213User.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this InlineResponse200213User.


        :param username: The username of this InlineResponse200213User.  # noqa: E501
        :type: str
        """

        self._username = username

    @property
    def email(self):
        """Gets the email of this InlineResponse200213User.  # noqa: E501


        :return: The email of this InlineResponse200213User.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this InlineResponse200213User.


        :param email: The email of this InlineResponse200213User.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def permissions(self):
        """Gets the permissions of this InlineResponse200213User.  # noqa: E501


        :return: The permissions of this InlineResponse200213User.  # noqa: E501
        :rtype: list[str]
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """Sets the permissions of this InlineResponse200213User.


        :param permissions: The permissions of this InlineResponse200213User.  # noqa: E501
        :type: list[str]
        """

        self._permissions = permissions

    @property
    def locked(self):
        """Gets the locked of this InlineResponse200213User.  # noqa: E501


        :return: The locked of this InlineResponse200213User.  # noqa: E501
        :rtype: bool
        """
        return self._locked

    @locked.setter
    def locked(self, locked):
        """Sets the locked of this InlineResponse200213User.


        :param locked: The locked of this InlineResponse200213User.  # noqa: E501
        :type: bool
        """

        self._locked = locked

    @property
    def roles(self):
        """Gets the roles of this InlineResponse200213User.  # noqa: E501


        :return: The roles of this InlineResponse200213User.  # noqa: E501
        :rtype: list[InlineResponse200208ResponseRoles]
        """
        return self._roles

    @roles.setter
    def roles(self, roles):
        """Sets the roles of this InlineResponse200213User.


        :param roles: The roles of this InlineResponse200213User.  # noqa: E501
        :type: list[InlineResponse200208ResponseRoles]
        """

        self._roles = roles

    @property
    def display_timezone(self):
        """Gets the display_timezone of this InlineResponse200213User.  # noqa: E501


        :return: The display_timezone of this InlineResponse200213User.  # noqa: E501
        :rtype: str
        """
        return self._display_timezone

    @display_timezone.setter
    def display_timezone(self, display_timezone):
        """Sets the display_timezone of this InlineResponse200213User.


        :param display_timezone: The display_timezone of this InlineResponse200213User.  # noqa: E501
        :type: str
        """

        self._display_timezone = display_timezone

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
        if issubclass(InlineResponse200213User, dict):
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
        if not isinstance(other, InlineResponse200213User):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse200213User):
            return True

        return self.to_dict() != other.to_dict()
