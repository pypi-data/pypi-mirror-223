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


class InlineResponse20038Nodes(object):
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
        'status': 'str',
        'absent': 'bool',
        'information': 'InlineResponse20038Information',
        'nic_information': 'list[InlineResponse20038NicInformation]',
        'services': 'list[InlineResponse20038Services]',
        'resources': 'InlineResponse20038Resources',
        'drives': 'list[InlineResponse20038Drives]',
        'fault_domain': 'str',
        'master': 'bool',
        'slave': 'bool',
        'faulty_services': 'list[str]',
        'config_role': 'str',
        'macs': 'InlineResponse20038Macs',
        'ips': 'InlineResponse20038Ips',
        'virtual_controllers': 'int',
        'license': 'InlineResponse20038License'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'status': 'status',
        'absent': 'absent',
        'information': 'information',
        'nic_information': 'nic_information',
        'services': 'services',
        'resources': 'resources',
        'drives': 'drives',
        'fault_domain': 'fault_domain',
        'master': 'master',
        'slave': 'slave',
        'faulty_services': 'faulty_services',
        'config_role': 'config_role',
        'macs': 'macs',
        'ips': 'ips',
        'virtual_controllers': 'virtual_controllers',
        'license': 'license'
    }

    def __init__(self, id=None, name=None, status=None, absent=None, information=None, nic_information=None, services=None, resources=None, drives=None, fault_domain=None, master=None, slave=None, faulty_services=None, config_role=None, macs=None, ips=None, virtual_controllers=None, license=None, _configuration=None):  # noqa: E501
        """InlineResponse20038Nodes - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._id = None
        self._name = None
        self._status = None
        self._absent = None
        self._information = None
        self._nic_information = None
        self._services = None
        self._resources = None
        self._drives = None
        self._fault_domain = None
        self._master = None
        self._slave = None
        self._faulty_services = None
        self._config_role = None
        self._macs = None
        self._ips = None
        self._virtual_controllers = None
        self._license = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if status is not None:
            self.status = status
        if absent is not None:
            self.absent = absent
        if information is not None:
            self.information = information
        if nic_information is not None:
            self.nic_information = nic_information
        if services is not None:
            self.services = services
        if resources is not None:
            self.resources = resources
        if drives is not None:
            self.drives = drives
        if fault_domain is not None:
            self.fault_domain = fault_domain
        if master is not None:
            self.master = master
        if slave is not None:
            self.slave = slave
        if faulty_services is not None:
            self.faulty_services = faulty_services
        if config_role is not None:
            self.config_role = config_role
        if macs is not None:
            self.macs = macs
        if ips is not None:
            self.ips = ips
        if virtual_controllers is not None:
            self.virtual_controllers = virtual_controllers
        if license is not None:
            self.license = license

    @property
    def id(self):
        """Gets the id of this InlineResponse20038Nodes.  # noqa: E501


        :return: The id of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InlineResponse20038Nodes.


        :param id: The id of this InlineResponse20038Nodes.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this InlineResponse20038Nodes.  # noqa: E501


        :return: The name of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse20038Nodes.


        :param name: The name of this InlineResponse20038Nodes.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def status(self):
        """Gets the status of this InlineResponse20038Nodes.  # noqa: E501


        :return: The status of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InlineResponse20038Nodes.


        :param status: The status of this InlineResponse20038Nodes.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def absent(self):
        """Gets the absent of this InlineResponse20038Nodes.  # noqa: E501


        :return: The absent of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: bool
        """
        return self._absent

    @absent.setter
    def absent(self, absent):
        """Sets the absent of this InlineResponse20038Nodes.


        :param absent: The absent of this InlineResponse20038Nodes.  # noqa: E501
        :type: bool
        """

        self._absent = absent

    @property
    def information(self):
        """Gets the information of this InlineResponse20038Nodes.  # noqa: E501


        :return: The information of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: InlineResponse20038Information
        """
        return self._information

    @information.setter
    def information(self, information):
        """Sets the information of this InlineResponse20038Nodes.


        :param information: The information of this InlineResponse20038Nodes.  # noqa: E501
        :type: InlineResponse20038Information
        """

        self._information = information

    @property
    def nic_information(self):
        """Gets the nic_information of this InlineResponse20038Nodes.  # noqa: E501


        :return: The nic_information of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: list[InlineResponse20038NicInformation]
        """
        return self._nic_information

    @nic_information.setter
    def nic_information(self, nic_information):
        """Sets the nic_information of this InlineResponse20038Nodes.


        :param nic_information: The nic_information of this InlineResponse20038Nodes.  # noqa: E501
        :type: list[InlineResponse20038NicInformation]
        """

        self._nic_information = nic_information

    @property
    def services(self):
        """Gets the services of this InlineResponse20038Nodes.  # noqa: E501


        :return: The services of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: list[InlineResponse20038Services]
        """
        return self._services

    @services.setter
    def services(self, services):
        """Sets the services of this InlineResponse20038Nodes.


        :param services: The services of this InlineResponse20038Nodes.  # noqa: E501
        :type: list[InlineResponse20038Services]
        """

        self._services = services

    @property
    def resources(self):
        """Gets the resources of this InlineResponse20038Nodes.  # noqa: E501


        :return: The resources of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: InlineResponse20038Resources
        """
        return self._resources

    @resources.setter
    def resources(self, resources):
        """Sets the resources of this InlineResponse20038Nodes.


        :param resources: The resources of this InlineResponse20038Nodes.  # noqa: E501
        :type: InlineResponse20038Resources
        """

        self._resources = resources

    @property
    def drives(self):
        """Gets the drives of this InlineResponse20038Nodes.  # noqa: E501


        :return: The drives of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: list[InlineResponse20038Drives]
        """
        return self._drives

    @drives.setter
    def drives(self, drives):
        """Sets the drives of this InlineResponse20038Nodes.


        :param drives: The drives of this InlineResponse20038Nodes.  # noqa: E501
        :type: list[InlineResponse20038Drives]
        """

        self._drives = drives

    @property
    def fault_domain(self):
        """Gets the fault_domain of this InlineResponse20038Nodes.  # noqa: E501


        :return: The fault_domain of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: str
        """
        return self._fault_domain

    @fault_domain.setter
    def fault_domain(self, fault_domain):
        """Sets the fault_domain of this InlineResponse20038Nodes.


        :param fault_domain: The fault_domain of this InlineResponse20038Nodes.  # noqa: E501
        :type: str
        """

        self._fault_domain = fault_domain

    @property
    def master(self):
        """Gets the master of this InlineResponse20038Nodes.  # noqa: E501


        :return: The master of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: bool
        """
        return self._master

    @master.setter
    def master(self, master):
        """Sets the master of this InlineResponse20038Nodes.


        :param master: The master of this InlineResponse20038Nodes.  # noqa: E501
        :type: bool
        """

        self._master = master

    @property
    def slave(self):
        """Gets the slave of this InlineResponse20038Nodes.  # noqa: E501


        :return: The slave of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: bool
        """
        return self._slave

    @slave.setter
    def slave(self, slave):
        """Sets the slave of this InlineResponse20038Nodes.


        :param slave: The slave of this InlineResponse20038Nodes.  # noqa: E501
        :type: bool
        """

        self._slave = slave

    @property
    def faulty_services(self):
        """Gets the faulty_services of this InlineResponse20038Nodes.  # noqa: E501


        :return: The faulty_services of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: list[str]
        """
        return self._faulty_services

    @faulty_services.setter
    def faulty_services(self, faulty_services):
        """Sets the faulty_services of this InlineResponse20038Nodes.


        :param faulty_services: The faulty_services of this InlineResponse20038Nodes.  # noqa: E501
        :type: list[str]
        """

        self._faulty_services = faulty_services

    @property
    def config_role(self):
        """Gets the config_role of this InlineResponse20038Nodes.  # noqa: E501


        :return: The config_role of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: str
        """
        return self._config_role

    @config_role.setter
    def config_role(self, config_role):
        """Sets the config_role of this InlineResponse20038Nodes.


        :param config_role: The config_role of this InlineResponse20038Nodes.  # noqa: E501
        :type: str
        """

        self._config_role = config_role

    @property
    def macs(self):
        """Gets the macs of this InlineResponse20038Nodes.  # noqa: E501


        :return: The macs of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: InlineResponse20038Macs
        """
        return self._macs

    @macs.setter
    def macs(self, macs):
        """Sets the macs of this InlineResponse20038Nodes.


        :param macs: The macs of this InlineResponse20038Nodes.  # noqa: E501
        :type: InlineResponse20038Macs
        """

        self._macs = macs

    @property
    def ips(self):
        """Gets the ips of this InlineResponse20038Nodes.  # noqa: E501


        :return: The ips of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: InlineResponse20038Ips
        """
        return self._ips

    @ips.setter
    def ips(self, ips):
        """Sets the ips of this InlineResponse20038Nodes.


        :param ips: The ips of this InlineResponse20038Nodes.  # noqa: E501
        :type: InlineResponse20038Ips
        """

        self._ips = ips

    @property
    def virtual_controllers(self):
        """Gets the virtual_controllers of this InlineResponse20038Nodes.  # noqa: E501


        :return: The virtual_controllers of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: int
        """
        return self._virtual_controllers

    @virtual_controllers.setter
    def virtual_controllers(self, virtual_controllers):
        """Sets the virtual_controllers of this InlineResponse20038Nodes.


        :param virtual_controllers: The virtual_controllers of this InlineResponse20038Nodes.  # noqa: E501
        :type: int
        """

        self._virtual_controllers = virtual_controllers

    @property
    def license(self):
        """Gets the license of this InlineResponse20038Nodes.  # noqa: E501


        :return: The license of this InlineResponse20038Nodes.  # noqa: E501
        :rtype: InlineResponse20038License
        """
        return self._license

    @license.setter
    def license(self, license):
        """Sets the license of this InlineResponse20038Nodes.


        :param license: The license of this InlineResponse20038Nodes.  # noqa: E501
        :type: InlineResponse20038License
        """

        self._license = license

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
        if issubclass(InlineResponse20038Nodes, dict):
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
        if not isinstance(other, InlineResponse20038Nodes):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20038Nodes):
            return True

        return self.to_dict() != other.to_dict()
