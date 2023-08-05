# coding: utf-8

"""
    Command Center operations

    Command Center operations  # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from CommandCenter.configuration import Configuration


class InlineResponse200AccessLogs(object):
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
        'user_id': 'str',
        'controller': 'str',
        'action': 'str',
        'access_type': 'str'
    }

    attribute_map = {
        'id': 'id',
        'user_id': 'user_id',
        'controller': 'controller',
        'action': 'action',
        'access_type': 'access_type'
    }

    def __init__(self, id=None, user_id=None, controller=None, action=None, access_type=None, _configuration=None):  # noqa: E501
        """InlineResponse200AccessLogs - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._id = None
        self._user_id = None
        self._controller = None
        self._action = None
        self._access_type = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if user_id is not None:
            self.user_id = user_id
        if controller is not None:
            self.controller = controller
        if action is not None:
            self.action = action
        if access_type is not None:
            self.access_type = access_type

    @property
    def id(self):
        """Gets the id of this InlineResponse200AccessLogs.  # noqa: E501


        :return: The id of this InlineResponse200AccessLogs.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InlineResponse200AccessLogs.


        :param id: The id of this InlineResponse200AccessLogs.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def user_id(self):
        """Gets the user_id of this InlineResponse200AccessLogs.  # noqa: E501


        :return: The user_id of this InlineResponse200AccessLogs.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this InlineResponse200AccessLogs.


        :param user_id: The user_id of this InlineResponse200AccessLogs.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

    @property
    def controller(self):
        """Gets the controller of this InlineResponse200AccessLogs.  # noqa: E501


        :return: The controller of this InlineResponse200AccessLogs.  # noqa: E501
        :rtype: str
        """
        return self._controller

    @controller.setter
    def controller(self, controller):
        """Sets the controller of this InlineResponse200AccessLogs.


        :param controller: The controller of this InlineResponse200AccessLogs.  # noqa: E501
        :type: str
        """

        self._controller = controller

    @property
    def action(self):
        """Gets the action of this InlineResponse200AccessLogs.  # noqa: E501


        :return: The action of this InlineResponse200AccessLogs.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this InlineResponse200AccessLogs.


        :param action: The action of this InlineResponse200AccessLogs.  # noqa: E501
        :type: str
        """

        self._action = action

    @property
    def access_type(self):
        """Gets the access_type of this InlineResponse200AccessLogs.  # noqa: E501


        :return: The access_type of this InlineResponse200AccessLogs.  # noqa: E501
        :rtype: str
        """
        return self._access_type

    @access_type.setter
    def access_type(self, access_type):
        """Sets the access_type of this InlineResponse200AccessLogs.


        :param access_type: The access_type of this InlineResponse200AccessLogs.  # noqa: E501
        :type: str
        """

        self._access_type = access_type

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
        if issubclass(InlineResponse200AccessLogs, dict):
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
        if not isinstance(other, InlineResponse200AccessLogs):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse200AccessLogs):
            return True

        return self.to_dict() != other.to_dict()
