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


class CreateRosRestoreJob(object):
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
        'mode': 'str',
        'poolname': 'str',
        'volname': 'str',
        'remote_object_store': 'str',
        'key': 'str',
        'local_snapname': 'str',
        'crypt': 'str',
        'dedupe': 'str',
        'compress': 'str'
    }

    attribute_map = {
        'name': 'name',
        'mode': 'mode',
        'poolname': 'poolname',
        'volname': 'volname',
        'remote_object_store': 'remote_object_store',
        'key': 'key',
        'local_snapname': 'local_snapname',
        'crypt': 'crypt',
        'dedupe': 'dedupe',
        'compress': 'compress'
    }

    def __init__(self, name=None, mode=None, poolname=None, volname=None, remote_object_store=None, key=None, local_snapname=None, crypt=None, dedupe=None, compress=None, _configuration=None):  # noqa: E501
        """CreateRosRestoreJob - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._mode = None
        self._poolname = None
        self._volname = None
        self._remote_object_store = None
        self._key = None
        self._local_snapname = None
        self._crypt = None
        self._dedupe = None
        self._compress = None
        self.discriminator = None

        if name is not None:
            self.name = name
        self.mode = mode
        self.poolname = poolname
        self.volname = volname
        self.remote_object_store = remote_object_store
        if key is not None:
            self.key = key
        if local_snapname is not None:
            self.local_snapname = local_snapname
        if crypt is not None:
            self.crypt = crypt
        if dedupe is not None:
            self.dedupe = dedupe
        if compress is not None:
            self.compress = compress

    @property
    def name(self):
        """Gets the name of this CreateRosRestoreJob.  # noqa: E501

        Display Name for object storage restore job  # noqa: E501

        :return: The name of this CreateRosRestoreJob.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateRosRestoreJob.

        Display Name for object storage restore job  # noqa: E501

        :param name: The name of this CreateRosRestoreJob.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def mode(self):
        """Gets the mode of this CreateRosRestoreJob.  # noqa: E501

        mode  # noqa: E501

        :return: The mode of this CreateRosRestoreJob.  # noqa: E501
        :rtype: str
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """Sets the mode of this CreateRosRestoreJob.

        mode  # noqa: E501

        :param mode: The mode of this CreateRosRestoreJob.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and mode is None:
            raise ValueError("Invalid value for `mode`, must not be `None`")  # noqa: E501

        self._mode = mode

    @property
    def poolname(self):
        """Gets the poolname of this CreateRosRestoreJob.  # noqa: E501

        Id of created volume's destination pool  # noqa: E501

        :return: The poolname of this CreateRosRestoreJob.  # noqa: E501
        :rtype: str
        """
        return self._poolname

    @poolname.setter
    def poolname(self, poolname):
        """Sets the poolname of this CreateRosRestoreJob.

        Id of created volume's destination pool  # noqa: E501

        :param poolname: The poolname of this CreateRosRestoreJob.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and poolname is None:
            raise ValueError("Invalid value for `poolname`, must not be `None`")  # noqa: E501
        if (self._configuration.client_side_validation and
                poolname is not None and not re.search(r'^pool-[0-9a-f]{8}$', poolname)):  # noqa: E501
            raise ValueError(r"Invalid value for `poolname`, must be a follow pattern or equal to `/^pool-[0-9a-f]{8}$/`")  # noqa: E501

        self._poolname = poolname

    @property
    def volname(self):
        """Gets the volname of this CreateRosRestoreJob.  # noqa: E501

        Name of Created Volume  # noqa: E501

        :return: The volname of this CreateRosRestoreJob.  # noqa: E501
        :rtype: str
        """
        return self._volname

    @volname.setter
    def volname(self, volname):
        """Sets the volname of this CreateRosRestoreJob.

        Name of Created Volume  # noqa: E501

        :param volname: The volname of this CreateRosRestoreJob.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and volname is None:
            raise ValueError("Invalid value for `volname`, must not be `None`")  # noqa: E501

        self._volname = volname

    @property
    def remote_object_store(self):
        """Gets the remote_object_store of this CreateRosRestoreJob.  # noqa: E501

        Id of object storage destination  # noqa: E501

        :return: The remote_object_store of this CreateRosRestoreJob.  # noqa: E501
        :rtype: str
        """
        return self._remote_object_store

    @remote_object_store.setter
    def remote_object_store(self, remote_object_store):
        """Sets the remote_object_store of this CreateRosRestoreJob.

        Id of object storage destination  # noqa: E501

        :param remote_object_store: The remote_object_store of this CreateRosRestoreJob.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and remote_object_store is None:
            raise ValueError("Invalid value for `remote_object_store`, must not be `None`")  # noqa: E501

        self._remote_object_store = remote_object_store

    @property
    def key(self):
        """Gets the key of this CreateRosRestoreJob.  # noqa: E501

        Object storage key from bucket  # noqa: E501

        :return: The key of this CreateRosRestoreJob.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this CreateRosRestoreJob.

        Object storage key from bucket  # noqa: E501

        :param key: The key of this CreateRosRestoreJob.  # noqa: E501
        :type: str
        """

        self._key = key

    @property
    def local_snapname(self):
        """Gets the local_snapname of this CreateRosRestoreJob.  # noqa: E501

        Object storage local snapshot name  # noqa: E501

        :return: The local_snapname of this CreateRosRestoreJob.  # noqa: E501
        :rtype: str
        """
        return self._local_snapname

    @local_snapname.setter
    def local_snapname(self, local_snapname):
        """Sets the local_snapname of this CreateRosRestoreJob.

        Object storage local snapshot name  # noqa: E501

        :param local_snapname: The local_snapname of this CreateRosRestoreJob.  # noqa: E501
        :type: str
        """

        self._local_snapname = local_snapname

    @property
    def crypt(self):
        """Gets the crypt of this CreateRosRestoreJob.  # noqa: E501

        Enable encryption on volume  # noqa: E501

        :return: The crypt of this CreateRosRestoreJob.  # noqa: E501
        :rtype: str
        """
        return self._crypt

    @crypt.setter
    def crypt(self, crypt):
        """Sets the crypt of this CreateRosRestoreJob.

        Enable encryption on volume  # noqa: E501

        :param crypt: The crypt of this CreateRosRestoreJob.  # noqa: E501
        :type: str
        """

        self._crypt = crypt

    @property
    def dedupe(self):
        """Gets the dedupe of this CreateRosRestoreJob.  # noqa: E501

        Enable Dedupe For Restore Job.  # noqa: E501

        :return: The dedupe of this CreateRosRestoreJob.  # noqa: E501
        :rtype: str
        """
        return self._dedupe

    @dedupe.setter
    def dedupe(self, dedupe):
        """Sets the dedupe of this CreateRosRestoreJob.

        Enable Dedupe For Restore Job.  # noqa: E501

        :param dedupe: The dedupe of this CreateRosRestoreJob.  # noqa: E501
        :type: str
        """

        self._dedupe = dedupe

    @property
    def compress(self):
        """Gets the compress of this CreateRosRestoreJob.  # noqa: E501

        Enable compress or Restore Job.  # noqa: E501

        :return: The compress of this CreateRosRestoreJob.  # noqa: E501
        :rtype: str
        """
        return self._compress

    @compress.setter
    def compress(self, compress):
        """Sets the compress of this CreateRosRestoreJob.

        Enable compress or Restore Job.  # noqa: E501

        :param compress: The compress of this CreateRosRestoreJob.  # noqa: E501
        :type: str
        """

        self._compress = compress

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
        if issubclass(CreateRosRestoreJob, dict):
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
        if not isinstance(other, CreateRosRestoreJob):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateRosRestoreJob):
            return True

        return self.to_dict() != other.to_dict()
