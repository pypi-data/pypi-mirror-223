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


class InlineResponse2008ResponseContainer(object):
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
        'image_name': 'str',
        'image_display_name': 'str',
        'image_id': 'int',
        'memory_pool_name': 'str',
        'memory_pool_display_name': 'str',
        'status': 'str',
        'entrypoint': 'str',
        'ip': 'str',
        'udp': 'str',
        'use_public_ip': 'int',
        'docker_id': 'str',
        'play_mode': 'int',
        'server_id': 'int',
        'exit_code': 'int',
        'created_at': 'str',
        'modified_at': 'str',
        'started_at': 'str',
        'exit_at': 'str',
        'ports': 'list[str]',
        'volumes': 'list[InlineResponse2006ResponseVolumes]',
        'envvars': 'list[str]',
        'args': 'list[str]',
        'links': 'list[str]',
        'is_running': 'str',
        'should_run': 'str',
        'comment': 'str',
        'dgroup_name': 'str',
        'dgroup_display_name': 'str'
    }

    attribute_map = {
        'name': 'name',
        'display_name': 'display_name',
        'image_name': 'image_name',
        'image_display_name': 'image_display_name',
        'image_id': 'image_id',
        'memory_pool_name': 'memory_pool_name',
        'memory_pool_display_name': 'memory_pool_display_name',
        'status': 'status',
        'entrypoint': 'entrypoint',
        'ip': 'ip',
        'udp': 'udp',
        'use_public_ip': 'use_public_ip',
        'docker_id': 'docker_id',
        'play_mode': 'play_mode',
        'server_id': 'server_id',
        'exit_code': 'exit_code',
        'created_at': 'created_at',
        'modified_at': 'modified_at',
        'started_at': 'started_at',
        'exit_at': 'exit_at',
        'ports': 'ports',
        'volumes': 'volumes',
        'envvars': 'envvars',
        'args': 'args',
        'links': 'links',
        'is_running': 'is_running',
        'should_run': 'should_run',
        'comment': 'comment',
        'dgroup_name': 'dgroup_name',
        'dgroup_display_name': 'dgroup_display_name'
    }

    def __init__(self, name=None, display_name=None, image_name=None, image_display_name=None, image_id=None, memory_pool_name=None, memory_pool_display_name=None, status=None, entrypoint=None, ip=None, udp=None, use_public_ip=None, docker_id=None, play_mode=None, server_id=None, exit_code=None, created_at=None, modified_at=None, started_at=None, exit_at=None, ports=None, volumes=None, envvars=None, args=None, links=None, is_running=None, should_run=None, comment=None, dgroup_name=None, dgroup_display_name=None, _configuration=None):  # noqa: E501
        """InlineResponse2008ResponseContainer - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._display_name = None
        self._image_name = None
        self._image_display_name = None
        self._image_id = None
        self._memory_pool_name = None
        self._memory_pool_display_name = None
        self._status = None
        self._entrypoint = None
        self._ip = None
        self._udp = None
        self._use_public_ip = None
        self._docker_id = None
        self._play_mode = None
        self._server_id = None
        self._exit_code = None
        self._created_at = None
        self._modified_at = None
        self._started_at = None
        self._exit_at = None
        self._ports = None
        self._volumes = None
        self._envvars = None
        self._args = None
        self._links = None
        self._is_running = None
        self._should_run = None
        self._comment = None
        self._dgroup_name = None
        self._dgroup_display_name = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if display_name is not None:
            self.display_name = display_name
        if image_name is not None:
            self.image_name = image_name
        if image_display_name is not None:
            self.image_display_name = image_display_name
        if image_id is not None:
            self.image_id = image_id
        if memory_pool_name is not None:
            self.memory_pool_name = memory_pool_name
        if memory_pool_display_name is not None:
            self.memory_pool_display_name = memory_pool_display_name
        if status is not None:
            self.status = status
        if entrypoint is not None:
            self.entrypoint = entrypoint
        if ip is not None:
            self.ip = ip
        if udp is not None:
            self.udp = udp
        if use_public_ip is not None:
            self.use_public_ip = use_public_ip
        if docker_id is not None:
            self.docker_id = docker_id
        if play_mode is not None:
            self.play_mode = play_mode
        if server_id is not None:
            self.server_id = server_id
        if exit_code is not None:
            self.exit_code = exit_code
        if created_at is not None:
            self.created_at = created_at
        if modified_at is not None:
            self.modified_at = modified_at
        if started_at is not None:
            self.started_at = started_at
        if exit_at is not None:
            self.exit_at = exit_at
        if ports is not None:
            self.ports = ports
        if volumes is not None:
            self.volumes = volumes
        if envvars is not None:
            self.envvars = envvars
        if args is not None:
            self.args = args
        if links is not None:
            self.links = links
        if is_running is not None:
            self.is_running = is_running
        if should_run is not None:
            self.should_run = should_run
        if comment is not None:
            self.comment = comment
        if dgroup_name is not None:
            self.dgroup_name = dgroup_name
        if dgroup_display_name is not None:
            self.dgroup_display_name = dgroup_display_name

    @property
    def name(self):
        """Gets the name of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse2008ResponseContainer.


        :param name: The name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def display_name(self):
        """Gets the display_name of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The display_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this InlineResponse2008ResponseContainer.


        :param display_name: The display_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def image_name(self):
        """Gets the image_name of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The image_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name):
        """Sets the image_name of this InlineResponse2008ResponseContainer.


        :param image_name: The image_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._image_name = image_name

    @property
    def image_display_name(self):
        """Gets the image_display_name of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The image_display_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._image_display_name

    @image_display_name.setter
    def image_display_name(self, image_display_name):
        """Sets the image_display_name of this InlineResponse2008ResponseContainer.


        :param image_display_name: The image_display_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._image_display_name = image_display_name

    @property
    def image_id(self):
        """Gets the image_id of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The image_id of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: int
        """
        return self._image_id

    @image_id.setter
    def image_id(self, image_id):
        """Sets the image_id of this InlineResponse2008ResponseContainer.


        :param image_id: The image_id of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: int
        """

        self._image_id = image_id

    @property
    def memory_pool_name(self):
        """Gets the memory_pool_name of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The memory_pool_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._memory_pool_name

    @memory_pool_name.setter
    def memory_pool_name(self, memory_pool_name):
        """Sets the memory_pool_name of this InlineResponse2008ResponseContainer.


        :param memory_pool_name: The memory_pool_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._memory_pool_name = memory_pool_name

    @property
    def memory_pool_display_name(self):
        """Gets the memory_pool_display_name of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The memory_pool_display_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._memory_pool_display_name

    @memory_pool_display_name.setter
    def memory_pool_display_name(self, memory_pool_display_name):
        """Sets the memory_pool_display_name of this InlineResponse2008ResponseContainer.


        :param memory_pool_display_name: The memory_pool_display_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._memory_pool_display_name = memory_pool_display_name

    @property
    def status(self):
        """Gets the status of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The status of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InlineResponse2008ResponseContainer.


        :param status: The status of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def entrypoint(self):
        """Gets the entrypoint of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The entrypoint of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._entrypoint

    @entrypoint.setter
    def entrypoint(self, entrypoint):
        """Sets the entrypoint of this InlineResponse2008ResponseContainer.


        :param entrypoint: The entrypoint of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._entrypoint = entrypoint

    @property
    def ip(self):
        """Gets the ip of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The ip of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._ip

    @ip.setter
    def ip(self, ip):
        """Sets the ip of this InlineResponse2008ResponseContainer.


        :param ip: The ip of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._ip = ip

    @property
    def udp(self):
        """Gets the udp of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The udp of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._udp

    @udp.setter
    def udp(self, udp):
        """Sets the udp of this InlineResponse2008ResponseContainer.


        :param udp: The udp of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._udp = udp

    @property
    def use_public_ip(self):
        """Gets the use_public_ip of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The use_public_ip of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: int
        """
        return self._use_public_ip

    @use_public_ip.setter
    def use_public_ip(self, use_public_ip):
        """Sets the use_public_ip of this InlineResponse2008ResponseContainer.


        :param use_public_ip: The use_public_ip of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: int
        """

        self._use_public_ip = use_public_ip

    @property
    def docker_id(self):
        """Gets the docker_id of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The docker_id of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._docker_id

    @docker_id.setter
    def docker_id(self, docker_id):
        """Sets the docker_id of this InlineResponse2008ResponseContainer.


        :param docker_id: The docker_id of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._docker_id = docker_id

    @property
    def play_mode(self):
        """Gets the play_mode of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The play_mode of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: int
        """
        return self._play_mode

    @play_mode.setter
    def play_mode(self, play_mode):
        """Sets the play_mode of this InlineResponse2008ResponseContainer.


        :param play_mode: The play_mode of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: int
        """

        self._play_mode = play_mode

    @property
    def server_id(self):
        """Gets the server_id of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The server_id of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: int
        """
        return self._server_id

    @server_id.setter
    def server_id(self, server_id):
        """Sets the server_id of this InlineResponse2008ResponseContainer.


        :param server_id: The server_id of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: int
        """

        self._server_id = server_id

    @property
    def exit_code(self):
        """Gets the exit_code of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The exit_code of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: int
        """
        return self._exit_code

    @exit_code.setter
    def exit_code(self, exit_code):
        """Sets the exit_code of this InlineResponse2008ResponseContainer.


        :param exit_code: The exit_code of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: int
        """

        self._exit_code = exit_code

    @property
    def created_at(self):
        """Gets the created_at of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The created_at of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InlineResponse2008ResponseContainer.


        :param created_at: The created_at of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def modified_at(self):
        """Gets the modified_at of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The modified_at of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this InlineResponse2008ResponseContainer.


        :param modified_at: The modified_at of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._modified_at = modified_at

    @property
    def started_at(self):
        """Gets the started_at of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The started_at of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._started_at

    @started_at.setter
    def started_at(self, started_at):
        """Sets the started_at of this InlineResponse2008ResponseContainer.


        :param started_at: The started_at of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._started_at = started_at

    @property
    def exit_at(self):
        """Gets the exit_at of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The exit_at of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._exit_at

    @exit_at.setter
    def exit_at(self, exit_at):
        """Sets the exit_at of this InlineResponse2008ResponseContainer.


        :param exit_at: The exit_at of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._exit_at = exit_at

    @property
    def ports(self):
        """Gets the ports of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The ports of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: list[str]
        """
        return self._ports

    @ports.setter
    def ports(self, ports):
        """Sets the ports of this InlineResponse2008ResponseContainer.


        :param ports: The ports of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: list[str]
        """

        self._ports = ports

    @property
    def volumes(self):
        """Gets the volumes of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The volumes of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: list[InlineResponse2006ResponseVolumes]
        """
        return self._volumes

    @volumes.setter
    def volumes(self, volumes):
        """Sets the volumes of this InlineResponse2008ResponseContainer.


        :param volumes: The volumes of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: list[InlineResponse2006ResponseVolumes]
        """

        self._volumes = volumes

    @property
    def envvars(self):
        """Gets the envvars of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The envvars of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: list[str]
        """
        return self._envvars

    @envvars.setter
    def envvars(self, envvars):
        """Sets the envvars of this InlineResponse2008ResponseContainer.


        :param envvars: The envvars of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: list[str]
        """

        self._envvars = envvars

    @property
    def args(self):
        """Gets the args of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The args of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: list[str]
        """
        return self._args

    @args.setter
    def args(self, args):
        """Sets the args of this InlineResponse2008ResponseContainer.


        :param args: The args of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: list[str]
        """

        self._args = args

    @property
    def links(self):
        """Gets the links of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The links of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: list[str]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this InlineResponse2008ResponseContainer.


        :param links: The links of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: list[str]
        """

        self._links = links

    @property
    def is_running(self):
        """Gets the is_running of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The is_running of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._is_running

    @is_running.setter
    def is_running(self, is_running):
        """Sets the is_running of this InlineResponse2008ResponseContainer.


        :param is_running: The is_running of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._is_running = is_running

    @property
    def should_run(self):
        """Gets the should_run of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The should_run of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._should_run

    @should_run.setter
    def should_run(self, should_run):
        """Sets the should_run of this InlineResponse2008ResponseContainer.


        :param should_run: The should_run of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._should_run = should_run

    @property
    def comment(self):
        """Gets the comment of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The comment of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this InlineResponse2008ResponseContainer.


        :param comment: The comment of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._comment = comment

    @property
    def dgroup_name(self):
        """Gets the dgroup_name of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The dgroup_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._dgroup_name

    @dgroup_name.setter
    def dgroup_name(self, dgroup_name):
        """Sets the dgroup_name of this InlineResponse2008ResponseContainer.


        :param dgroup_name: The dgroup_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._dgroup_name = dgroup_name

    @property
    def dgroup_display_name(self):
        """Gets the dgroup_display_name of this InlineResponse2008ResponseContainer.  # noqa: E501


        :return: The dgroup_display_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :rtype: str
        """
        return self._dgroup_display_name

    @dgroup_display_name.setter
    def dgroup_display_name(self, dgroup_display_name):
        """Sets the dgroup_display_name of this InlineResponse2008ResponseContainer.


        :param dgroup_display_name: The dgroup_display_name of this InlineResponse2008ResponseContainer.  # noqa: E501
        :type: str
        """

        self._dgroup_display_name = dgroup_display_name

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
        if issubclass(InlineResponse2008ResponseContainer, dict):
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
        if not isinstance(other, InlineResponse2008ResponseContainer):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse2008ResponseContainer):
            return True

        return self.to_dict() != other.to_dict()
