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


class InlineResponse20039ResponseLcPolicies(object):
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
        'display_name': 'str',
        'enabled': 'str',
        'dry_run_mode': 'str',
        'use_recycle_bin': 'str',
        'file_selection_criteria': 'str',
        'whitelist_paths': 'str',
        'blacklist_paths': 'str',
        'action': 'str',
        'created_at': 'str',
        'modified_at': 'str'
    }

    attribute_map = {
        'name': 'name',
        'display_name': 'display_name',
        'enabled': 'enabled',
        'dry_run_mode': 'dry_run_mode',
        'use_recycle_bin': 'use_recycle_bin',
        'file_selection_criteria': 'file_selection_criteria',
        'whitelist_paths': 'whitelist_paths',
        'blacklist_paths': 'blacklist_paths',
        'action': 'action',
        'created_at': 'created_at',
        'modified_at': 'modified_at'
    }

    def __init__(self, name=None, display_name=None, enabled=None, dry_run_mode=None, use_recycle_bin=None, file_selection_criteria=None, whitelist_paths=None, blacklist_paths=None, action=None, created_at=None, modified_at=None, _configuration=None):  # noqa: E501
        """InlineResponse20039ResponseLcPolicies - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._display_name = None
        self._enabled = None
        self._dry_run_mode = None
        self._use_recycle_bin = None
        self._file_selection_criteria = None
        self._whitelist_paths = None
        self._blacklist_paths = None
        self._action = None
        self._created_at = None
        self._modified_at = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if display_name is not None:
            self.display_name = display_name
        if enabled is not None:
            self.enabled = enabled
        if dry_run_mode is not None:
            self.dry_run_mode = dry_run_mode
        if use_recycle_bin is not None:
            self.use_recycle_bin = use_recycle_bin
        if file_selection_criteria is not None:
            self.file_selection_criteria = file_selection_criteria
        if whitelist_paths is not None:
            self.whitelist_paths = whitelist_paths
        if blacklist_paths is not None:
            self.blacklist_paths = blacklist_paths
        if action is not None:
            self.action = action
        if created_at is not None:
            self.created_at = created_at
        if modified_at is not None:
            self.modified_at = modified_at

    @property
    def name(self):
        """Gets the name of this InlineResponse20039ResponseLcPolicies.  # noqa: E501


        :return: The name of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InlineResponse20039ResponseLcPolicies.


        :param name: The name of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def display_name(self):
        """Gets the display_name of this InlineResponse20039ResponseLcPolicies.  # noqa: E501


        :return: The display_name of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this InlineResponse20039ResponseLcPolicies.


        :param display_name: The display_name of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def enabled(self):
        """Gets the enabled of this InlineResponse20039ResponseLcPolicies.  # noqa: E501


        :return: The enabled of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :rtype: str
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this InlineResponse20039ResponseLcPolicies.


        :param enabled: The enabled of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :type: str
        """

        self._enabled = enabled

    @property
    def dry_run_mode(self):
        """Gets the dry_run_mode of this InlineResponse20039ResponseLcPolicies.  # noqa: E501


        :return: The dry_run_mode of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :rtype: str
        """
        return self._dry_run_mode

    @dry_run_mode.setter
    def dry_run_mode(self, dry_run_mode):
        """Sets the dry_run_mode of this InlineResponse20039ResponseLcPolicies.


        :param dry_run_mode: The dry_run_mode of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :type: str
        """

        self._dry_run_mode = dry_run_mode

    @property
    def use_recycle_bin(self):
        """Gets the use_recycle_bin of this InlineResponse20039ResponseLcPolicies.  # noqa: E501


        :return: The use_recycle_bin of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :rtype: str
        """
        return self._use_recycle_bin

    @use_recycle_bin.setter
    def use_recycle_bin(self, use_recycle_bin):
        """Sets the use_recycle_bin of this InlineResponse20039ResponseLcPolicies.


        :param use_recycle_bin: The use_recycle_bin of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :type: str
        """

        self._use_recycle_bin = use_recycle_bin

    @property
    def file_selection_criteria(self):
        """Gets the file_selection_criteria of this InlineResponse20039ResponseLcPolicies.  # noqa: E501


        :return: The file_selection_criteria of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :rtype: str
        """
        return self._file_selection_criteria

    @file_selection_criteria.setter
    def file_selection_criteria(self, file_selection_criteria):
        """Sets the file_selection_criteria of this InlineResponse20039ResponseLcPolicies.


        :param file_selection_criteria: The file_selection_criteria of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :type: str
        """

        self._file_selection_criteria = file_selection_criteria

    @property
    def whitelist_paths(self):
        """Gets the whitelist_paths of this InlineResponse20039ResponseLcPolicies.  # noqa: E501


        :return: The whitelist_paths of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :rtype: str
        """
        return self._whitelist_paths

    @whitelist_paths.setter
    def whitelist_paths(self, whitelist_paths):
        """Sets the whitelist_paths of this InlineResponse20039ResponseLcPolicies.


        :param whitelist_paths: The whitelist_paths of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :type: str
        """

        self._whitelist_paths = whitelist_paths

    @property
    def blacklist_paths(self):
        """Gets the blacklist_paths of this InlineResponse20039ResponseLcPolicies.  # noqa: E501


        :return: The blacklist_paths of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :rtype: str
        """
        return self._blacklist_paths

    @blacklist_paths.setter
    def blacklist_paths(self, blacklist_paths):
        """Sets the blacklist_paths of this InlineResponse20039ResponseLcPolicies.


        :param blacklist_paths: The blacklist_paths of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :type: str
        """

        self._blacklist_paths = blacklist_paths

    @property
    def action(self):
        """Gets the action of this InlineResponse20039ResponseLcPolicies.  # noqa: E501


        :return: The action of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this InlineResponse20039ResponseLcPolicies.


        :param action: The action of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :type: str
        """

        self._action = action

    @property
    def created_at(self):
        """Gets the created_at of this InlineResponse20039ResponseLcPolicies.  # noqa: E501


        :return: The created_at of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InlineResponse20039ResponseLcPolicies.


        :param created_at: The created_at of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def modified_at(self):
        """Gets the modified_at of this InlineResponse20039ResponseLcPolicies.  # noqa: E501


        :return: The modified_at of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :rtype: str
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this InlineResponse20039ResponseLcPolicies.


        :param modified_at: The modified_at of this InlineResponse20039ResponseLcPolicies.  # noqa: E501
        :type: str
        """

        self._modified_at = modified_at

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
        if issubclass(InlineResponse20039ResponseLcPolicies, dict):
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
        if not isinstance(other, InlineResponse20039ResponseLcPolicies):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InlineResponse20039ResponseLcPolicies):
            return True

        return self.to_dict() != other.to_dict()
