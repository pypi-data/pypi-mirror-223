# coding: utf-8

"""
    Zadara VPSA Object Storage REST API

    # Overview  This document outlines the methods available for administrating your VPSA&#174; Object Storage. The API supports form-encoded, JSON, and XML requests, and can return either JSON or XML responses.  ## Usage  The majority of the APIs available require authentication which requires an API token to use. You can retrieve this token through the Users section of your VPSA, or through the API using the \"Return a user's access key\" API in the Users Section below.  ## Authentication Methods  The authentication token can be passed either through the access_key parameter inside of the body of the REST API request, or through the X-Access-Key header. Alternately, you can use the username and password parameters for authentication, but we do not recommend this method for anything other than possibly retrieving an API key.  By default , all operations are allowed only to VPSA Object Storage admin. Some actions are allowed by an account admin and they will be marked on the action's header  ## Timeouts  By default, all operations that don't complete within five seconds will return a message informing you that the action may take some time to complete. When using the API, this can cause some actions, such as adding drives to storage policy, to be undesirably asynchronous. You can specify your own timeout with the timeout parameter, in seconds, and a timeout value of -1 specifies an infinite timeout.  ## Metering API  Metering information can be retrieved using the VPSA Object Storage API for the following components:  - Accounts - Users - Drives - Virtual Controllers - Load Balancer Groups - Storage Policies  Metering information returned by the API is subject to the following constraints:  - 10 seconds interval - 1 hour range - 1 minute interval - 1 day range - 1 hour interval - 30 days range  Values outside the accepted range will be returned as 0.  ## Questions  If you have any questions or need support involving the REST API, please contact for assistance.   # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from Zios.api_client import ApiClient


class DrivesApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_all_drives(self, **kwargs):  # noqa: E501
        """get_all_drives  # noqa: E501

        Returns a list of all drives.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_drives(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int start: The item number to start from. 0 starts from the beginning.
        :param int limit: The total number of records to return.
        :return: InlineResponse20029
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_drives_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_all_drives_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_all_drives_with_http_info(self, **kwargs):  # noqa: E501
        """get_all_drives  # noqa: E501

        Returns a list of all drives.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_drives_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int start: The item number to start from. 0 starts from the beginning.
        :param int limit: The total number of records to return.
        :return: InlineResponse20029
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['start', 'limit']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_drives" % key
                )
            params[key] = val
        del params['kwargs']

        if self.api_client.client_side_validation and ('start' in params and params['start'] < 0):  # noqa: E501
            raise ValueError("Invalid value for parameter `start` when calling `get_all_drives`, must be a value greater than or equal to `0`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'start' in params:
            query_params.append(('start', params['start']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/zios/drives.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20029',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_vpsaos_drive(self, name, **kwargs):  # noqa: E501
        """get_vpsaos_drive  # noqa: E501

        Returns one drive.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_vpsaos_drive(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: VPSA Object Storage drive name. (required)
        :return: InlineResponse20030
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_vpsaos_drive_with_http_info(name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_vpsaos_drive_with_http_info(name, **kwargs)  # noqa: E501
            return data

    def get_vpsaos_drive_with_http_info(self, name, **kwargs):  # noqa: E501
        """get_vpsaos_drive  # noqa: E501

        Returns one drive.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_vpsaos_drive_with_http_info(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: VPSA Object Storage drive name. (required)
        :return: InlineResponse20030
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_vpsaos_drive" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and ('name' not in params or
                                                       params['name'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `name` when calling `get_vpsaos_drive`")  # noqa: E501

        if self.api_client.client_side_validation and ('name' in params and not re.search(r'^volume-[0-9a-f]{8}$', params['name'])):  # noqa: E501
            raise ValueError("Invalid value for parameter `name` when calling `get_vpsaos_drive`, must conform to the pattern `/^volume-[0-9a-f]{8}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/zios/drives/{name}.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20030',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def show_bandwidth_throughput_metering_of_drive(self, name, vc, **kwargs):  # noqa: E501
        """show_bandwidth_throughput_metering_of_drive  # noqa: E501

        Shows bandwidth throughput metering (B/s) of a drive.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.show_bandwidth_throughput_metering_of_drive(name, vc, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: VPSA Object Storage drive name. (required)
        :param str vc: (required)
        :param int interval:
        :param int count:
        :return: InlineResponse20014
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.show_bandwidth_throughput_metering_of_drive_with_http_info(name, vc, **kwargs)  # noqa: E501
        else:
            (data) = self.show_bandwidth_throughput_metering_of_drive_with_http_info(name, vc, **kwargs)  # noqa: E501
            return data

    def show_bandwidth_throughput_metering_of_drive_with_http_info(self, name, vc, **kwargs):  # noqa: E501
        """show_bandwidth_throughput_metering_of_drive  # noqa: E501

        Shows bandwidth throughput metering (B/s) of a drive.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.show_bandwidth_throughput_metering_of_drive_with_http_info(name, vc, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: VPSA Object Storage drive name. (required)
        :param str vc: (required)
        :param int interval:
        :param int count:
        :return: InlineResponse20014
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name', 'vc', 'interval', 'count']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method show_bandwidth_throughput_metering_of_drive" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and ('name' not in params or
                                                       params['name'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `name` when calling `show_bandwidth_throughput_metering_of_drive`")  # noqa: E501
        # verify the required parameter 'vc' is set
        if self.api_client.client_side_validation and ('vc' not in params or
                                                       params['vc'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `vc` when calling `show_bandwidth_throughput_metering_of_drive`")  # noqa: E501

        if self.api_client.client_side_validation and ('name' in params and not re.search(r'^volume-[0-9a-f]{8}$', params['name'])):  # noqa: E501
            raise ValueError("Invalid value for parameter `name` when calling `show_bandwidth_throughput_metering_of_drive`, must conform to the pattern `/^volume-[0-9a-f]{8}$/`")  # noqa: E501
        if self.api_client.client_side_validation and ('vc' in params and not re.search(r'^vc-[0-9]*$', params['vc'])):  # noqa: E501
            raise ValueError("Invalid value for parameter `vc` when calling `show_bandwidth_throughput_metering_of_drive`, must conform to the pattern `/^vc-[0-9]*$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501

        query_params = []
        if 'vc' in params:
            query_params.append(('vc', params['vc']))  # noqa: E501
        if 'interval' in params:
            query_params.append(('interval', params['interval']))  # noqa: E501
        if 'count' in params:
            query_params.append(('count', params['count']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/zios/drives/{name}/throughput.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20014',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def show_iops_metering_of_drive(self, name, vc, **kwargs):  # noqa: E501
        """show_iops_metering_of_drive  # noqa: E501

        Shows IOPs metering of a drive.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.show_iops_metering_of_drive(name, vc, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: VPSA Object Storage drive name. (required)
        :param str vc: (required)
        :param int interval:
        :param int count:
        :return: InlineResponse20012
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.show_iops_metering_of_drive_with_http_info(name, vc, **kwargs)  # noqa: E501
        else:
            (data) = self.show_iops_metering_of_drive_with_http_info(name, vc, **kwargs)  # noqa: E501
            return data

    def show_iops_metering_of_drive_with_http_info(self, name, vc, **kwargs):  # noqa: E501
        """show_iops_metering_of_drive  # noqa: E501

        Shows IOPs metering of a drive.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.show_iops_metering_of_drive_with_http_info(name, vc, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: VPSA Object Storage drive name. (required)
        :param str vc: (required)
        :param int interval:
        :param int count:
        :return: InlineResponse20012
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name', 'vc', 'interval', 'count']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method show_iops_metering_of_drive" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and ('name' not in params or
                                                       params['name'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `name` when calling `show_iops_metering_of_drive`")  # noqa: E501
        # verify the required parameter 'vc' is set
        if self.api_client.client_side_validation and ('vc' not in params or
                                                       params['vc'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `vc` when calling `show_iops_metering_of_drive`")  # noqa: E501

        if self.api_client.client_side_validation and ('name' in params and not re.search(r'^volume-[0-9a-f]{8}$', params['name'])):  # noqa: E501
            raise ValueError("Invalid value for parameter `name` when calling `show_iops_metering_of_drive`, must conform to the pattern `/^volume-[0-9a-f]{8}$/`")  # noqa: E501
        if self.api_client.client_side_validation and ('vc' in params and not re.search(r'^vc-[0-9]*$', params['vc'])):  # noqa: E501
            raise ValueError("Invalid value for parameter `vc` when calling `show_iops_metering_of_drive`, must conform to the pattern `/^vc-[0-9]*$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501

        query_params = []
        if 'vc' in params:
            query_params.append(('vc', params['vc']))  # noqa: E501
        if 'interval' in params:
            query_params.append(('interval', params['interval']))  # noqa: E501
        if 'count' in params:
            query_params.append(('count', params['count']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/zios/drives/{name}/iops.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20012',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def show_latency_metering_of_drive(self, name, vc, **kwargs):  # noqa: E501
        """show_latency_metering_of_drive  # noqa: E501

        Shows latency metering (ms) of a drive.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.show_latency_metering_of_drive(name, vc, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: VPSA Object Storage drive name. (required)
        :param str vc: (required)
        :param int interval:
        :param int count:
        :return: InlineResponse20013
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.show_latency_metering_of_drive_with_http_info(name, vc, **kwargs)  # noqa: E501
        else:
            (data) = self.show_latency_metering_of_drive_with_http_info(name, vc, **kwargs)  # noqa: E501
            return data

    def show_latency_metering_of_drive_with_http_info(self, name, vc, **kwargs):  # noqa: E501
        """show_latency_metering_of_drive  # noqa: E501

        Shows latency metering (ms) of a drive.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.show_latency_metering_of_drive_with_http_info(name, vc, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str name: VPSA Object Storage drive name. (required)
        :param str vc: (required)
        :param int interval:
        :param int count:
        :return: InlineResponse20013
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['name', 'vc', 'interval', 'count']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method show_latency_metering_of_drive" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and ('name' not in params or
                                                       params['name'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `name` when calling `show_latency_metering_of_drive`")  # noqa: E501
        # verify the required parameter 'vc' is set
        if self.api_client.client_side_validation and ('vc' not in params or
                                                       params['vc'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `vc` when calling `show_latency_metering_of_drive`")  # noqa: E501

        if self.api_client.client_side_validation and ('name' in params and not re.search(r'^volume-[0-9a-f]{8}$', params['name'])):  # noqa: E501
            raise ValueError("Invalid value for parameter `name` when calling `show_latency_metering_of_drive`, must conform to the pattern `/^volume-[0-9a-f]{8}$/`")  # noqa: E501
        if self.api_client.client_side_validation and ('vc' in params and not re.search(r'^vc-[0-9]*$', params['vc'])):  # noqa: E501
            raise ValueError("Invalid value for parameter `vc` when calling `show_latency_metering_of_drive`, must conform to the pattern `/^vc-[0-9]*$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'name' in params:
            path_params['name'] = params['name']  # noqa: E501

        query_params = []
        if 'vc' in params:
            query_params.append(('vc', params['vc']))  # noqa: E501
        if 'interval' in params:
            query_params.append(('interval', params['interval']))  # noqa: E501
        if 'count' in params:
            query_params.append(('count', params['count']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/zios/drives/{name}/latency.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20013',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
