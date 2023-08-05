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


class GetVolumeQuota(object):
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
        'scope': 'str',
        'quota_id': 'int',
        'quota_nas': 'str',
        'quota_ad': 'str'
    }

    attribute_map = {
        'scope': 'scope',
        'quota_id': 'quota_id',
        'quota_nas': 'quota_nas',
        'quota_ad': 'quota_ad'
    }

    def __init__(self, scope=None, quota_id=None, quota_nas=None, quota_ad=None, _configuration=None):  # noqa: E501
        """GetVolumeQuota - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._scope = None
        self._quota_id = None
        self._quota_nas = None
        self._quota_ad = None
        self.discriminator = None

        self.scope = scope
        if quota_id is not None:
            self.quota_id = quota_id
        if quota_nas is not None:
            self.quota_nas = quota_nas
        if quota_ad is not None:
            self.quota_ad = quota_ad

    @property
    def scope(self):
        """Gets the scope of this GetVolumeQuota.  # noqa: E501

        quota's type  # noqa: E501

        :return: The scope of this GetVolumeQuota.  # noqa: E501
        :rtype: str
        """
        return self._scope

    @scope.setter
    def scope(self, scope):
        """Sets the scope of this GetVolumeQuota.

        quota's type  # noqa: E501

        :param scope: The scope of this GetVolumeQuota.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and scope is None:
            raise ValueError("Invalid value for `scope`, must not be `None`")  # noqa: E501
        allowed_values = ["user", "group", "project"]  # noqa: E501
        if (self._configuration.client_side_validation and
                scope not in allowed_values):
            raise ValueError(
                "Invalid value for `scope` ({0}), must be one of {1}"  # noqa: E501
                .format(scope, allowed_values)
            )

        self._scope = scope

    @property
    def quota_id(self):
        """Gets the quota_id of this GetVolumeQuota.  # noqa: E501

        NFS id / Project Id  # noqa: E501

        :return: The quota_id of this GetVolumeQuota.  # noqa: E501
        :rtype: int
        """
        return self._quota_id

    @quota_id.setter
    def quota_id(self, quota_id):
        """Sets the quota_id of this GetVolumeQuota.

        NFS id / Project Id  # noqa: E501

        :param quota_id: The quota_id of this GetVolumeQuota.  # noqa: E501
        :type: int
        """

        self._quota_id = quota_id

    @property
    def quota_nas(self):
        """Gets the quota_nas of this GetVolumeQuota.  # noqa: E501

        NAS name  # noqa: E501

        :return: The quota_nas of this GetVolumeQuota.  # noqa: E501
        :rtype: str
        """
        return self._quota_nas

    @quota_nas.setter
    def quota_nas(self, quota_nas):
        """Sets the quota_nas of this GetVolumeQuota.

        NAS name  # noqa: E501

        :param quota_nas: The quota_nas of this GetVolumeQuota.  # noqa: E501
        :type: str
        """

        self._quota_nas = quota_nas

    @property
    def quota_ad(self):
        """Gets the quota_ad of this GetVolumeQuota.  # noqa: E501

        Active directry name  # noqa: E501

        :return: The quota_ad of this GetVolumeQuota.  # noqa: E501
        :rtype: str
        """
        return self._quota_ad

    @quota_ad.setter
    def quota_ad(self, quota_ad):
        """Sets the quota_ad of this GetVolumeQuota.

        Active directry name  # noqa: E501

        :param quota_ad: The quota_ad of this GetVolumeQuota.  # noqa: E501
        :type: str
        """

        self._quota_ad = quota_ad

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
        if issubclass(GetVolumeQuota, dict):
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
        if not isinstance(other, GetVolumeQuota):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GetVolumeQuota):
            return True

        return self.to_dict() != other.to_dict()
