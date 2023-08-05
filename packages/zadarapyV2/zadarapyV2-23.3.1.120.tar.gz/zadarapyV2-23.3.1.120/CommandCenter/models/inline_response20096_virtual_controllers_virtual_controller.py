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


class InlineResponse20096VirtualControllersVirtualController(object):
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
        'state': 'str',
        'type': 'str',
        'node': 'str',
        'be_ip': 'str',
        'be_vlan_id': 'int',
        'fe_ip': 'str',
        'fe_vlan_id': 'str',
        'hb_ip': 'str',
        'hb_vlan_id': 'str'
    }

    attribute_map = {
        'name': 'name',
        'state': 'state',
        'type': 'type',
        'node': 'node',
        'be_ip': 'be_ip',
        'be_vlan_id': 'be_vlan_id',
        'fe_ip': 'fe_ip',
        'fe_vlan_id': 'fe_vlan_id',
        'hb_ip': 'hb_ip',
        'hb_vlan_id': 'hb_vlan_id'
    }

    def __init__(self, name=None, state=None, type=None, node=None, be_ip=None, be_vlan_id=None, fe_ip=None, fe_vlan_id=None, hb_ip=None, hb_vlan_id=None, _configuration=None):  # noqa: E501
        """InlineResponse20096VirtualControllersVirtualController - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._state = None
        self._type = None
        self._node = None
        self._be_ip = None
        self._be_vlan_id = None
        self._fe_ip = None
        self._fe_vlan_id = None
        self._hb_ip = None
        self._hb_vlan_id = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if state is not None:
            self.state = state
        if type is not None:
            self.type = type
        if node is not None:
            self.node = node
        if be_ip is not None:
            self.be_ip = be_ip
        if be_vlan_id is not None:
            self.be_vlan_id = be_vlan_id
        if fe_ip is not None:
            self.fe_ip = fe_ip
        if fe_vlan_id is not None:
            self.fe_vlan_id = fe_vlan_id
        if hb_ip is not None:
            self.hb_ip = hb_ip
        if hb_vlan_id is not None:
            self.hb_vlan_id = hb_vlan_id

    @property
    def name(self):
        """Gets the name of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501


        :return: The name of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse20096VirtualControllersVirtualController.


        :param name: The name of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def state(self):
        """Gets the state of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501


        :return: The state of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this InlineResponse20096VirtualControllersVirtualController.


        :param state: The state of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def type(self):
        """Gets the type of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501


        :return: The type of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this InlineResponse20096VirtualControllersVirtualController.


        :param type: The type of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def node(self):
        """Gets the node of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501


        :return: The node of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :rtype: str
        """
        return self._node

    @node.setter
    def node(self, node):
        """Sets the node of this InlineResponse20096VirtualControllersVirtualController.


        :param node: The node of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :type: str
        """

        self._node = node

    @property
    def be_ip(self):
        """Gets the be_ip of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501


        :return: The be_ip of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :rtype: str
        """
        return self._be_ip

    @be_ip.setter
    def be_ip(self, be_ip):
        """Sets the be_ip of this InlineResponse20096VirtualControllersVirtualController.


        :param be_ip: The be_ip of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :type: str
        """

        self._be_ip = be_ip

    @property
    def be_vlan_id(self):
        """Gets the be_vlan_id of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501


        :return: The be_vlan_id of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :rtype: int
        """
        return self._be_vlan_id

    @be_vlan_id.setter
    def be_vlan_id(self, be_vlan_id):
        """Sets the be_vlan_id of this InlineResponse20096VirtualControllersVirtualController.


        :param be_vlan_id: The be_vlan_id of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :type: int
        """

        self._be_vlan_id = be_vlan_id

    @property
    def fe_ip(self):
        """Gets the fe_ip of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501


        :return: The fe_ip of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :rtype: str
        """
        return self._fe_ip

    @fe_ip.setter
    def fe_ip(self, fe_ip):
        """Sets the fe_ip of this InlineResponse20096VirtualControllersVirtualController.


        :param fe_ip: The fe_ip of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :type: str
        """

        self._fe_ip = fe_ip

    @property
    def fe_vlan_id(self):
        """Gets the fe_vlan_id of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501


        :return: The fe_vlan_id of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :rtype: str
        """
        return self._fe_vlan_id

    @fe_vlan_id.setter
    def fe_vlan_id(self, fe_vlan_id):
        """Sets the fe_vlan_id of this InlineResponse20096VirtualControllersVirtualController.


        :param fe_vlan_id: The fe_vlan_id of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :type: str
        """

        self._fe_vlan_id = fe_vlan_id

    @property
    def hb_ip(self):
        """Gets the hb_ip of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501


        :return: The hb_ip of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :rtype: str
        """
        return self._hb_ip

    @hb_ip.setter
    def hb_ip(self, hb_ip):
        """Sets the hb_ip of this InlineResponse20096VirtualControllersVirtualController.


        :param hb_ip: The hb_ip of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :type: str
        """

        self._hb_ip = hb_ip

    @property
    def hb_vlan_id(self):
        """Gets the hb_vlan_id of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501


        :return: The hb_vlan_id of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :rtype: str
        """
        return self._hb_vlan_id

    @hb_vlan_id.setter
    def hb_vlan_id(self, hb_vlan_id):
        """Sets the hb_vlan_id of this InlineResponse20096VirtualControllersVirtualController.


        :param hb_vlan_id: The hb_vlan_id of this InlineResponse20096VirtualControllersVirtualController.  # noqa: E501
        :type: str
        """

        self._hb_vlan_id = hb_vlan_id

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
        if issubclass(InlineResponse20096VirtualControllersVirtualController, dict):
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
        if not isinstance(other, InlineResponse20096VirtualControllersVirtualController):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20096VirtualControllersVirtualController):
            return True

        return self.to_dict() != other.to_dict()
