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


class InlineResponse20013ResponseContainerMemoryPools(object):
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
        'mb': 'str',
        'containers': 'list[InlineResponse20013ResponseContainers]'
    }

    attribute_map = {
        'name': 'name',
        'display_name': 'display_name',
        'mb': 'mb',
        'containers': 'containers'
    }

    def __init__(self, name=None, display_name=None, mb=None, containers=None, _configuration=None):  # noqa: E501
        """InlineResponse20013ResponseContainerMemoryPools - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._display_name = None
        self._mb = None
        self._containers = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if display_name is not None:
            self.display_name = display_name
        if mb is not None:
            self.mb = mb
        if containers is not None:
            self.containers = containers

    @property
    def name(self):
        """Gets the name of this InlineResponse20013ResponseContainerMemoryPools.  # noqa: E501


        :return: The name of this InlineResponse20013ResponseContainerMemoryPools.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse20013ResponseContainerMemoryPools.


        :param name: The name of this InlineResponse20013ResponseContainerMemoryPools.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def display_name(self):
        """Gets the display_name of this InlineResponse20013ResponseContainerMemoryPools.  # noqa: E501


        :return: The display_name of this InlineResponse20013ResponseContainerMemoryPools.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this InlineResponse20013ResponseContainerMemoryPools.


        :param display_name: The display_name of this InlineResponse20013ResponseContainerMemoryPools.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def mb(self):
        """Gets the mb of this InlineResponse20013ResponseContainerMemoryPools.  # noqa: E501


        :return: The mb of this InlineResponse20013ResponseContainerMemoryPools.  # noqa: E501
        :rtype: str
        """
        return self._mb

    @mb.setter
    def mb(self, mb):
        """Sets the mb of this InlineResponse20013ResponseContainerMemoryPools.


        :param mb: The mb of this InlineResponse20013ResponseContainerMemoryPools.  # noqa: E501
        :type: str
        """

        self._mb = mb

    @property
    def containers(self):
        """Gets the containers of this InlineResponse20013ResponseContainerMemoryPools.  # noqa: E501


        :return: The containers of this InlineResponse20013ResponseContainerMemoryPools.  # noqa: E501
        :rtype: list[InlineResponse20013ResponseContainers]
        """
        return self._containers

    @containers.setter
    def containers(self, containers):
        """Sets the containers of this InlineResponse20013ResponseContainerMemoryPools.


        :param containers: The containers of this InlineResponse20013ResponseContainerMemoryPools.  # noqa: E501
        :type: list[InlineResponse20013ResponseContainers]
        """

        self._containers = containers

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
        if issubclass(InlineResponse20013ResponseContainerMemoryPools, dict):
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
        if not isinstance(other, InlineResponse20013ResponseContainerMemoryPools):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20013ResponseContainerMemoryPools):
            return True

        return self.to_dict() != other.to_dict()
