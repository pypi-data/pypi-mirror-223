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


class InlineResponse20020ResponseSessions(object):
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
        'access_type': 'str',
        'initiator': 'str',
        'target': 'str',
        'count': 'int',
        'vc': 'int',
        'server_name': 'str',
        'server_display_name': 'str'
    }

    attribute_map = {
        'access_type': 'access_type',
        'initiator': 'initiator',
        'target': 'target',
        'count': 'count',
        'vc': 'vc',
        'server_name': 'server_name',
        'server_display_name': 'server_display_name'
    }

    def __init__(self, access_type=None, initiator=None, target=None, count=None, vc=None, server_name=None, server_display_name=None, _configuration=None):  # noqa: E501
        """InlineResponse20020ResponseSessions - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._access_type = None
        self._initiator = None
        self._target = None
        self._count = None
        self._vc = None
        self._server_name = None
        self._server_display_name = None
        self.discriminator = None

        if access_type is not None:
            self.access_type = access_type
        if initiator is not None:
            self.initiator = initiator
        if target is not None:
            self.target = target
        if count is not None:
            self.count = count
        if vc is not None:
            self.vc = vc
        if server_name is not None:
            self.server_name = server_name
        if server_display_name is not None:
            self.server_display_name = server_display_name

    @property
    def access_type(self):
        """Gets the access_type of this InlineResponse20020ResponseSessions.  # noqa: E501


        :return: The access_type of this InlineResponse20020ResponseSessions.  # noqa: E501
        :rtype: str
        """
        return self._access_type

    @access_type.setter
    def access_type(self, access_type):
        """Sets the access_type of this InlineResponse20020ResponseSessions.


        :param access_type: The access_type of this InlineResponse20020ResponseSessions.  # noqa: E501
        :type: str
        """

        self._access_type = access_type

    @property
    def initiator(self):
        """Gets the initiator of this InlineResponse20020ResponseSessions.  # noqa: E501


        :return: The initiator of this InlineResponse20020ResponseSessions.  # noqa: E501
        :rtype: str
        """
        return self._initiator

    @initiator.setter
    def initiator(self, initiator):
        """Sets the initiator of this InlineResponse20020ResponseSessions.


        :param initiator: The initiator of this InlineResponse20020ResponseSessions.  # noqa: E501
        :type: str
        """

        self._initiator = initiator

    @property
    def target(self):
        """Gets the target of this InlineResponse20020ResponseSessions.  # noqa: E501


        :return: The target of this InlineResponse20020ResponseSessions.  # noqa: E501
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """Sets the target of this InlineResponse20020ResponseSessions.


        :param target: The target of this InlineResponse20020ResponseSessions.  # noqa: E501
        :type: str
        """

        self._target = target

    @property
    def count(self):
        """Gets the count of this InlineResponse20020ResponseSessions.  # noqa: E501


        :return: The count of this InlineResponse20020ResponseSessions.  # noqa: E501
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this InlineResponse20020ResponseSessions.


        :param count: The count of this InlineResponse20020ResponseSessions.  # noqa: E501
        :type: int
        """

        self._count = count

    @property
    def vc(self):
        """Gets the vc of this InlineResponse20020ResponseSessions.  # noqa: E501


        :return: The vc of this InlineResponse20020ResponseSessions.  # noqa: E501
        :rtype: int
        """
        return self._vc

    @vc.setter
    def vc(self, vc):
        """Sets the vc of this InlineResponse20020ResponseSessions.


        :param vc: The vc of this InlineResponse20020ResponseSessions.  # noqa: E501
        :type: int
        """

        self._vc = vc

    @property
    def server_name(self):
        """Gets the server_name of this InlineResponse20020ResponseSessions.  # noqa: E501


        :return: The server_name of this InlineResponse20020ResponseSessions.  # noqa: E501
        :rtype: str
        """
        return self._server_name

    @server_name.setter
    def server_name(self, server_name):
        """Sets the server_name of this InlineResponse20020ResponseSessions.


        :param server_name: The server_name of this InlineResponse20020ResponseSessions.  # noqa: E501
        :type: str
        """

        self._server_name = server_name

    @property
    def server_display_name(self):
        """Gets the server_display_name of this InlineResponse20020ResponseSessions.  # noqa: E501


        :return: The server_display_name of this InlineResponse20020ResponseSessions.  # noqa: E501
        :rtype: str
        """
        return self._server_display_name

    @server_display_name.setter
    def server_display_name(self, server_display_name):
        """Sets the server_display_name of this InlineResponse20020ResponseSessions.


        :param server_display_name: The server_display_name of this InlineResponse20020ResponseSessions.  # noqa: E501
        :type: str
        """

        self._server_display_name = server_display_name

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
        if issubclass(InlineResponse20020ResponseSessions, dict):
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
        if not isinstance(other, InlineResponse20020ResponseSessions):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20020ResponseSessions):
            return True

        return self.to_dict() != other.to_dict()
