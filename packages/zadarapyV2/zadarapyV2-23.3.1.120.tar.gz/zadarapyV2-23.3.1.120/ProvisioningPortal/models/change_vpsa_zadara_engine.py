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


class ChangeVpsaZadaraEngine(object):
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
        'engine': 'str',
        'app_engine': 'str'
    }

    attribute_map = {
        'engine': 'engine',
        'app_engine': 'app_engine'
    }

    def __init__(self, engine=None, app_engine=None, _configuration=None):  # noqa: E501
        """ChangeVpsaZadaraEngine - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._engine = None
        self._app_engine = None
        self.discriminator = None

        self.engine = engine
        self.app_engine = app_engine

    @property
    def engine(self):
        """Gets the engine of this ChangeVpsaZadaraEngine.  # noqa: E501

        The Engine Type key for your desired Engine Type.  # noqa: E501

        :return: The engine of this ChangeVpsaZadaraEngine.  # noqa: E501
        :rtype: str
        """
        return self._engine

    @engine.setter
    def engine(self, engine):
        """Sets the engine of this ChangeVpsaZadaraEngine.

        The Engine Type key for your desired Engine Type.  # noqa: E501

        :param engine: The engine of this ChangeVpsaZadaraEngine.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and engine is None:
            raise ValueError("Invalid value for `engine`, must not be `None`")  # noqa: E501

        self._engine = engine

    @property
    def app_engine(self):
        """Gets the app_engine of this ChangeVpsaZadaraEngine.  # noqa: E501

        The APP Engine Type key for your desired APP Engine Type.  # noqa: E501

        :return: The app_engine of this ChangeVpsaZadaraEngine.  # noqa: E501
        :rtype: str
        """
        return self._app_engine

    @app_engine.setter
    def app_engine(self, app_engine):
        """Sets the app_engine of this ChangeVpsaZadaraEngine.

        The APP Engine Type key for your desired APP Engine Type.  # noqa: E501

        :param app_engine: The app_engine of this ChangeVpsaZadaraEngine.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and app_engine is None:
            raise ValueError("Invalid value for `app_engine`, must not be `None`")  # noqa: E501

        self._app_engine = app_engine

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
        if issubclass(ChangeVpsaZadaraEngine, dict):
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
        if not isinstance(other, ChangeVpsaZadaraEngine):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ChangeVpsaZadaraEngine):
            return True

        return self.to_dict() != other.to_dict()
