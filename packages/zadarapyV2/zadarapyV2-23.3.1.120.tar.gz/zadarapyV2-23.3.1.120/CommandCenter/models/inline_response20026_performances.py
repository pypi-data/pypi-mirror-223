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


class InlineResponse20026Performances(object):
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
        'iops': 'InlineResponse20026Iops',
        'iotime': 'InlineResponse20026Iotime',
        'bandwidth': 'InlineResponse20026Iotime',
        'queue_length': 'InlineResponse20026Iops',
        '_datetime': 'str',
        'label': 'str'
    }

    attribute_map = {
        'iops': 'iops',
        'iotime': 'iotime',
        'bandwidth': 'bandwidth',
        'queue_length': 'queue_length',
        '_datetime': 'datetime',
        'label': 'label'
    }

    def __init__(self, iops=None, iotime=None, bandwidth=None, queue_length=None, _datetime=None, label=None, _configuration=None):  # noqa: E501
        """InlineResponse20026Performances - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._iops = None
        self._iotime = None
        self._bandwidth = None
        self._queue_length = None
        self.__datetime = None
        self._label = None
        self.discriminator = None

        if iops is not None:
            self.iops = iops
        if iotime is not None:
            self.iotime = iotime
        if bandwidth is not None:
            self.bandwidth = bandwidth
        if queue_length is not None:
            self.queue_length = queue_length
        if _datetime is not None:
            self._datetime = _datetime
        if label is not None:
            self.label = label

    @property
    def iops(self):
        """Gets the iops of this InlineResponse20026Performances.  # noqa: E501


        :return: The iops of this InlineResponse20026Performances.  # noqa: E501
        :rtype: InlineResponse20026Iops
        """
        return self._iops

    @iops.setter
    def iops(self, iops):
        """Sets the iops of this InlineResponse20026Performances.


        :param iops: The iops of this InlineResponse20026Performances.  # noqa: E501
        :type: InlineResponse20026Iops
        """

        self._iops = iops

    @property
    def iotime(self):
        """Gets the iotime of this InlineResponse20026Performances.  # noqa: E501


        :return: The iotime of this InlineResponse20026Performances.  # noqa: E501
        :rtype: InlineResponse20026Iotime
        """
        return self._iotime

    @iotime.setter
    def iotime(self, iotime):
        """Sets the iotime of this InlineResponse20026Performances.


        :param iotime: The iotime of this InlineResponse20026Performances.  # noqa: E501
        :type: InlineResponse20026Iotime
        """

        self._iotime = iotime

    @property
    def bandwidth(self):
        """Gets the bandwidth of this InlineResponse20026Performances.  # noqa: E501


        :return: The bandwidth of this InlineResponse20026Performances.  # noqa: E501
        :rtype: InlineResponse20026Iotime
        """
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        """Sets the bandwidth of this InlineResponse20026Performances.


        :param bandwidth: The bandwidth of this InlineResponse20026Performances.  # noqa: E501
        :type: InlineResponse20026Iotime
        """

        self._bandwidth = bandwidth

    @property
    def queue_length(self):
        """Gets the queue_length of this InlineResponse20026Performances.  # noqa: E501


        :return: The queue_length of this InlineResponse20026Performances.  # noqa: E501
        :rtype: InlineResponse20026Iops
        """
        return self._queue_length

    @queue_length.setter
    def queue_length(self, queue_length):
        """Sets the queue_length of this InlineResponse20026Performances.


        :param queue_length: The queue_length of this InlineResponse20026Performances.  # noqa: E501
        :type: InlineResponse20026Iops
        """

        self._queue_length = queue_length

    @property
    def _datetime(self):
        """Gets the _datetime of this InlineResponse20026Performances.  # noqa: E501


        :return: The _datetime of this InlineResponse20026Performances.  # noqa: E501
        :rtype: str
        """
        return self.__datetime

    @_datetime.setter
    def _datetime(self, _datetime):
        """Sets the _datetime of this InlineResponse20026Performances.


        :param _datetime: The _datetime of this InlineResponse20026Performances.  # noqa: E501
        :type: str
        """

        self.__datetime = _datetime

    @property
    def label(self):
        """Gets the label of this InlineResponse20026Performances.  # noqa: E501


        :return: The label of this InlineResponse20026Performances.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this InlineResponse20026Performances.


        :param label: The label of this InlineResponse20026Performances.  # noqa: E501
        :type: str
        """

        self._label = label

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
        if issubclass(InlineResponse20026Performances, dict):
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
        if not isinstance(other, InlineResponse20026Performances):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20026Performances):
            return True

        return self.to_dict() != other.to_dict()
