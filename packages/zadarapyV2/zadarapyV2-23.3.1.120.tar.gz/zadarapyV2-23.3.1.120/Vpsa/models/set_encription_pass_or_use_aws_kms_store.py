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


class SetEncriptionPassOrUseAwsKmsStore(object):
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
        'region': 'str',
        'kmskeyid': 'str',
        'access_id': 'str',
        'secret': 'str',
        'encryption_pwd': 'str',
        'old_encryption_pwd': 'str',
        'password': 'str'
    }

    attribute_map = {
        'region': 'region',
        'kmskeyid': 'kmskeyid',
        'access_id': 'access_id',
        'secret': 'secret',
        'encryption_pwd': 'encryption_pwd',
        'old_encryption_pwd': 'old_encryption_pwd',
        'password': 'password'
    }

    def __init__(self, region=None, kmskeyid=None, access_id=None, secret=None, encryption_pwd=None, old_encryption_pwd=None, password=None, _configuration=None):  # noqa: E501
        """SetEncriptionPassOrUseAwsKmsStore - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._region = None
        self._kmskeyid = None
        self._access_id = None
        self._secret = None
        self._encryption_pwd = None
        self._old_encryption_pwd = None
        self._password = None
        self.discriminator = None

        if region is not None:
            self.region = region
        if kmskeyid is not None:
            self.kmskeyid = kmskeyid
        if access_id is not None:
            self.access_id = access_id
        if secret is not None:
            self.secret = secret
        if encryption_pwd is not None:
            self.encryption_pwd = encryption_pwd
        if old_encryption_pwd is not None:
            self.old_encryption_pwd = old_encryption_pwd
        if password is not None:
            self.password = password

    @property
    def region(self):
        """Gets the region of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501


        :return: The region of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :rtype: str
        """
        return self._region

    @region.setter
    def region(self, region):
        """Sets the region of this SetEncriptionPassOrUseAwsKmsStore.


        :param region: The region of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :type: str
        """

        self._region = region

    @property
    def kmskeyid(self):
        """Gets the kmskeyid of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501


        :return: The kmskeyid of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :rtype: str
        """
        return self._kmskeyid

    @kmskeyid.setter
    def kmskeyid(self, kmskeyid):
        """Sets the kmskeyid of this SetEncriptionPassOrUseAwsKmsStore.


        :param kmskeyid: The kmskeyid of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :type: str
        """

        self._kmskeyid = kmskeyid

    @property
    def access_id(self):
        """Gets the access_id of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501


        :return: The access_id of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :rtype: str
        """
        return self._access_id

    @access_id.setter
    def access_id(self, access_id):
        """Sets the access_id of this SetEncriptionPassOrUseAwsKmsStore.


        :param access_id: The access_id of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :type: str
        """

        self._access_id = access_id

    @property
    def secret(self):
        """Gets the secret of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501


        :return: The secret of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :rtype: str
        """
        return self._secret

    @secret.setter
    def secret(self, secret):
        """Sets the secret of this SetEncriptionPassOrUseAwsKmsStore.


        :param secret: The secret of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :type: str
        """

        self._secret = secret

    @property
    def encryption_pwd(self):
        """Gets the encryption_pwd of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501


        :return: The encryption_pwd of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :rtype: str
        """
        return self._encryption_pwd

    @encryption_pwd.setter
    def encryption_pwd(self, encryption_pwd):
        """Sets the encryption_pwd of this SetEncriptionPassOrUseAwsKmsStore.


        :param encryption_pwd: The encryption_pwd of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :type: str
        """

        self._encryption_pwd = encryption_pwd

    @property
    def old_encryption_pwd(self):
        """Gets the old_encryption_pwd of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501


        :return: The old_encryption_pwd of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :rtype: str
        """
        return self._old_encryption_pwd

    @old_encryption_pwd.setter
    def old_encryption_pwd(self, old_encryption_pwd):
        """Sets the old_encryption_pwd of this SetEncriptionPassOrUseAwsKmsStore.


        :param old_encryption_pwd: The old_encryption_pwd of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :type: str
        """

        self._old_encryption_pwd = old_encryption_pwd

    @property
    def password(self):
        """Gets the password of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501


        :return: The password of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """Sets the password of this SetEncriptionPassOrUseAwsKmsStore.


        :param password: The password of this SetEncriptionPassOrUseAwsKmsStore.  # noqa: E501
        :type: str
        """

        self._password = password

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
        if issubclass(SetEncriptionPassOrUseAwsKmsStore, dict):
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
        if not isinstance(other, SetEncriptionPassOrUseAwsKmsStore):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SetEncriptionPassOrUseAwsKmsStore):
            return True

        return self.to_dict() != other.to_dict()
