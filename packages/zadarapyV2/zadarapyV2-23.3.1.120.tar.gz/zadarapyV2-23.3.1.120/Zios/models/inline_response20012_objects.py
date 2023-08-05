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


class InlineResponse20012Objects(object):
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
        'time': 'int',
        'iops_put': 'float',
        'iops_delete': 'float',
        'iops_get': 'float'
    }

    attribute_map = {
        'time': 'time',
        'iops_put': 'iops_put',
        'iops_delete': 'iops_delete',
        'iops_get': 'iops_get'
    }

    def __init__(self, time=None, iops_put=None, iops_delete=None, iops_get=None, _configuration=None):  # noqa: E501
        """InlineResponse20012Objects - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._time = None
        self._iops_put = None
        self._iops_delete = None
        self._iops_get = None
        self.discriminator = None

        if time is not None:
            self.time = time
        if iops_put is not None:
            self.iops_put = iops_put
        if iops_delete is not None:
            self.iops_delete = iops_delete
        if iops_get is not None:
            self.iops_get = iops_get

    @property
    def time(self):
        """Gets the time of this InlineResponse20012Objects.  # noqa: E501


        :return: The time of this InlineResponse20012Objects.  # noqa: E501
        :rtype: int
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this InlineResponse20012Objects.


        :param time: The time of this InlineResponse20012Objects.  # noqa: E501
        :type: int
        """

        self._time = time

    @property
    def iops_put(self):
        """Gets the iops_put of this InlineResponse20012Objects.  # noqa: E501


        :return: The iops_put of this InlineResponse20012Objects.  # noqa: E501
        :rtype: float
        """
        return self._iops_put

    @iops_put.setter
    def iops_put(self, iops_put):
        """Sets the iops_put of this InlineResponse20012Objects.


        :param iops_put: The iops_put of this InlineResponse20012Objects.  # noqa: E501
        :type: float
        """

        self._iops_put = iops_put

    @property
    def iops_delete(self):
        """Gets the iops_delete of this InlineResponse20012Objects.  # noqa: E501


        :return: The iops_delete of this InlineResponse20012Objects.  # noqa: E501
        :rtype: float
        """
        return self._iops_delete

    @iops_delete.setter
    def iops_delete(self, iops_delete):
        """Sets the iops_delete of this InlineResponse20012Objects.


        :param iops_delete: The iops_delete of this InlineResponse20012Objects.  # noqa: E501
        :type: float
        """

        self._iops_delete = iops_delete

    @property
    def iops_get(self):
        """Gets the iops_get of this InlineResponse20012Objects.  # noqa: E501


        :return: The iops_get of this InlineResponse20012Objects.  # noqa: E501
        :rtype: float
        """
        return self._iops_get

    @iops_get.setter
    def iops_get(self, iops_get):
        """Sets the iops_get of this InlineResponse20012Objects.


        :param iops_get: The iops_get of this InlineResponse20012Objects.  # noqa: E501
        :type: float
        """

        self._iops_get = iops_get

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
        if issubclass(InlineResponse20012Objects, dict):
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
        if not isinstance(other, InlineResponse20012Objects):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20012Objects):
            return True

        return self.to_dict() != other.to_dict()
