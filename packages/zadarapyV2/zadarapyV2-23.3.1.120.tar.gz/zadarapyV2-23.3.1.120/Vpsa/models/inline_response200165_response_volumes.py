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


class InlineResponse200165ResponseVolumes(object):
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
        'cg_display_name': 'str',
        'cg_name': 'str',
        'cg_user_created': 'str',
        'pool_display_name': 'str',
        'pool_name': 'str',
        'status': 'str',
        'virtual_capacity': 'int',
        'server_name': 'str',
        'data_type': 'str',
        'thin': 'str',
        'encryption': 'str',
        'access_type': 'str',
        'read_only': 'str',
        'export_name': 'str',
        'mount_sync': 'str',
        'atime_update': 'str',
        'target': 'str',
        'lun': 'str',
        'cache': 'str',
        'read_iops_limit': 'str',
        'read_mbps_limit': 'str',
        'write_iops_limit': 'str',
        'write_mbps_limit': 'str',
        'created_at': 'str',
        'modified_at': 'str'
    }

    attribute_map = {
        'name': 'name',
        'display_name': 'display_name',
        'cg_display_name': 'cg_display_name',
        'cg_name': 'cg_name',
        'cg_user_created': 'cg_user_created',
        'pool_display_name': 'pool_display_name',
        'pool_name': 'pool_name',
        'status': 'status',
        'virtual_capacity': 'virtual_capacity',
        'server_name': 'server_name',
        'data_type': 'data_type',
        'thin': 'thin',
        'encryption': 'encryption',
        'access_type': 'access_type',
        'read_only': 'read_only',
        'export_name': 'export_name',
        'mount_sync': 'mount_sync',
        'atime_update': 'atime_update',
        'target': 'target',
        'lun': 'lun',
        'cache': 'cache',
        'read_iops_limit': 'read_iops_limit',
        'read_mbps_limit': 'read_mbps_limit',
        'write_iops_limit': 'write_iops_limit',
        'write_mbps_limit': 'write_mbps_limit',
        'created_at': 'created_at',
        'modified_at': 'modified_at'
    }

    def __init__(self, name=None, display_name=None, cg_display_name=None, cg_name=None, cg_user_created=None, pool_display_name=None, pool_name=None, status=None, virtual_capacity=None, server_name=None, data_type=None, thin=None, encryption=None, access_type=None, read_only=None, export_name=None, mount_sync=None, atime_update=None, target=None, lun=None, cache=None, read_iops_limit=None, read_mbps_limit=None, write_iops_limit=None, write_mbps_limit=None, created_at=None, modified_at=None, _configuration=None):  # noqa: E501
        """InlineResponse200165ResponseVolumes - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._display_name = None
        self._cg_display_name = None
        self._cg_name = None
        self._cg_user_created = None
        self._pool_display_name = None
        self._pool_name = None
        self._status = None
        self._virtual_capacity = None
        self._server_name = None
        self._data_type = None
        self._thin = None
        self._encryption = None
        self._access_type = None
        self._read_only = None
        self._export_name = None
        self._mount_sync = None
        self._atime_update = None
        self._target = None
        self._lun = None
        self._cache = None
        self._read_iops_limit = None
        self._read_mbps_limit = None
        self._write_iops_limit = None
        self._write_mbps_limit = None
        self._created_at = None
        self._modified_at = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if display_name is not None:
            self.display_name = display_name
        if cg_display_name is not None:
            self.cg_display_name = cg_display_name
        if cg_name is not None:
            self.cg_name = cg_name
        if cg_user_created is not None:
            self.cg_user_created = cg_user_created
        if pool_display_name is not None:
            self.pool_display_name = pool_display_name
        if pool_name is not None:
            self.pool_name = pool_name
        if status is not None:
            self.status = status
        if virtual_capacity is not None:
            self.virtual_capacity = virtual_capacity
        if server_name is not None:
            self.server_name = server_name
        if data_type is not None:
            self.data_type = data_type
        if thin is not None:
            self.thin = thin
        if encryption is not None:
            self.encryption = encryption
        if access_type is not None:
            self.access_type = access_type
        if read_only is not None:
            self.read_only = read_only
        if export_name is not None:
            self.export_name = export_name
        if mount_sync is not None:
            self.mount_sync = mount_sync
        if atime_update is not None:
            self.atime_update = atime_update
        if target is not None:
            self.target = target
        if lun is not None:
            self.lun = lun
        if cache is not None:
            self.cache = cache
        if read_iops_limit is not None:
            self.read_iops_limit = read_iops_limit
        if read_mbps_limit is not None:
            self.read_mbps_limit = read_mbps_limit
        if write_iops_limit is not None:
            self.write_iops_limit = write_iops_limit
        if write_mbps_limit is not None:
            self.write_mbps_limit = write_mbps_limit
        if created_at is not None:
            self.created_at = created_at
        if modified_at is not None:
            self.modified_at = modified_at

    @property
    def name(self):
        """Gets the name of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse200165ResponseVolumes.


        :param name: The name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def display_name(self):
        """Gets the display_name of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The display_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this InlineResponse200165ResponseVolumes.


        :param display_name: The display_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def cg_display_name(self):
        """Gets the cg_display_name of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The cg_display_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._cg_display_name

    @cg_display_name.setter
    def cg_display_name(self, cg_display_name):
        """Sets the cg_display_name of this InlineResponse200165ResponseVolumes.


        :param cg_display_name: The cg_display_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._cg_display_name = cg_display_name

    @property
    def cg_name(self):
        """Gets the cg_name of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The cg_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._cg_name

    @cg_name.setter
    def cg_name(self, cg_name):
        """Sets the cg_name of this InlineResponse200165ResponseVolumes.


        :param cg_name: The cg_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._cg_name = cg_name

    @property
    def cg_user_created(self):
        """Gets the cg_user_created of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The cg_user_created of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._cg_user_created

    @cg_user_created.setter
    def cg_user_created(self, cg_user_created):
        """Sets the cg_user_created of this InlineResponse200165ResponseVolumes.


        :param cg_user_created: The cg_user_created of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._cg_user_created = cg_user_created

    @property
    def pool_display_name(self):
        """Gets the pool_display_name of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The pool_display_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._pool_display_name

    @pool_display_name.setter
    def pool_display_name(self, pool_display_name):
        """Sets the pool_display_name of this InlineResponse200165ResponseVolumes.


        :param pool_display_name: The pool_display_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._pool_display_name = pool_display_name

    @property
    def pool_name(self):
        """Gets the pool_name of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The pool_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._pool_name

    @pool_name.setter
    def pool_name(self, pool_name):
        """Sets the pool_name of this InlineResponse200165ResponseVolumes.


        :param pool_name: The pool_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._pool_name = pool_name

    @property
    def status(self):
        """Gets the status of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The status of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InlineResponse200165ResponseVolumes.


        :param status: The status of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def virtual_capacity(self):
        """Gets the virtual_capacity of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The virtual_capacity of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: int
        """
        return self._virtual_capacity

    @virtual_capacity.setter
    def virtual_capacity(self, virtual_capacity):
        """Sets the virtual_capacity of this InlineResponse200165ResponseVolumes.


        :param virtual_capacity: The virtual_capacity of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: int
        """

        self._virtual_capacity = virtual_capacity

    @property
    def server_name(self):
        """Gets the server_name of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The server_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._server_name

    @server_name.setter
    def server_name(self, server_name):
        """Sets the server_name of this InlineResponse200165ResponseVolumes.


        :param server_name: The server_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._server_name = server_name

    @property
    def data_type(self):
        """Gets the data_type of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The data_type of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        """Sets the data_type of this InlineResponse200165ResponseVolumes.


        :param data_type: The data_type of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._data_type = data_type

    @property
    def thin(self):
        """Gets the thin of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The thin of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._thin

    @thin.setter
    def thin(self, thin):
        """Sets the thin of this InlineResponse200165ResponseVolumes.


        :param thin: The thin of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._thin = thin

    @property
    def encryption(self):
        """Gets the encryption of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The encryption of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._encryption

    @encryption.setter
    def encryption(self, encryption):
        """Sets the encryption of this InlineResponse200165ResponseVolumes.


        :param encryption: The encryption of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._encryption = encryption

    @property
    def access_type(self):
        """Gets the access_type of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The access_type of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._access_type

    @access_type.setter
    def access_type(self, access_type):
        """Sets the access_type of this InlineResponse200165ResponseVolumes.


        :param access_type: The access_type of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._access_type = access_type

    @property
    def read_only(self):
        """Gets the read_only of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The read_only of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._read_only

    @read_only.setter
    def read_only(self, read_only):
        """Sets the read_only of this InlineResponse200165ResponseVolumes.


        :param read_only: The read_only of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._read_only = read_only

    @property
    def export_name(self):
        """Gets the export_name of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The export_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._export_name

    @export_name.setter
    def export_name(self, export_name):
        """Sets the export_name of this InlineResponse200165ResponseVolumes.


        :param export_name: The export_name of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._export_name = export_name

    @property
    def mount_sync(self):
        """Gets the mount_sync of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The mount_sync of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._mount_sync

    @mount_sync.setter
    def mount_sync(self, mount_sync):
        """Sets the mount_sync of this InlineResponse200165ResponseVolumes.


        :param mount_sync: The mount_sync of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._mount_sync = mount_sync

    @property
    def atime_update(self):
        """Gets the atime_update of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The atime_update of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._atime_update

    @atime_update.setter
    def atime_update(self, atime_update):
        """Sets the atime_update of this InlineResponse200165ResponseVolumes.


        :param atime_update: The atime_update of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._atime_update = atime_update

    @property
    def target(self):
        """Gets the target of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The target of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """Sets the target of this InlineResponse200165ResponseVolumes.


        :param target: The target of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._target = target

    @property
    def lun(self):
        """Gets the lun of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The lun of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._lun

    @lun.setter
    def lun(self, lun):
        """Sets the lun of this InlineResponse200165ResponseVolumes.


        :param lun: The lun of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._lun = lun

    @property
    def cache(self):
        """Gets the cache of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The cache of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._cache

    @cache.setter
    def cache(self, cache):
        """Sets the cache of this InlineResponse200165ResponseVolumes.


        :param cache: The cache of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._cache = cache

    @property
    def read_iops_limit(self):
        """Gets the read_iops_limit of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The read_iops_limit of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._read_iops_limit

    @read_iops_limit.setter
    def read_iops_limit(self, read_iops_limit):
        """Sets the read_iops_limit of this InlineResponse200165ResponseVolumes.


        :param read_iops_limit: The read_iops_limit of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._read_iops_limit = read_iops_limit

    @property
    def read_mbps_limit(self):
        """Gets the read_mbps_limit of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The read_mbps_limit of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._read_mbps_limit

    @read_mbps_limit.setter
    def read_mbps_limit(self, read_mbps_limit):
        """Sets the read_mbps_limit of this InlineResponse200165ResponseVolumes.


        :param read_mbps_limit: The read_mbps_limit of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._read_mbps_limit = read_mbps_limit

    @property
    def write_iops_limit(self):
        """Gets the write_iops_limit of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The write_iops_limit of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._write_iops_limit

    @write_iops_limit.setter
    def write_iops_limit(self, write_iops_limit):
        """Sets the write_iops_limit of this InlineResponse200165ResponseVolumes.


        :param write_iops_limit: The write_iops_limit of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._write_iops_limit = write_iops_limit

    @property
    def write_mbps_limit(self):
        """Gets the write_mbps_limit of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The write_mbps_limit of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._write_mbps_limit

    @write_mbps_limit.setter
    def write_mbps_limit(self, write_mbps_limit):
        """Sets the write_mbps_limit of this InlineResponse200165ResponseVolumes.


        :param write_mbps_limit: The write_mbps_limit of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._write_mbps_limit = write_mbps_limit

    @property
    def created_at(self):
        """Gets the created_at of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The created_at of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InlineResponse200165ResponseVolumes.


        :param created_at: The created_at of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def modified_at(self):
        """Gets the modified_at of this InlineResponse200165ResponseVolumes.  # noqa: E501


        :return: The modified_at of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :rtype: str
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this InlineResponse200165ResponseVolumes.


        :param modified_at: The modified_at of this InlineResponse200165ResponseVolumes.  # noqa: E501
        :type: str
        """

        self._modified_at = modified_at

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
        if issubclass(InlineResponse200165ResponseVolumes, dict):
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
        if not isinstance(other, InlineResponse200165ResponseVolumes):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse200165ResponseVolumes):
            return True

        return self.to_dict() != other.to_dict()
