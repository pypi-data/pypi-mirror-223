# coding: utf-8

"""
    Zadara Provisioning Portal API

     # Overview  This document outlines the methods available for creation and high-level administration of Zadara Storage VPSAs via a Zadara Storage Provisioning Portal. This API supports form-encoded requests, and can return either JSON or XML responses.  ## Endpoint  The base URL for the requests is the Provisioning Portal URL you created your VPSA through - for example: https://manage.zadarastorage.com/, and all APIs will be prefixed with /api as noted in the documentation below.  ## Authentication  To use this API, an authentication token is required. The API for retrieving this token can be found below in the Authentication section. You may pass this token in requests either via the the X-Token header or via basic authentication (base64 encoded) in Authorization header.  ## Questions  If you have any questions or need support involving the REST API, please contact for assistance.   # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from ProvisioningPortal.api_client import ApiClient


class BillingApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_billing_items(self, start_datetime, end_datetime, **kwargs):  # noqa: E501
        """get_billing_items  # noqa: E501

        Download Billing Reports. The returned file is in zip format containing csv files.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_billing_items(start_datetime, end_datetime, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str start_datetime: Report start datetime in format yyyy-MM-DD HH:MM (required)
        :param str end_datetime: Report end datetime in format yyyy-MM-DD HH:MM (required)
        :param str user_id: Filter reports of a specific user
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_billing_items_with_http_info(start_datetime, end_datetime, **kwargs)  # noqa: E501
        else:
            (data) = self.get_billing_items_with_http_info(start_datetime, end_datetime, **kwargs)  # noqa: E501
            return data

    def get_billing_items_with_http_info(self, start_datetime, end_datetime, **kwargs):  # noqa: E501
        """get_billing_items  # noqa: E501

        Download Billing Reports. The returned file is in zip format containing csv files.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_billing_items_with_http_info(start_datetime, end_datetime, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str start_datetime: Report start datetime in format yyyy-MM-DD HH:MM (required)
        :param str end_datetime: Report end datetime in format yyyy-MM-DD HH:MM (required)
        :param str user_id: Filter reports of a specific user
        :return: str
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['start_datetime', 'end_datetime', 'user_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_billing_items" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'start_datetime' is set
        if self.api_client.client_side_validation and ('start_datetime' not in params or
                                                       params['start_datetime'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `start_datetime` when calling `get_billing_items`")  # noqa: E501
        # verify the required parameter 'end_datetime' is set
        if self.api_client.client_side_validation and ('end_datetime' not in params or
                                                       params['end_datetime'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `end_datetime` when calling `get_billing_items`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'start_datetime' in params:
            query_params.append(('start_datetime', params['start_datetime']))  # noqa: E501
        if 'end_datetime' in params:
            query_params.append(('end_datetime', params['end_datetime']))  # noqa: E501
        if 'user_id' in params:
            query_params.append(('user_id', params['user_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/zip'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/billing_items.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='str',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
