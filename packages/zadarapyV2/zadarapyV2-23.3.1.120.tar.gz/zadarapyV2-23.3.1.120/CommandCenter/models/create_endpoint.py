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


class CreateEndpoint(object):
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
        'endpoint_name': 'str',
        'endpoint_method': 'str',
        'config': 'str'
    }

    attribute_map = {
        'endpoint_name': 'endpoint_name',
        'endpoint_method': 'endpoint_method',
        'config': 'config'
    }

    def __init__(self, endpoint_name=None, endpoint_method=None, config=None, _configuration=None):  # noqa: E501
        """CreateEndpoint - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._endpoint_name = None
        self._endpoint_method = None
        self._config = None
        self.discriminator = None

        self.endpoint_name = endpoint_name
        self.endpoint_method = endpoint_method
        self.config = config

    @property
    def endpoint_name(self):
        """Gets the endpoint_name of this CreateEndpoint.  # noqa: E501

        Endpoint name  # noqa: E501

        :return: The endpoint_name of this CreateEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._endpoint_name

    @endpoint_name.setter
    def endpoint_name(self, endpoint_name):
        """Sets the endpoint_name of this CreateEndpoint.

        Endpoint name  # noqa: E501

        :param endpoint_name: The endpoint_name of this CreateEndpoint.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and endpoint_name is None:
            raise ValueError("Invalid value for `endpoint_name`, must not be `None`")  # noqa: E501

        self._endpoint_name = endpoint_name

    @property
    def endpoint_method(self):
        """Gets the endpoint_method of this CreateEndpoint.  # noqa: E501

        Endpoint upload method  # noqa: E501

        :return: The endpoint_method of this CreateEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._endpoint_method

    @endpoint_method.setter
    def endpoint_method(self, endpoint_method):
        """Sets the endpoint_method of this CreateEndpoint.

        Endpoint upload method  # noqa: E501

        :param endpoint_method: The endpoint_method of this CreateEndpoint.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and endpoint_method is None:
            raise ValueError("Invalid value for `endpoint_method`, must not be `None`")  # noqa: E501
        allowed_values = ["s3_aws", "s3_zios", "ftp"]  # noqa: E501
        if (self._configuration.client_side_validation and
                endpoint_method not in allowed_values):
            raise ValueError(
                "Invalid value for `endpoint_method` ({0}), must be one of {1}"  # noqa: E501
                .format(endpoint_method, allowed_values)
            )

        self._endpoint_method = endpoint_method

    @property
    def config(self):
        """Gets the config of this CreateEndpoint.  # noqa: E501

        Endpoint configuration JSON, depending on the chosen upload method. For 's3_aws' and 's3_zios' methods, config should include 'access_key', 'secret_key' and 'region'. For 's3_zios' method, config should also include 'endpoint'. For 'ftp' method, config should include 'server', 'user', 'password', 'use_proxy' (boolean '0' or '1').  # noqa: E501

        :return: The config of this CreateEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this CreateEndpoint.

        Endpoint configuration JSON, depending on the chosen upload method. For 's3_aws' and 's3_zios' methods, config should include 'access_key', 'secret_key' and 'region'. For 's3_zios' method, config should also include 'endpoint'. For 'ftp' method, config should include 'server', 'user', 'password', 'use_proxy' (boolean '0' or '1').  # noqa: E501

        :param config: The config of this CreateEndpoint.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and config is None:
            raise ValueError("Invalid value for `config`, must not be `None`")  # noqa: E501

        self._config = config

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
        if issubclass(CreateEndpoint, dict):
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
        if not isinstance(other, CreateEndpoint):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateEndpoint):
            return True

        return self.to_dict() != other.to_dict()
