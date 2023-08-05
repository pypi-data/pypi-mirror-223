# coding: utf-8

"""
    Command Center operations

    Command Center operations  # noqa: E501

    OpenAPI spec version: 23.03-sp1
    Contact: support@zadarastorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from CommandCenter.api_client import ApiClient


class ImagesApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_all_images(self, cloud_name, **kwargs):  # noqa: E501
        """get_all_images  # noqa: E501

        Returns a list of Cloud's registered images.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_images(cloud_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cloud_name: (required)
        :param int page: The page number to start from.
        :param int per_page: The total number of records to return.
        :return: InlineResponse20033
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_all_images_with_http_info(cloud_name, **kwargs)  # noqa: E501
        else:
            (data) = self.get_all_images_with_http_info(cloud_name, **kwargs)  # noqa: E501
            return data

    def get_all_images_with_http_info(self, cloud_name, **kwargs):  # noqa: E501
        """get_all_images  # noqa: E501

        Returns a list of Cloud's registered images.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_images_with_http_info(cloud_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cloud_name: (required)
        :param int page: The page number to start from.
        :param int per_page: The total number of records to return.
        :return: InlineResponse20033
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['cloud_name', 'page', 'per_page']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_all_images" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'cloud_name' is set
        if self.api_client.client_side_validation and ('cloud_name' not in params or
                                                       params['cloud_name'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `cloud_name` when calling `get_all_images`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'cloud_name' in params:
            path_params['cloud_name'] = params['cloud_name']  # noqa: E501

        query_params = []
        if 'page' in params:
            query_params.append(('page', params['page']))  # noqa: E501
        if 'per_page' in params:
            query_params.append(('per_page', params['per_page']))  # noqa: E501

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
            '/clouds/{cloud_name}/images.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20033',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_image(self, cloud_name, id, **kwargs):  # noqa: E501
        """get_image  # noqa: E501

        Returns a single image's details.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_image(cloud_name, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cloud_name: (required)
        :param str id: (required)
        :return: InlineResponse20034
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_image_with_http_info(cloud_name, id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_image_with_http_info(cloud_name, id, **kwargs)  # noqa: E501
            return data

    def get_image_with_http_info(self, cloud_name, id, **kwargs):  # noqa: E501
        """get_image  # noqa: E501

        Returns a single image's details.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_image_with_http_info(cloud_name, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cloud_name: (required)
        :param str id: (required)
        :return: InlineResponse20034
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['cloud_name', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_image" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'cloud_name' is set
        if self.api_client.client_side_validation and ('cloud_name' not in params or
                                                       params['cloud_name'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `cloud_name` when calling `get_image`")  # noqa: E501
        # verify the required parameter 'id' is set
        if self.api_client.client_side_validation and ('id' not in params or
                                                       params['id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `id` when calling `get_image`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'cloud_name' in params:
            path_params['cloud_name'] = params['cloud_name']  # noqa: E501
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

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
            '/clouds/{cloud_name}/images/{id}.json', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20034',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def set_default_image(self, cloud_name, id, **kwargs):  # noqa: E501
        """set_default_image  # noqa: E501

        Sets an image as the default for a Cloud.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.set_default_image(cloud_name, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cloud_name: (required)
        :param str id: (required)
        :return: InlineResponse20010
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.set_default_image_with_http_info(cloud_name, id, **kwargs)  # noqa: E501
        else:
            (data) = self.set_default_image_with_http_info(cloud_name, id, **kwargs)  # noqa: E501
            return data

    def set_default_image_with_http_info(self, cloud_name, id, **kwargs):  # noqa: E501
        """set_default_image  # noqa: E501

        Sets an image as the default for a Cloud.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.set_default_image_with_http_info(cloud_name, id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str cloud_name: (required)
        :param str id: (required)
        :return: InlineResponse20010
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['cloud_name', 'id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method set_default_image" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'cloud_name' is set
        if self.api_client.client_side_validation and ('cloud_name' not in params or
                                                       params['cloud_name'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `cloud_name` when calling `set_default_image`")  # noqa: E501
        # verify the required parameter 'id' is set
        if self.api_client.client_side_validation and ('id' not in params or
                                                       params['id'] is None):  # noqa: E501
            raise ValueError("Missing the required parameter `id` when calling `set_default_image`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'cloud_name' in params:
            path_params['cloud_name'] = params['cloud_name']  # noqa: E501
        if 'id' in params:
            path_params['id'] = params['id']  # noqa: E501

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
            '/clouds/{cloud_name}/images/{id}/set_default.json', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='InlineResponse20010',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
