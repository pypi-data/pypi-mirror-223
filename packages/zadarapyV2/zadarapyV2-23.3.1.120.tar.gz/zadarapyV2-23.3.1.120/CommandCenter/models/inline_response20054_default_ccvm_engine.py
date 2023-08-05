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


class InlineResponse20054DefaultCcvmEngine(object):
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
        'name': 'str',
        'vcpus': 'int',
        'ram': 'int',
        'created_at': 'str',
        'updated_at': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'vcpus': 'vcpus',
        'ram': 'ram',
        'created_at': 'created_at',
        'updated_at': 'updated_at'
    }

    def __init__(self, id=None, name=None, vcpus=None, ram=None, created_at=None, updated_at=None, _configuration=None):  # noqa: E501
        """InlineResponse20054DefaultCcvmEngine - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._id = None
        self._name = None
        self._vcpus = None
        self._ram = None
        self._created_at = None
        self._updated_at = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if vcpus is not None:
            self.vcpus = vcpus
        if ram is not None:
            self.ram = ram
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at

    @property
    def id(self):
        """Gets the id of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501


        :return: The id of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InlineResponse20054DefaultCcvmEngine.


        :param id: The id of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501


        :return: The name of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse20054DefaultCcvmEngine.


        :param name: The name of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def vcpus(self):
        """Gets the vcpus of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501


        :return: The vcpus of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501
        :rtype: int
        """
        return self._vcpus

    @vcpus.setter
    def vcpus(self, vcpus):
        """Sets the vcpus of this InlineResponse20054DefaultCcvmEngine.


        :param vcpus: The vcpus of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501
        :type: int
        """

        self._vcpus = vcpus

    @property
    def ram(self):
        """Gets the ram of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501


        :return: The ram of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501
        :rtype: int
        """
        return self._ram

    @ram.setter
    def ram(self, ram):
        """Sets the ram of this InlineResponse20054DefaultCcvmEngine.


        :param ram: The ram of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501
        :type: int
        """

        self._ram = ram

    @property
    def created_at(self):
        """Gets the created_at of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501


        :return: The created_at of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InlineResponse20054DefaultCcvmEngine.


        :param created_at: The created_at of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def updated_at(self):
        """Gets the updated_at of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501


        :return: The updated_at of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501
        :rtype: str
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at):
        """Sets the updated_at of this InlineResponse20054DefaultCcvmEngine.


        :param updated_at: The updated_at of this InlineResponse20054DefaultCcvmEngine.  # noqa: E501
        :type: str
        """

        self._updated_at = updated_at

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
        if issubclass(InlineResponse20054DefaultCcvmEngine, dict):
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
        if not isinstance(other, InlineResponse20054DefaultCcvmEngine):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20054DefaultCcvmEngine):
            return True

        return self.to_dict() != other.to_dict()
