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


class ChangeMtuForNetworkInterface(object):
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
        'fe_mtu': 'str',
        'public_mtu': 'str',
        'force': 'str'
    }

    attribute_map = {
        'fe_mtu': 'fe_mtu',
        'public_mtu': 'public_mtu',
        'force': 'force'
    }

    def __init__(self, fe_mtu=None, public_mtu=None, force=None, _configuration=None):  # noqa: E501
        """ChangeMtuForNetworkInterface - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._fe_mtu = None
        self._public_mtu = None
        self._force = None
        self.discriminator = None

        if fe_mtu is not None:
            self.fe_mtu = fe_mtu
        if public_mtu is not None:
            self.public_mtu = public_mtu
        if force is not None:
            self.force = force

    @property
    def fe_mtu(self):
        """Gets the fe_mtu of this ChangeMtuForNetworkInterface.  # noqa: E501

        An MTU value for the frontend interface  # noqa: E501

        :return: The fe_mtu of this ChangeMtuForNetworkInterface.  # noqa: E501
        :rtype: str
        """
        return self._fe_mtu

    @fe_mtu.setter
    def fe_mtu(self, fe_mtu):
        """Sets the fe_mtu of this ChangeMtuForNetworkInterface.

        An MTU value for the frontend interface  # noqa: E501

        :param fe_mtu: The fe_mtu of this ChangeMtuForNetworkInterface.  # noqa: E501
        :type: str
        """

        self._fe_mtu = fe_mtu

    @property
    def public_mtu(self):
        """Gets the public_mtu of this ChangeMtuForNetworkInterface.  # noqa: E501

        An MTU value for the public interface  # noqa: E501

        :return: The public_mtu of this ChangeMtuForNetworkInterface.  # noqa: E501
        :rtype: str
        """
        return self._public_mtu

    @public_mtu.setter
    def public_mtu(self, public_mtu):
        """Sets the public_mtu of this ChangeMtuForNetworkInterface.

        An MTU value for the public interface  # noqa: E501

        :param public_mtu: The public_mtu of this ChangeMtuForNetworkInterface.  # noqa: E501
        :type: str
        """

        self._public_mtu = public_mtu

    @property
    def force(self):
        """Gets the force of this ChangeMtuForNetworkInterface.  # noqa: E501


        :return: The force of this ChangeMtuForNetworkInterface.  # noqa: E501
        :rtype: str
        """
        return self._force

    @force.setter
    def force(self, force):
        """Sets the force of this ChangeMtuForNetworkInterface.


        :param force: The force of this ChangeMtuForNetworkInterface.  # noqa: E501
        :type: str
        """
        allowed_values = ["YES", "NO"]  # noqa: E501
        if (self._configuration.client_side_validation and
                force not in allowed_values):
            raise ValueError(
                "Invalid value for `force` ({0}), must be one of {1}"  # noqa: E501
                .format(force, allowed_values)
            )

        self._force = force

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
        if issubclass(ChangeMtuForNetworkInterface, dict):
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
        if not isinstance(other, ChangeMtuForNetworkInterface):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChangeMtuForNetworkInterface):
            return True

        return self.to_dict() != other.to_dict()
