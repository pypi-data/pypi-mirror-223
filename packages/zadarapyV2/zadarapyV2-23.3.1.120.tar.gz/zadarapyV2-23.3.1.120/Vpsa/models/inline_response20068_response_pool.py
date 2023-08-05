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


class InlineResponse20068ResponsePool(object):
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
        'status': 'str',
        'capacity': 'int',
        'available_capacity': 'float',
        'version': 'int',
        'data_type': 'str',
        'mount_sync': 'str',
        'access_time_update': 'str',
        'raid_group_name': 'str',
        'mode': 'str',
        'stripe_size': 'int',
        'cache': 'str',
        'cow_cache': 'str',
        'capacity_mode': 'str',
        'capacity_history': 'int',
        'alert_mode': 'int',
        'protected_mode': 'int',
        'emergency_mode': 'int',
        'chunk_size': 'int',
        'type': 'str',
        'created_at': 'str',
        'modified_at': 'str',
        'metadata_capacity': 'float',
        'av_protected_capacity': 'float',
        'provisioned_capacity': 'float',
        'ssd': 'InlineResponse20068ResponsePoolSsd',
        'hdd': 'InlineResponse20068ResponsePoolSsd',
        'obs': 'InlineResponse20068ResponsePoolSsd',
        'antivirus': 'str',
        'maintenance_mode': 'str',
        'cool_off_hours': 'int',
        'thresholds': 'str',
        'comment': 'str'
    }

    attribute_map = {
        'name': 'name',
        'display_name': 'display_name',
        'status': 'status',
        'capacity': 'capacity',
        'available_capacity': 'available_capacity',
        'version': 'version',
        'data_type': 'data_type',
        'mount_sync': 'mount_sync',
        'access_time_update': 'access_time_update',
        'raid_group_name': 'raid_group_name',
        'mode': 'mode',
        'stripe_size': 'stripe_size',
        'cache': 'cache',
        'cow_cache': 'cow_cache',
        'capacity_mode': 'capacity_mode',
        'capacity_history': 'capacity_history',
        'alert_mode': 'alert_mode',
        'protected_mode': 'protected_mode',
        'emergency_mode': 'emergency_mode',
        'chunk_size': 'chunk_size',
        'type': 'type',
        'created_at': 'created_at',
        'modified_at': 'modified_at',
        'metadata_capacity': 'metadata_capacity',
        'av_protected_capacity': 'av_protected_capacity',
        'provisioned_capacity': 'provisioned_capacity',
        'ssd': 'ssd',
        'hdd': 'hdd',
        'obs': 'obs',
        'antivirus': 'antivirus',
        'maintenance_mode': 'maintenance_mode',
        'cool_off_hours': 'cool_off_hours',
        'thresholds': 'thresholds',
        'comment': 'comment'
    }

    def __init__(self, name=None, display_name=None, status=None, capacity=None, available_capacity=None, version=None, data_type=None, mount_sync=None, access_time_update=None, raid_group_name=None, mode=None, stripe_size=None, cache=None, cow_cache=None, capacity_mode=None, capacity_history=None, alert_mode=None, protected_mode=None, emergency_mode=None, chunk_size=None, type=None, created_at=None, modified_at=None, metadata_capacity=None, av_protected_capacity=None, provisioned_capacity=None, ssd=None, hdd=None, obs=None, antivirus=None, maintenance_mode=None, cool_off_hours=None, thresholds=None, comment=None, _configuration=None):  # noqa: E501
        """InlineResponse20068ResponsePool - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._display_name = None
        self._status = None
        self._capacity = None
        self._available_capacity = None
        self._version = None
        self._data_type = None
        self._mount_sync = None
        self._access_time_update = None
        self._raid_group_name = None
        self._mode = None
        self._stripe_size = None
        self._cache = None
        self._cow_cache = None
        self._capacity_mode = None
        self._capacity_history = None
        self._alert_mode = None
        self._protected_mode = None
        self._emergency_mode = None
        self._chunk_size = None
        self._type = None
        self._created_at = None
        self._modified_at = None
        self._metadata_capacity = None
        self._av_protected_capacity = None
        self._provisioned_capacity = None
        self._ssd = None
        self._hdd = None
        self._obs = None
        self._antivirus = None
        self._maintenance_mode = None
        self._cool_off_hours = None
        self._thresholds = None
        self._comment = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if display_name is not None:
            self.display_name = display_name
        if status is not None:
            self.status = status
        if capacity is not None:
            self.capacity = capacity
        if available_capacity is not None:
            self.available_capacity = available_capacity
        if version is not None:
            self.version = version
        if data_type is not None:
            self.data_type = data_type
        if mount_sync is not None:
            self.mount_sync = mount_sync
        if access_time_update is not None:
            self.access_time_update = access_time_update
        if raid_group_name is not None:
            self.raid_group_name = raid_group_name
        if mode is not None:
            self.mode = mode
        if stripe_size is not None:
            self.stripe_size = stripe_size
        if cache is not None:
            self.cache = cache
        if cow_cache is not None:
            self.cow_cache = cow_cache
        if capacity_mode is not None:
            self.capacity_mode = capacity_mode
        if capacity_history is not None:
            self.capacity_history = capacity_history
        if alert_mode is not None:
            self.alert_mode = alert_mode
        if protected_mode is not None:
            self.protected_mode = protected_mode
        if emergency_mode is not None:
            self.emergency_mode = emergency_mode
        if chunk_size is not None:
            self.chunk_size = chunk_size
        if type is not None:
            self.type = type
        if created_at is not None:
            self.created_at = created_at
        if modified_at is not None:
            self.modified_at = modified_at
        if metadata_capacity is not None:
            self.metadata_capacity = metadata_capacity
        if av_protected_capacity is not None:
            self.av_protected_capacity = av_protected_capacity
        if provisioned_capacity is not None:
            self.provisioned_capacity = provisioned_capacity
        if ssd is not None:
            self.ssd = ssd
        if hdd is not None:
            self.hdd = hdd
        if obs is not None:
            self.obs = obs
        if antivirus is not None:
            self.antivirus = antivirus
        if maintenance_mode is not None:
            self.maintenance_mode = maintenance_mode
        if cool_off_hours is not None:
            self.cool_off_hours = cool_off_hours
        if thresholds is not None:
            self.thresholds = thresholds
        if comment is not None:
            self.comment = comment

    @property
    def name(self):
        """Gets the name of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The name of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse20068ResponsePool.


        :param name: The name of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def display_name(self):
        """Gets the display_name of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The display_name of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this InlineResponse20068ResponsePool.


        :param display_name: The display_name of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def status(self):
        """Gets the status of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The status of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this InlineResponse20068ResponsePool.


        :param status: The status of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def capacity(self):
        """Gets the capacity of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The capacity of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: int
        """
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        """Sets the capacity of this InlineResponse20068ResponsePool.


        :param capacity: The capacity of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: int
        """
        if (self._configuration.client_side_validation and
                capacity is not None and capacity < 1):  # noqa: E501
            raise ValueError("Invalid value for `capacity`, must be a value greater than or equal to `1`")  # noqa: E501

        self._capacity = capacity

    @property
    def available_capacity(self):
        """Gets the available_capacity of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The available_capacity of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: float
        """
        return self._available_capacity

    @available_capacity.setter
    def available_capacity(self, available_capacity):
        """Sets the available_capacity of this InlineResponse20068ResponsePool.


        :param available_capacity: The available_capacity of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: float
        """

        self._available_capacity = available_capacity

    @property
    def version(self):
        """Gets the version of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The version of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this InlineResponse20068ResponsePool.


        :param version: The version of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: int
        """

        self._version = version

    @property
    def data_type(self):
        """Gets the data_type of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The data_type of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        """Sets the data_type of this InlineResponse20068ResponsePool.


        :param data_type: The data_type of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._data_type = data_type

    @property
    def mount_sync(self):
        """Gets the mount_sync of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The mount_sync of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._mount_sync

    @mount_sync.setter
    def mount_sync(self, mount_sync):
        """Sets the mount_sync of this InlineResponse20068ResponsePool.


        :param mount_sync: The mount_sync of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._mount_sync = mount_sync

    @property
    def access_time_update(self):
        """Gets the access_time_update of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The access_time_update of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._access_time_update

    @access_time_update.setter
    def access_time_update(self, access_time_update):
        """Sets the access_time_update of this InlineResponse20068ResponsePool.


        :param access_time_update: The access_time_update of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._access_time_update = access_time_update

    @property
    def raid_group_name(self):
        """Gets the raid_group_name of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The raid_group_name of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._raid_group_name

    @raid_group_name.setter
    def raid_group_name(self, raid_group_name):
        """Sets the raid_group_name of this InlineResponse20068ResponsePool.


        :param raid_group_name: The raid_group_name of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._raid_group_name = raid_group_name

    @property
    def mode(self):
        """Gets the mode of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The mode of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """Sets the mode of this InlineResponse20068ResponsePool.


        :param mode: The mode of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._mode = mode

    @property
    def stripe_size(self):
        """Gets the stripe_size of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The stripe_size of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: int
        """
        return self._stripe_size

    @stripe_size.setter
    def stripe_size(self, stripe_size):
        """Sets the stripe_size of this InlineResponse20068ResponsePool.


        :param stripe_size: The stripe_size of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: int
        """

        self._stripe_size = stripe_size

    @property
    def cache(self):
        """Gets the cache of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The cache of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._cache

    @cache.setter
    def cache(self, cache):
        """Sets the cache of this InlineResponse20068ResponsePool.


        :param cache: The cache of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._cache = cache

    @property
    def cow_cache(self):
        """Gets the cow_cache of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The cow_cache of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._cow_cache

    @cow_cache.setter
    def cow_cache(self, cow_cache):
        """Sets the cow_cache of this InlineResponse20068ResponsePool.


        :param cow_cache: The cow_cache of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._cow_cache = cow_cache

    @property
    def capacity_mode(self):
        """Gets the capacity_mode of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The capacity_mode of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._capacity_mode

    @capacity_mode.setter
    def capacity_mode(self, capacity_mode):
        """Sets the capacity_mode of this InlineResponse20068ResponsePool.


        :param capacity_mode: The capacity_mode of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._capacity_mode = capacity_mode

    @property
    def capacity_history(self):
        """Gets the capacity_history of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The capacity_history of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: int
        """
        return self._capacity_history

    @capacity_history.setter
    def capacity_history(self, capacity_history):
        """Sets the capacity_history of this InlineResponse20068ResponsePool.


        :param capacity_history: The capacity_history of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: int
        """

        self._capacity_history = capacity_history

    @property
    def alert_mode(self):
        """Gets the alert_mode of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The alert_mode of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: int
        """
        return self._alert_mode

    @alert_mode.setter
    def alert_mode(self, alert_mode):
        """Sets the alert_mode of this InlineResponse20068ResponsePool.


        :param alert_mode: The alert_mode of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: int
        """

        self._alert_mode = alert_mode

    @property
    def protected_mode(self):
        """Gets the protected_mode of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The protected_mode of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: int
        """
        return self._protected_mode

    @protected_mode.setter
    def protected_mode(self, protected_mode):
        """Sets the protected_mode of this InlineResponse20068ResponsePool.


        :param protected_mode: The protected_mode of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: int
        """

        self._protected_mode = protected_mode

    @property
    def emergency_mode(self):
        """Gets the emergency_mode of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The emergency_mode of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: int
        """
        return self._emergency_mode

    @emergency_mode.setter
    def emergency_mode(self, emergency_mode):
        """Sets the emergency_mode of this InlineResponse20068ResponsePool.


        :param emergency_mode: The emergency_mode of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: int
        """

        self._emergency_mode = emergency_mode

    @property
    def chunk_size(self):
        """Gets the chunk_size of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The chunk_size of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: int
        """
        return self._chunk_size

    @chunk_size.setter
    def chunk_size(self, chunk_size):
        """Sets the chunk_size of this InlineResponse20068ResponsePool.


        :param chunk_size: The chunk_size of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: int
        """

        self._chunk_size = chunk_size

    @property
    def type(self):
        """Gets the type of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The type of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this InlineResponse20068ResponsePool.


        :param type: The type of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def created_at(self):
        """Gets the created_at of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The created_at of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InlineResponse20068ResponsePool.


        :param created_at: The created_at of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def modified_at(self):
        """Gets the modified_at of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The modified_at of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this InlineResponse20068ResponsePool.


        :param modified_at: The modified_at of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._modified_at = modified_at

    @property
    def metadata_capacity(self):
        """Gets the metadata_capacity of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The metadata_capacity of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: float
        """
        return self._metadata_capacity

    @metadata_capacity.setter
    def metadata_capacity(self, metadata_capacity):
        """Sets the metadata_capacity of this InlineResponse20068ResponsePool.


        :param metadata_capacity: The metadata_capacity of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: float
        """

        self._metadata_capacity = metadata_capacity

    @property
    def av_protected_capacity(self):
        """Gets the av_protected_capacity of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The av_protected_capacity of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: float
        """
        return self._av_protected_capacity

    @av_protected_capacity.setter
    def av_protected_capacity(self, av_protected_capacity):
        """Sets the av_protected_capacity of this InlineResponse20068ResponsePool.


        :param av_protected_capacity: The av_protected_capacity of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: float
        """

        self._av_protected_capacity = av_protected_capacity

    @property
    def provisioned_capacity(self):
        """Gets the provisioned_capacity of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The provisioned_capacity of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: float
        """
        return self._provisioned_capacity

    @provisioned_capacity.setter
    def provisioned_capacity(self, provisioned_capacity):
        """Sets the provisioned_capacity of this InlineResponse20068ResponsePool.


        :param provisioned_capacity: The provisioned_capacity of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: float
        """

        self._provisioned_capacity = provisioned_capacity

    @property
    def ssd(self):
        """Gets the ssd of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The ssd of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: InlineResponse20068ResponsePoolSsd
        """
        return self._ssd

    @ssd.setter
    def ssd(self, ssd):
        """Sets the ssd of this InlineResponse20068ResponsePool.


        :param ssd: The ssd of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: InlineResponse20068ResponsePoolSsd
        """

        self._ssd = ssd

    @property
    def hdd(self):
        """Gets the hdd of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The hdd of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: InlineResponse20068ResponsePoolSsd
        """
        return self._hdd

    @hdd.setter
    def hdd(self, hdd):
        """Sets the hdd of this InlineResponse20068ResponsePool.


        :param hdd: The hdd of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: InlineResponse20068ResponsePoolSsd
        """

        self._hdd = hdd

    @property
    def obs(self):
        """Gets the obs of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The obs of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: InlineResponse20068ResponsePoolSsd
        """
        return self._obs

    @obs.setter
    def obs(self, obs):
        """Sets the obs of this InlineResponse20068ResponsePool.


        :param obs: The obs of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: InlineResponse20068ResponsePoolSsd
        """

        self._obs = obs

    @property
    def antivirus(self):
        """Gets the antivirus of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The antivirus of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._antivirus

    @antivirus.setter
    def antivirus(self, antivirus):
        """Sets the antivirus of this InlineResponse20068ResponsePool.


        :param antivirus: The antivirus of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._antivirus = antivirus

    @property
    def maintenance_mode(self):
        """Gets the maintenance_mode of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The maintenance_mode of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._maintenance_mode

    @maintenance_mode.setter
    def maintenance_mode(self, maintenance_mode):
        """Sets the maintenance_mode of this InlineResponse20068ResponsePool.


        :param maintenance_mode: The maintenance_mode of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._maintenance_mode = maintenance_mode

    @property
    def cool_off_hours(self):
        """Gets the cool_off_hours of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The cool_off_hours of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: int
        """
        return self._cool_off_hours

    @cool_off_hours.setter
    def cool_off_hours(self, cool_off_hours):
        """Sets the cool_off_hours of this InlineResponse20068ResponsePool.


        :param cool_off_hours: The cool_off_hours of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: int
        """

        self._cool_off_hours = cool_off_hours

    @property
    def thresholds(self):
        """Gets the thresholds of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The thresholds of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._thresholds

    @thresholds.setter
    def thresholds(self, thresholds):
        """Sets the thresholds of this InlineResponse20068ResponsePool.


        :param thresholds: The thresholds of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._thresholds = thresholds

    @property
    def comment(self):
        """Gets the comment of this InlineResponse20068ResponsePool.  # noqa: E501


        :return: The comment of this InlineResponse20068ResponsePool.  # noqa: E501
        :rtype: str
        """
        return self._comment

    @comment.setter
    def comment(self, comment):
        """Sets the comment of this InlineResponse20068ResponsePool.


        :param comment: The comment of this InlineResponse20068ResponsePool.  # noqa: E501
        :type: str
        """

        self._comment = comment

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
        if issubclass(InlineResponse20068ResponsePool, dict):
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
        if not isinstance(other, InlineResponse20068ResponsePool):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20068ResponsePool):
            return True

        return self.to_dict() != other.to_dict()
