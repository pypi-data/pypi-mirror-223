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


class DeleteServerSession(object):
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
        'initiator': 'str',
        'target': 'str'
    }

    attribute_map = {
        'initiator': 'initiator',
        'target': 'target'
    }

    def __init__(self, initiator=None, target=None, _configuration=None):  # noqa: E501
        """DeleteServerSession - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._initiator = None
        self._target = None
        self.discriminator = None

        self.initiator = initiator
        self.target = target

    @property
    def initiator(self):
        """Gets the initiator of this DeleteServerSession.  # noqa: E501

        Session's Initiator  # noqa: E501

        :return: The initiator of this DeleteServerSession.  # noqa: E501
        :rtype: str
        """
        return self._initiator

    @initiator.setter
    def initiator(self, initiator):
        """Sets the initiator of this DeleteServerSession.

        Session's Initiator  # noqa: E501

        :param initiator: The initiator of this DeleteServerSession.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and initiator is None:
            raise ValueError("Invalid value for `initiator`, must not be `None`")  # noqa: E501

        self._initiator = initiator

    @property
    def target(self):
        """Gets the target of this DeleteServerSession.  # noqa: E501

        Session's Target  # noqa: E501

        :return: The target of this DeleteServerSession.  # noqa: E501
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """Sets the target of this DeleteServerSession.

        Session's Target  # noqa: E501

        :param target: The target of this DeleteServerSession.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and target is None:
            raise ValueError("Invalid value for `target`, must not be `None`")  # noqa: E501

        self._target = target

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
        if issubclass(DeleteServerSession, dict):
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
        if not isinstance(other, DeleteServerSession):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DeleteServerSession):
            return True

        return self.to_dict() != other.to_dict()
