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


class ContainerReplicationApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_container_replication_job(self, create_container_replication_job, **kwargs):  # noqa: E501
        """create_container_replication_job  # noqa: E501

        Create a Container Replication Job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_container_replication_job(create_container_replication_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateContainerReplicationJob create_container_replication_job: (required)
        :return: InlineResponse20021
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_container_replication_job_with_http_info(create_container_replication_job, **kwargs)  # noqa: E501
        else:
            (data) = self.create_container_replication_job_with_http_info(create_container_replication_job, **kwargs)  # noqa: E501
            return data

    def create_container_replication_job_with_http_info(self, create_container_replication_job, **kwargs):  # noqa: E501
        """create_container_replication_job  # noqa: E501

        Create a Container Replication Job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_container_replication_job_with_http_info(create_container_replication_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param CreateContainerReplicationJob create_container_replication_job: (required)
        :return: InlineResponse20021
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['create_container_replication_job']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_container_replication_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'create_container_replication_job' is set
        if self.api_client.client_side_validation and ('create_container_replication_job' not in params or
                                                       params['create_container_replication_job'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `create_container_replication_job` when calling `create_container_replication_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'create_container_replication_job' in params:
            body_params = params['create_container_replication_job']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/zios/containers_replications.json', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20021',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_container_replication_job(self, delete_container_replication_job, **kwargs):  # noqa: E501
        """delete_container_replication_job  # noqa: E501

        delete a Container Replication Job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_container_replication_job(delete_container_replication_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeleteContainerReplicationJob delete_container_replication_job: (required)
        :return: InlineResponse20024
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.delete_container_replication_job_with_http_info(delete_container_replication_job, **kwargs)  # noqa: E501
        else:
            (data) = self.delete_container_replication_job_with_http_info(delete_container_replication_job, **kwargs)  # noqa: E501
            return data

    def delete_container_replication_job_with_http_info(self, delete_container_replication_job, **kwargs):  # noqa: E501
        """delete_container_replication_job  # noqa: E501

        delete a Container Replication Job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_container_replication_job_with_http_info(delete_container_replication_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param DeleteContainerReplicationJob delete_container_replication_job: (required)
        :return: InlineResponse20024
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['delete_container_replication_job']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_container_replication_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'delete_container_replication_job' is set
        if self.api_client.client_side_validation and ('delete_container_replication_job' not in params or
                                                       params['delete_container_replication_job'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `delete_container_replication_job` when calling `delete_container_replication_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'delete_container_replication_job' in params:
            body_params = params['delete_container_replication_job']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/zios/containers_replications/delete.json', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20024',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_container_replication_job(self, **kwargs):  # noqa: E501
        """get_container_replication_job  # noqa: E501

        Get a list of Container Replication Jobs or one Container Replication Job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_container_replication_job(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str replication_id: Replication job id. For example: 1_src-cont.1.json
        :return: InlineResponse20020
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_container_replication_job_with_http_info(**kwargs)  # noqa: E501
        else:
            (data) = self.get_container_replication_job_with_http_info(**kwargs)  # noqa: E501
            return data

    def get_container_replication_job_with_http_info(self, **kwargs):  # noqa: E501
        """get_container_replication_job  # noqa: E501

        Get a list of Container Replication Jobs or one Container Replication Job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_container_replication_job_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str replication_id: Replication job id. For example: 1_src-cont.1.json
        :return: InlineResponse20020
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['replication_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_container_replication_job" % key
                )
            params[key] = val
        del params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'replication_id' in params:
            query_params.append(('replicationId', params['replication_id']))  # noqa: E501

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
            '/zios/containers_replications.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20020',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_stats_of_container_replication_job(self, get_stats_of_container_replication_job, **kwargs):  # noqa: E501
        """get_stats_of_container_replication_job  # noqa: E501

        Get statistics of Container Replication Jobs in an account.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_stats_of_container_replication_job(get_stats_of_container_replication_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GetStatsOfContainerReplicationJob get_stats_of_container_replication_job: (required)
        :return: InlineResponse20025
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_stats_of_container_replication_job_with_http_info(get_stats_of_container_replication_job, **kwargs)  # noqa: E501
        else:
            (data) = self.get_stats_of_container_replication_job_with_http_info(get_stats_of_container_replication_job, **kwargs)  # noqa: E501
            return data

    def get_stats_of_container_replication_job_with_http_info(self, get_stats_of_container_replication_job, **kwargs):  # noqa: E501
        """get_stats_of_container_replication_job  # noqa: E501

        Get statistics of Container Replication Jobs in an account.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_stats_of_container_replication_job_with_http_info(get_stats_of_container_replication_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GetStatsOfContainerReplicationJob get_stats_of_container_replication_job: (required)
        :return: InlineResponse20025
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['get_stats_of_container_replication_job']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_stats_of_container_replication_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'get_stats_of_container_replication_job' is set
        if self.api_client.client_side_validation and ('get_stats_of_container_replication_job' not in params or
                                                       params['get_stats_of_container_replication_job'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `get_stats_of_container_replication_job` when calling `get_stats_of_container_replication_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'get_stats_of_container_replication_job' in params:
            body_params = params['get_stats_of_container_replication_job']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/zios/containers_replications/stats_of_account.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20025',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_stats_of_replication_job(self, get_stats_of_replication_job, **kwargs):  # noqa: E501
        """get_stats_of_replication_job  # noqa: E501

        Get statistics of a replication job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_stats_of_replication_job(get_stats_of_replication_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GetStatsOfReplicationJob get_stats_of_replication_job: (required)
        :return: InlineResponse20026
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_stats_of_replication_job_with_http_info(get_stats_of_replication_job, **kwargs)  # noqa: E501
        else:
            (data) = self.get_stats_of_replication_job_with_http_info(get_stats_of_replication_job, **kwargs)  # noqa: E501
            return data

    def get_stats_of_replication_job_with_http_info(self, get_stats_of_replication_job, **kwargs):  # noqa: E501
        """get_stats_of_replication_job  # noqa: E501

        Get statistics of a replication job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_stats_of_replication_job_with_http_info(get_stats_of_replication_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param GetStatsOfReplicationJob get_stats_of_replication_job: (required)
        :return: InlineResponse20026
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['get_stats_of_replication_job']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_stats_of_replication_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'get_stats_of_replication_job' is set
        if self.api_client.client_side_validation and ('get_stats_of_replication_job' not in params or
                                                       params['get_stats_of_replication_job'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `get_stats_of_replication_job` when calling `get_stats_of_replication_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'get_stats_of_replication_job' in params:
            body_params = params['get_stats_of_replication_job']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/zios/containers_replications/replication_job_stats.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20026',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def pause_container_replication_job(self, pause_container_replication_job, **kwargs):  # noqa: E501
        """pause_container_replication_job  # noqa: E501

        Pause a Container Replication Job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.pause_container_replication_job(pause_container_replication_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param PauseContainerReplicationJob pause_container_replication_job: (required)
        :return: InlineResponse20023
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.pause_container_replication_job_with_http_info(pause_container_replication_job, **kwargs)  # noqa: E501
        else:
            (data) = self.pause_container_replication_job_with_http_info(pause_container_replication_job, **kwargs)  # noqa: E501
            return data

    def pause_container_replication_job_with_http_info(self, pause_container_replication_job, **kwargs):  # noqa: E501
        """pause_container_replication_job  # noqa: E501

        Pause a Container Replication Job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.pause_container_replication_job_with_http_info(pause_container_replication_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param PauseContainerReplicationJob pause_container_replication_job: (required)
        :return: InlineResponse20023
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['pause_container_replication_job']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method pause_container_replication_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'pause_container_replication_job' is set
        if self.api_client.client_side_validation and ('pause_container_replication_job' not in params or
                                                       params['pause_container_replication_job'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `pause_container_replication_job` when calling `pause_container_replication_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'pause_container_replication_job' in params:
            body_params = params['pause_container_replication_job']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/zios/containers_replications/pause.json', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20023',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def resume_container_replication_job(self, resume_container_replication_job, **kwargs):  # noqa: E501
        """resume_container_replication_job  # noqa: E501

        Resume a Container Replication Job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.resume_container_replication_job(resume_container_replication_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ResumeContainerReplicationJob resume_container_replication_job: (required)
        :return: InlineResponse20022
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.resume_container_replication_job_with_http_info(resume_container_replication_job, **kwargs)  # noqa: E501
        else:
            (data) = self.resume_container_replication_job_with_http_info(resume_container_replication_job, **kwargs)  # noqa: E501
            return data

    def resume_container_replication_job_with_http_info(self, resume_container_replication_job, **kwargs):  # noqa: E501
        """resume_container_replication_job  # noqa: E501

        Resume a Container Replication Job.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.resume_container_replication_job_with_http_info(resume_container_replication_job, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ResumeContainerReplicationJob resume_container_replication_job: (required)
        :return: InlineResponse20022
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['resume_container_replication_job']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method resume_container_replication_job" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'resume_container_replication_job' is set
        if self.api_client.client_side_validation and ('resume_container_replication_job' not in params or
                                                       params['resume_container_replication_job'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `resume_container_replication_job` when calling `resume_container_replication_job`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'resume_container_replication_job' in params:
            body_params = params['resume_container_replication_job']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'application/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/zios/containers_replications/resume.json', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20022',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
