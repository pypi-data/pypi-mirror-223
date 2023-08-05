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


class InlineResponse20023ResponseUsages(object):
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
        'zcache_data_dirty': 'float',
        'zcache_meta_dirty': 'float',
        'zcache_data_clean': 'float',
        'zcache_meta_clean': 'float',
        'zcache_data_cb_util': 'float',
        'zcache_meta_cb_util': 'float',
        'zcache_data_read_hit': 'float',
        'zcache_meta_read_hit': 'float',
        'zcache_data_write_hit': 'float',
        'zcache_meta_write_hit': 'float',
        'point': 'int'
    }

    attribute_map = {
        'zcache_data_dirty': 'zcache_data_dirty',
        'zcache_meta_dirty': 'zcache_meta_dirty',
        'zcache_data_clean': 'zcache_data_clean',
        'zcache_meta_clean': 'zcache_meta_clean',
        'zcache_data_cb_util': 'zcache_data_cb_util',
        'zcache_meta_cb_util': 'zcache_meta_cb_util',
        'zcache_data_read_hit': 'zcache_data_read_hit',
        'zcache_meta_read_hit': 'zcache_meta_read_hit',
        'zcache_data_write_hit': 'zcache_data_write_hit',
        'zcache_meta_write_hit': 'zcache_meta_write_hit',
        'point': 'point'
    }

    def __init__(self, zcache_data_dirty=None, zcache_meta_dirty=None, zcache_data_clean=None, zcache_meta_clean=None, zcache_data_cb_util=None, zcache_meta_cb_util=None, zcache_data_read_hit=None, zcache_meta_read_hit=None, zcache_data_write_hit=None, zcache_meta_write_hit=None, point=None, _configuration=None):  # noqa: E501
        """InlineResponse20023ResponseUsages - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._zcache_data_dirty = None
        self._zcache_meta_dirty = None
        self._zcache_data_clean = None
        self._zcache_meta_clean = None
        self._zcache_data_cb_util = None
        self._zcache_meta_cb_util = None
        self._zcache_data_read_hit = None
        self._zcache_meta_read_hit = None
        self._zcache_data_write_hit = None
        self._zcache_meta_write_hit = None
        self._point = None
        self.discriminator = None

        if zcache_data_dirty is not None:
            self.zcache_data_dirty = zcache_data_dirty
        if zcache_meta_dirty is not None:
            self.zcache_meta_dirty = zcache_meta_dirty
        if zcache_data_clean is not None:
            self.zcache_data_clean = zcache_data_clean
        if zcache_meta_clean is not None:
            self.zcache_meta_clean = zcache_meta_clean
        if zcache_data_cb_util is not None:
            self.zcache_data_cb_util = zcache_data_cb_util
        if zcache_meta_cb_util is not None:
            self.zcache_meta_cb_util = zcache_meta_cb_util
        if zcache_data_read_hit is not None:
            self.zcache_data_read_hit = zcache_data_read_hit
        if zcache_meta_read_hit is not None:
            self.zcache_meta_read_hit = zcache_meta_read_hit
        if zcache_data_write_hit is not None:
            self.zcache_data_write_hit = zcache_data_write_hit
        if zcache_meta_write_hit is not None:
            self.zcache_meta_write_hit = zcache_meta_write_hit
        if point is not None:
            self.point = point

    @property
    def zcache_data_dirty(self):
        """Gets the zcache_data_dirty of this InlineResponse20023ResponseUsages.  # noqa: E501


        :return: The zcache_data_dirty of this InlineResponse20023ResponseUsages.  # noqa: E501
        :rtype: float
        """
        return self._zcache_data_dirty

    @zcache_data_dirty.setter
    def zcache_data_dirty(self, zcache_data_dirty):
        """Sets the zcache_data_dirty of this InlineResponse20023ResponseUsages.


        :param zcache_data_dirty: The zcache_data_dirty of this InlineResponse20023ResponseUsages.  # noqa: E501
        :type: float
        """

        self._zcache_data_dirty = zcache_data_dirty

    @property
    def zcache_meta_dirty(self):
        """Gets the zcache_meta_dirty of this InlineResponse20023ResponseUsages.  # noqa: E501


        :return: The zcache_meta_dirty of this InlineResponse20023ResponseUsages.  # noqa: E501
        :rtype: float
        """
        return self._zcache_meta_dirty

    @zcache_meta_dirty.setter
    def zcache_meta_dirty(self, zcache_meta_dirty):
        """Sets the zcache_meta_dirty of this InlineResponse20023ResponseUsages.


        :param zcache_meta_dirty: The zcache_meta_dirty of this InlineResponse20023ResponseUsages.  # noqa: E501
        :type: float
        """

        self._zcache_meta_dirty = zcache_meta_dirty

    @property
    def zcache_data_clean(self):
        """Gets the zcache_data_clean of this InlineResponse20023ResponseUsages.  # noqa: E501


        :return: The zcache_data_clean of this InlineResponse20023ResponseUsages.  # noqa: E501
        :rtype: float
        """
        return self._zcache_data_clean

    @zcache_data_clean.setter
    def zcache_data_clean(self, zcache_data_clean):
        """Sets the zcache_data_clean of this InlineResponse20023ResponseUsages.


        :param zcache_data_clean: The zcache_data_clean of this InlineResponse20023ResponseUsages.  # noqa: E501
        :type: float
        """

        self._zcache_data_clean = zcache_data_clean

    @property
    def zcache_meta_clean(self):
        """Gets the zcache_meta_clean of this InlineResponse20023ResponseUsages.  # noqa: E501


        :return: The zcache_meta_clean of this InlineResponse20023ResponseUsages.  # noqa: E501
        :rtype: float
        """
        return self._zcache_meta_clean

    @zcache_meta_clean.setter
    def zcache_meta_clean(self, zcache_meta_clean):
        """Sets the zcache_meta_clean of this InlineResponse20023ResponseUsages.


        :param zcache_meta_clean: The zcache_meta_clean of this InlineResponse20023ResponseUsages.  # noqa: E501
        :type: float
        """

        self._zcache_meta_clean = zcache_meta_clean

    @property
    def zcache_data_cb_util(self):
        """Gets the zcache_data_cb_util of this InlineResponse20023ResponseUsages.  # noqa: E501


        :return: The zcache_data_cb_util of this InlineResponse20023ResponseUsages.  # noqa: E501
        :rtype: float
        """
        return self._zcache_data_cb_util

    @zcache_data_cb_util.setter
    def zcache_data_cb_util(self, zcache_data_cb_util):
        """Sets the zcache_data_cb_util of this InlineResponse20023ResponseUsages.


        :param zcache_data_cb_util: The zcache_data_cb_util of this InlineResponse20023ResponseUsages.  # noqa: E501
        :type: float
        """

        self._zcache_data_cb_util = zcache_data_cb_util

    @property
    def zcache_meta_cb_util(self):
        """Gets the zcache_meta_cb_util of this InlineResponse20023ResponseUsages.  # noqa: E501


        :return: The zcache_meta_cb_util of this InlineResponse20023ResponseUsages.  # noqa: E501
        :rtype: float
        """
        return self._zcache_meta_cb_util

    @zcache_meta_cb_util.setter
    def zcache_meta_cb_util(self, zcache_meta_cb_util):
        """Sets the zcache_meta_cb_util of this InlineResponse20023ResponseUsages.


        :param zcache_meta_cb_util: The zcache_meta_cb_util of this InlineResponse20023ResponseUsages.  # noqa: E501
        :type: float
        """

        self._zcache_meta_cb_util = zcache_meta_cb_util

    @property
    def zcache_data_read_hit(self):
        """Gets the zcache_data_read_hit of this InlineResponse20023ResponseUsages.  # noqa: E501


        :return: The zcache_data_read_hit of this InlineResponse20023ResponseUsages.  # noqa: E501
        :rtype: float
        """
        return self._zcache_data_read_hit

    @zcache_data_read_hit.setter
    def zcache_data_read_hit(self, zcache_data_read_hit):
        """Sets the zcache_data_read_hit of this InlineResponse20023ResponseUsages.


        :param zcache_data_read_hit: The zcache_data_read_hit of this InlineResponse20023ResponseUsages.  # noqa: E501
        :type: float
        """

        self._zcache_data_read_hit = zcache_data_read_hit

    @property
    def zcache_meta_read_hit(self):
        """Gets the zcache_meta_read_hit of this InlineResponse20023ResponseUsages.  # noqa: E501


        :return: The zcache_meta_read_hit of this InlineResponse20023ResponseUsages.  # noqa: E501
        :rtype: float
        """
        return self._zcache_meta_read_hit

    @zcache_meta_read_hit.setter
    def zcache_meta_read_hit(self, zcache_meta_read_hit):
        """Sets the zcache_meta_read_hit of this InlineResponse20023ResponseUsages.


        :param zcache_meta_read_hit: The zcache_meta_read_hit of this InlineResponse20023ResponseUsages.  # noqa: E501
        :type: float
        """

        self._zcache_meta_read_hit = zcache_meta_read_hit

    @property
    def zcache_data_write_hit(self):
        """Gets the zcache_data_write_hit of this InlineResponse20023ResponseUsages.  # noqa: E501


        :return: The zcache_data_write_hit of this InlineResponse20023ResponseUsages.  # noqa: E501
        :rtype: float
        """
        return self._zcache_data_write_hit

    @zcache_data_write_hit.setter
    def zcache_data_write_hit(self, zcache_data_write_hit):
        """Sets the zcache_data_write_hit of this InlineResponse20023ResponseUsages.


        :param zcache_data_write_hit: The zcache_data_write_hit of this InlineResponse20023ResponseUsages.  # noqa: E501
        :type: float
        """

        self._zcache_data_write_hit = zcache_data_write_hit

    @property
    def zcache_meta_write_hit(self):
        """Gets the zcache_meta_write_hit of this InlineResponse20023ResponseUsages.  # noqa: E501


        :return: The zcache_meta_write_hit of this InlineResponse20023ResponseUsages.  # noqa: E501
        :rtype: float
        """
        return self._zcache_meta_write_hit

    @zcache_meta_write_hit.setter
    def zcache_meta_write_hit(self, zcache_meta_write_hit):
        """Sets the zcache_meta_write_hit of this InlineResponse20023ResponseUsages.


        :param zcache_meta_write_hit: The zcache_meta_write_hit of this InlineResponse20023ResponseUsages.  # noqa: E501
        :type: float
        """

        self._zcache_meta_write_hit = zcache_meta_write_hit

    @property
    def point(self):
        """Gets the point of this InlineResponse20023ResponseUsages.  # noqa: E501


        :return: The point of this InlineResponse20023ResponseUsages.  # noqa: E501
        :rtype: int
        """
        return self._point

    @point.setter
    def point(self, point):
        """Sets the point of this InlineResponse20023ResponseUsages.


        :param point: The point of this InlineResponse20023ResponseUsages.  # noqa: E501
        :type: int
        """

        self._point = point

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
        if issubclass(InlineResponse20023ResponseUsages, dict):
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
        if not isinstance(other, InlineResponse20023ResponseUsages):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20023ResponseUsages):
            return True

        return self.to_dict() != other.to_dict()
