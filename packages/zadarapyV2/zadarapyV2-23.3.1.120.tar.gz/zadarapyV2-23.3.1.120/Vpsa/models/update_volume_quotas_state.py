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


class UpdateVolumeQuotasState(object):
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
        'uquota': 'bool',
        'gquota': 'bool',
        'pquota': 'bool',
        'force': 'str'
    }

    attribute_map = {
        'uquota': 'uquota',
        'gquota': 'gquota',
        'pquota': 'pquota',
        'force': 'force'
    }

    def __init__(self, uquota=None, gquota=None, pquota=None, force=None, _configuration=None):  # noqa: E501
        """UpdateVolumeQuotasState - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._uquota = None
        self._gquota = None
        self._pquota = None
        self._force = None
        self.discriminator = None

        if uquota is not None:
            self.uquota = uquota
        if gquota is not None:
            self.gquota = gquota
        if pquota is not None:
            self.pquota = pquota
        if force is not None:
            self.force = force

    @property
    def uquota(self):
        """Gets the uquota of this UpdateVolumeQuotasState.  # noqa: E501

        set user quota state  # noqa: E501

        :return: The uquota of this UpdateVolumeQuotasState.  # noqa: E501
        :rtype: bool
        """
        return self._uquota

    @uquota.setter
    def uquota(self, uquota):
        """Sets the uquota of this UpdateVolumeQuotasState.

        set user quota state  # noqa: E501

        :param uquota: The uquota of this UpdateVolumeQuotasState.  # noqa: E501
        :type: bool
        """

        self._uquota = uquota

    @property
    def gquota(self):
        """Gets the gquota of this UpdateVolumeQuotasState.  # noqa: E501

        set group quota state  # noqa: E501

        :return: The gquota of this UpdateVolumeQuotasState.  # noqa: E501
        :rtype: bool
        """
        return self._gquota

    @gquota.setter
    def gquota(self, gquota):
        """Sets the gquota of this UpdateVolumeQuotasState.

        set group quota state  # noqa: E501

        :param gquota: The gquota of this UpdateVolumeQuotasState.  # noqa: E501
        :type: bool
        """

        self._gquota = gquota

    @property
    def pquota(self):
        """Gets the pquota of this UpdateVolumeQuotasState.  # noqa: E501

        set group quota state  # noqa: E501

        :return: The pquota of this UpdateVolumeQuotasState.  # noqa: E501
        :rtype: bool
        """
        return self._pquota

    @pquota.setter
    def pquota(self, pquota):
        """Sets the pquota of this UpdateVolumeQuotasState.

        set group quota state  # noqa: E501

        :param pquota: The pquota of this UpdateVolumeQuotasState.  # noqa: E501
        :type: bool
        """

        self._pquota = pquota

    @property
    def force(self):
        """Gets the force of this UpdateVolumeQuotasState.  # noqa: E501

        Force quota state change (skip warnings)  # noqa: E501

        :return: The force of this UpdateVolumeQuotasState.  # noqa: E501
        :rtype: str
        """
        return self._force

    @force.setter
    def force(self, force):
        """Sets the force of this UpdateVolumeQuotasState.

        Force quota state change (skip warnings)  # noqa: E501

        :param force: The force of this UpdateVolumeQuotasState.  # noqa: E501
        :type: str
        """
        allowed_values = ["YES", "NO"]  # noqa: E501
        if (self._configuration.client_side_validation and
                force not in allowed_values):
            raise ValueError(
                "Invalid value for `force` ({0}), must be one of {1}"  # noqa: E501
                .format(force, allowed_values)
            )

        self._force = force

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
        if issubclass(UpdateVolumeQuotasState, dict):
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
        if not isinstance(other, UpdateVolumeQuotasState):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateVolumeQuotasState):
            return True

        return self.to_dict() != other.to_dict()
