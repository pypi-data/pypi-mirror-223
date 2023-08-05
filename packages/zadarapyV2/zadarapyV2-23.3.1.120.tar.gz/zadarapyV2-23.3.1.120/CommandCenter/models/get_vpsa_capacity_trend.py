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


class GetVpsaCapacityTrend(object):
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
        'pool_id': 'str',
        'start_date': 'str',
        'end_date': 'str'
    }

    attribute_map = {
        'pool_id': 'pool_id',
        'start_date': 'start_date',
        'end_date': 'end_date'
    }

    def __init__(self, pool_id=None, start_date=None, end_date=None, _configuration=None):  # noqa: E501
        """GetVpsaCapacityTrend - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._pool_id = None
        self._start_date = None
        self._end_date = None
        self.discriminator = None

        self.pool_id = pool_id
        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date

    @property
    def pool_id(self):
        """Gets the pool_id of this GetVpsaCapacityTrend.  # noqa: E501


        :return: The pool_id of this GetVpsaCapacityTrend.  # noqa: E501
        :rtype: str
        """
        return self._pool_id

    @pool_id.setter
    def pool_id(self, pool_id):
        """Sets the pool_id of this GetVpsaCapacityTrend.


        :param pool_id: The pool_id of this GetVpsaCapacityTrend.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and pool_id is None:
            raise ValueError("Invalid value for `pool_id`, must not be `None`")  # noqa: E501
        if (self._configuration.client_side_validation and
                pool_id is not None and not re.search(r'^pool-[0-9a-f]{8}$', pool_id)):  # noqa: E501
            raise ValueError(r"Invalid value for `pool_id`, must be a follow pattern or equal to `/^pool-[0-9a-f]{8}$/`")  # noqa: E501

        self._pool_id = pool_id

    @property
    def start_date(self):
        """Gets the start_date of this GetVpsaCapacityTrend.  # noqa: E501


        :return: The start_date of this GetVpsaCapacityTrend.  # noqa: E501
        :rtype: str
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this GetVpsaCapacityTrend.


        :param start_date: The start_date of this GetVpsaCapacityTrend.  # noqa: E501
        :type: str
        """

        self._start_date = start_date

    @property
    def end_date(self):
        """Gets the end_date of this GetVpsaCapacityTrend.  # noqa: E501


        :return: The end_date of this GetVpsaCapacityTrend.  # noqa: E501
        :rtype: str
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Sets the end_date of this GetVpsaCapacityTrend.


        :param end_date: The end_date of this GetVpsaCapacityTrend.  # noqa: E501
        :type: str
        """

        self._end_date = end_date

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
        if issubclass(GetVpsaCapacityTrend, dict):
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
        if not isinstance(other, GetVpsaCapacityTrend):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GetVpsaCapacityTrend):
            return True

        return self.to_dict() != other.to_dict()
