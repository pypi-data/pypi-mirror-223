# coding: utf-8

"""
    Zadara Provisioning Portal API

     # Overview  This document outlines the methods available for creation and high-level administration of Zadara Storage VPSAs via a Zadara Storage Provisioning Portal. This API supports form-encoded requests, and can return either JSON or XML responses.  ## Endpoint  The base URL for the requests is the Provisioning Portal URL you created your VPSA through - for example: https://manage.zadarastorage.com/, and all APIs will be prefixed with /api as noted in the documentation below.  ## Authentication  To use this API, an authentication token is required. The API for retrieving this token can be found below in the Authentication section. You may pass this token in requests either via the the X-Token header or via basic authentication (base64 encoded) in Authorization header.  ## Questions  If you have any questions or need support involving the REST API, please contact for assistance.   # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from ProvisioningPortal.configuration import Configuration


class InlineResponse20023DataCache(object):
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
        'total_partitions': 'int',
        'total_gb': 'int',
        'gb_from_engine': 'int',
        'partitions_from_engine': 'int'
    }

    attribute_map = {
        'total_partitions': 'total_partitions',
        'total_gb': 'total_gb',
        'gb_from_engine': 'gb_from_engine',
        'partitions_from_engine': 'partitions_from_engine'
    }

    def __init__(self, total_partitions=None, total_gb=None, gb_from_engine=None, partitions_from_engine=None, _configuration=None):  # noqa: E501
        """InlineResponse20023DataCache - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._total_partitions = None
        self._total_gb = None
        self._gb_from_engine = None
        self._partitions_from_engine = None
        self.discriminator = None

        if total_partitions is not None:
            self.total_partitions = total_partitions
        if total_gb is not None:
            self.total_gb = total_gb
        if gb_from_engine is not None:
            self.gb_from_engine = gb_from_engine
        if partitions_from_engine is not None:
            self.partitions_from_engine = partitions_from_engine

    @property
    def total_partitions(self):
        """Gets the total_partitions of this InlineResponse20023DataCache.  # noqa: E501


        :return: The total_partitions of this InlineResponse20023DataCache.  # noqa: E501
        :rtype: int
        """
        return self._total_partitions

    @total_partitions.setter
    def total_partitions(self, total_partitions):
        """Sets the total_partitions of this InlineResponse20023DataCache.


        :param total_partitions: The total_partitions of this InlineResponse20023DataCache.  # noqa: E501
        :type: int
        """

        self._total_partitions = total_partitions

    @property
    def total_gb(self):
        """Gets the total_gb of this InlineResponse20023DataCache.  # noqa: E501


        :return: The total_gb of this InlineResponse20023DataCache.  # noqa: E501
        :rtype: int
        """
        return self._total_gb

    @total_gb.setter
    def total_gb(self, total_gb):
        """Sets the total_gb of this InlineResponse20023DataCache.


        :param total_gb: The total_gb of this InlineResponse20023DataCache.  # noqa: E501
        :type: int
        """

        self._total_gb = total_gb

    @property
    def gb_from_engine(self):
        """Gets the gb_from_engine of this InlineResponse20023DataCache.  # noqa: E501


        :return: The gb_from_engine of this InlineResponse20023DataCache.  # noqa: E501
        :rtype: int
        """
        return self._gb_from_engine

    @gb_from_engine.setter
    def gb_from_engine(self, gb_from_engine):
        """Sets the gb_from_engine of this InlineResponse20023DataCache.


        :param gb_from_engine: The gb_from_engine of this InlineResponse20023DataCache.  # noqa: E501
        :type: int
        """

        self._gb_from_engine = gb_from_engine

    @property
    def partitions_from_engine(self):
        """Gets the partitions_from_engine of this InlineResponse20023DataCache.  # noqa: E501


        :return: The partitions_from_engine of this InlineResponse20023DataCache.  # noqa: E501
        :rtype: int
        """
        return self._partitions_from_engine

    @partitions_from_engine.setter
    def partitions_from_engine(self, partitions_from_engine):
        """Sets the partitions_from_engine of this InlineResponse20023DataCache.


        :param partitions_from_engine: The partitions_from_engine of this InlineResponse20023DataCache.  # noqa: E501
        :type: int
        """

        self._partitions_from_engine = partitions_from_engine

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
        if issubclass(InlineResponse20023DataCache, dict):
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
        if not isinstance(other, InlineResponse20023DataCache):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20023DataCache):
            return True

        return self.to_dict() != other.to_dict()
