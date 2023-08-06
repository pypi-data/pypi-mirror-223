import os
from concurrent.futures import ThreadPoolExecutor
from typing import (
    Any, Dict, List, Tuple, Union, Optional, Callable, MutableMapping,
)
from urllib.parse import urlsplit, urljoin

from pyxk.utils import (
    chardet,
    make_open,
    LazyLoader,
    get_user_agent,
    download_progress,
    str_conversion_digit,
    read_file_by_generator,
    units_conversion_from_byte
)

from requests.auth import HTTPBasicAuth
from requests.cookies import RequestsCookieJar
from requests.models import Response
from requests.sessions import Session as _Session
from requests.structures import CaseInsensitiveDict
from requests.exceptions import Timeout, InvalidURL, RetryError, ConnectionError as _ConnectionError

_box = LazyLoader("_box", globals(), "rich.box")
_live = LazyLoader("_live", globals(), "rich.live")
_panel = LazyLoader("_panel", globals(), "rich.panel")
_table = LazyLoader("_table", globals(), "rich.table")
_console = LazyLoader("_console", globals(), "rich.console")

Url = Union[str, bytes]
Method = str
Params = Union[Dict[str, str], MutableMapping[str, str], None]
Auth = Union[HTTPBasicAuth, Tuple[Union[str, str]], None]
Cert = Optional[Tuple[Union[str, str]]]
Json = Union[Dict[str, Any], MutableMapping[str, Any], None]
Hooks = Optional[Dict[str, List[Callable]]]
Files = Union[Dict[str, Any], MutableMapping[str, Any], None]
Headers = Union[Dict[str, str], CaseInsensitiveDict, None]
Cookies = Union[dict, RequestsCookieJar, None]
Proxies = Optional[Dict[str, str]]
Data = Union[str, bytes, MutableMapping[str, Any], None]


class Session(_Session):
    """request.Session 重构"""

    def __init__(
        self,
        *,
        headers: Headers = None,
        base_url: Optional[Url] = None,
        user_agent: Optional[str] = None,
    ):
        """request.Session

        :param headers: Headers
        :param base_url: Base Url
        :param user_agent: User Agent
        """
        super().__init__()

        # headers
        headers = CaseInsensitiveDict(headers)
        if not headers.__contains__('User-Agent'):
            headers['User-Agent'] = get_user_agent()

        # user agent
        if user_agent and isinstance(user_agent, str):
            headers['User-Agent'] = user_agent

        # update headers
        self.headers.update(headers)

        # base url
        self._base_url = self._set_base_url(base_url)

        # console
        self._console = _console.Console()

    def request(
        self,
        method: Method,
        url: Url,
        *,
        params: Params = None,
        data: Data = None,
        headers: Headers = None,
        cookies: Cookies = None,
        files: Files = None,
        auth: Auth = None,
        timeout: Optional[Union[int, float]] = 5,
        allow_redirects: bool = True,
        proxies: Proxies = None,
        hooks: Hooks = None,
        stream: Optional[bool] = None,
        verify: Optional[Union[bool, str]] = None,
        cert: Cert = None,
        json: Json = None,
        show_status: bool = True,
        max_retries: Optional[int] = 10,
        status_force_list: Optional[List[int]] = None,
        method_write_list: Optional[List[str]] = None,
    ) -> Response:
        """request

        :param method: 请求方法 'GET', 'POST', 'HEAD', 'OPTIONS', 'DELETE', 'PUT', 'PATCH'
        :param url: url
        :param params: params
        :param data: data
        :param headers: 请求头
        :param cookies: cookies
        :param files: files
        :param auth: auth
        :param timeout: 超时时间
        :param allow_redirects: 请求重定向
        :param proxies: 请求代理
        :param hooks: hooks - {'response': [callable, ...]}
        :param stream: 流式相应 大文件请求
        :param verify: verify ssl
        :param cert: 请求证书
        :param json: json
        :param show_status: 请求显示 rich.status
        :param max_retries: 最大重试次数
        :param status_force_list: 状态码重试列表
        :param method_write_list: 请求方式白名单
        :return: requests.Response
        """
        # url 和 method
        url = self.build_url(url)
        if not isinstance(method, str):
            raise TypeError(f'method must be a str, got {type(method).__name__!r}')

        method = method.upper()

        # 最大重试次数 默认10
        max_retries = max_retries if isinstance(max_retries, int) and max_retries > 0 else 1

        # 状态码重试列表
        status_force_list = status_force_list if isinstance(status_force_list, (list, tuple)) else []

        # 指定需要重试的请求方法 默认为所有方法
        method_write_list = [item.upper() for item in method_write_list] \
            if isinstance(method_write_list, (list, tuple)) \
            else ['GET', 'POST', 'HEAD', 'OPTIONS', 'DELETE', 'PUT', 'PATCH']

        # request kwargs
        req_kwargs = dict(
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
        )

        # 开启request
        result = {'result': False, 'response': None, 'exc': None}

        for index in range(1, max_retries+1):
            result = self._send(
                method=method,
                url=url,
                retries=index,
                show_status=show_status,
                status_force_list=status_force_list,
                method_write_list=method_write_list,
                **req_kwargs
            )
            # 请求成功
            if result['result'] is True:
                break
        else:
            # 请求失败
            if result['result'] is False:
                if isinstance(result['exc'], Exception):
                    raise result['exc']
                else:
                    raise RetryError(
                        f'<Response[{result["response"].status_code}] {url}>, '
                        f'max_retries: {max_retries}'
                    )
        return result['response']

    def _send(
        self,
        method: Method,
        url: Url,
        retries: int,
        show_status: bool,
        status_force_list: List[int],
        method_write_list: List[str],
        **kwargs
    ):
        """send request

        :param method: 请求方法 'GET', 'POST', 'HEAD', 'OPTIONS', 'DELETE', 'PUT', 'PATCH'
        :param url: url
        :param retries: 当前请求重试次数
        :param show_status: 请求显示 rich.status
        :param status_force_list: 状态码重试列表
        :param method_write_list: 请求方式白名单
        :param kwargs: kwargs
        :return: dict
        """
        # rich.status
        rich_status = None
        if show_status:
            retries = f'[{retries}]' if retries > 1 else ''
            rich_status = self.console.status(
                f'{retries}Request <[magenta]{method}[/] [bright_blue u]{url}[/]>',
                spinner='arc'
            )
            rich_status.start()

        result = {'result': False, 'response': None, 'exc': None}

        try:
            # 忽略 requests verify=False 警告
            if not kwargs.get('verify'):
                import urllib3
                urllib3.disable_warnings()

            # request
            response = super().request(method=method, url=url, **kwargs)
            result['response'] = response

            # 请求状态码重试
            if (
                method in method_write_list
                and response.status_code in status_force_list
            ):
                return result
            result['result'] = True
            return result

        # exception
        except (Timeout, _ConnectionError) as exc:
            if method not in method_write_list:
                raise exc
            result['exc'] = exc
            return result

        # 关闭 rich.status
        finally:
            if rich_status:
                rich_status.stop()

    def get(
        self,
        url: Url,
        *,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Headers = None,
        cookies: Cookies = None,
        files: Files = None,
        auth: Auth = None,
        timeout: Optional[Union[int, float]] = 5,
        allow_redirects: bool = True,
        proxies: Proxies = None,
        hooks: Hooks = None,
        stream: Optional[bool] = None,
        verify: Optional[Union[bool, str]] = None,
        cert: Cert = None,
        json: Json = None,
        show_status: bool = True,
        max_retries: Optional[int] = 10,
        status_force_list: Optional[List[int]] = None,
        method_write_list: Optional[List[str]] = None,
    ) -> Response:
        """request - get

        :param url: url
        :param params: params
        :param data: data
        :param headers: 请求头
        :param cookies: cookies
        :param files: files
        :param auth: auth
        :param timeout: 超时时间
        :param allow_redirects: 请求重定向
        :param proxies: 请求代理
        :param hooks: hooks - {'response': [callable, ...]}
        :param stream: 流式相应 大文件请求
        :param verify: verify ssl
        :param cert: 请求证书
        :param json: json
        :param show_status: 请求显示 rich.status
        :param max_retries: 最大重试次数
        :param status_force_list: 状态码重试列表
        :param method_write_list: 请求方式白名单
        :return: requests.Response
        """
        return self.request(
            method='GET',
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            show_status=show_status,
            max_retries=max_retries,
            status_force_list=status_force_list,
            method_write_list=method_write_list
        )

    def post(
        self,
        url: Url,
        *,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Headers = None,
        cookies: Cookies = None,
        files: Files = None,
        auth: Auth = None,
        timeout: Optional[Union[int, float]] = 5,
        allow_redirects: bool = True,
        proxies: Proxies = None,
        hooks: Hooks = None,
        stream: Optional[bool] = None,
        verify: Optional[Union[bool, str]] = None,
        cert: Cert = None,
        json: Json = None,
        show_status: bool = True,
        max_retries: Optional[int] = 10,
        status_force_list: Optional[List[int]] = None,
        method_write_list: Optional[List[str]] = None,
    ) -> Response:
        """request - post

        :param url: url
        :param params: params
        :param data: data
        :param headers: 请求头
        :param cookies: cookies
        :param files: files
        :param auth: auth
        :param timeout: 超时时间
        :param allow_redirects: 请求重定向
        :param proxies: 请求代理
        :param hooks: hooks - {'response': [callable, ...]}
        :param stream: 流式相应 大文件请求
        :param verify: verify ssl
        :param cert: 请求证书
        :param json: json
        :param show_status: 请求显示 rich.status
        :param max_retries: 最大重试次数
        :param status_force_list: 状态码重试列表
        :param method_write_list: 请求方式白名单
        :return: requests.Response
        """
        return self.request(
            method='POST',
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            show_status=show_status,
            max_retries=max_retries,
            status_force_list=status_force_list,
            method_write_list=method_write_list
        )

    def head(
        self,
        url: Url,
        *,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Headers = None,
        cookies: Cookies = None,
        files: Files = None,
        auth: Auth = None,
        timeout: Optional[Union[int, float]] = 5,
        allow_redirects: bool = False,
        proxies: Proxies = None,
        hooks: Hooks = None,
        stream: Optional[bool] = None,
        verify: Optional[Union[bool, str]] = None,
        cert: Cert = None,
        json: Json = None,
        show_status: bool = True,
        max_retries: Optional[int] = 10,
        status_force_list: Optional[List[int]] = None,
        method_write_list: Optional[List[str]] = None,
    ) -> Response:
        """request - head

        :param url: url
        :param params: params
        :param data: data
        :param headers: 请求头
        :param cookies: cookies
        :param files: files
        :param auth: auth
        :param timeout: 超时时间
        :param allow_redirects: 请求重定向
        :param proxies: 请求代理
        :param hooks: hooks - {'response': [callable, ...]}
        :param stream: 流式相应 大文件请求
        :param verify: verify ssl
        :param cert: 请求证书
        :param json: json
        :param show_status: 请求显示 rich.status
        :param max_retries: 最大重试次数
        :param status_force_list: 状态码重试列表
        :param method_write_list: 请求方式白名单
        :return: requests.Response
        """
        return self.request(
            method='HEAD',
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            show_status=show_status,
            max_retries=max_retries,
            status_force_list=status_force_list,
            method_write_list=method_write_list
        )

    def put(
        self,
        url: Url,
        *,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Headers = None,
        cookies: Cookies = None,
        files: Files = None,
        auth: Auth = None,
        timeout: Optional[Union[int, float]] = 5,
        allow_redirects: bool = True,
        proxies: Proxies = None,
        hooks: Hooks = None,
        stream: Optional[bool] = None,
        verify: Optional[Union[bool, str]] = None,
        cert: Cert = None,
        json: Json = None,
        show_status: bool = True,
        max_retries: Optional[int] = 10,
        status_force_list: Optional[List[int]] = None,
        method_write_list: Optional[List[str]] = None,
    ) -> Response:
        """request - put

        :param url: url
        :param params: params
        :param data: data
        :param headers: 请求头
        :param cookies: cookies
        :param files: files
        :param auth: auth
        :param timeout: 超时时间
        :param allow_redirects: 请求重定向
        :param proxies: 请求代理
        :param hooks: hooks - {'response': [callable, ...]}
        :param stream: 流式相应 大文件请求
        :param verify: verify ssl
        :param cert: 请求证书
        :param json: json
        :param show_status: 请求显示 rich.status
        :param max_retries: 最大重试次数
        :param status_force_list: 状态码重试列表
        :param method_write_list: 请求方式白名单
        :return: requests.Response
        """
        return self.request(
            method='PUT',
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            show_status=show_status,
            max_retries=max_retries,
            status_force_list=status_force_list,
            method_write_list=method_write_list
        )

    def patch(
        self,
        url: Url,
        *,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Headers = None,
        cookies: Cookies = None,
        files: Files = None,
        auth: Auth = None,
        timeout: Optional[Union[int, float]] = 5,
        allow_redirects: bool = True,
        proxies: Proxies = None,
        hooks: Hooks = None,
        stream: Optional[bool] = None,
        verify: Optional[Union[bool, str]] = None,
        cert: Cert = None,
        json: Json = None,
        show_status: bool = True,
        max_retries: Optional[int] = 10,
        status_force_list: Optional[List[int]] = None,
        method_write_list: Optional[List[str]] = None,
    ) -> Response:
        """request - patch

        :param url: url
        :param params: params
        :param data: data
        :param headers: 请求头
        :param cookies: cookies
        :param files: files
        :param auth: auth
        :param timeout: 超时时间
        :param allow_redirects: 请求重定向
        :param proxies: 请求代理
        :param hooks: hooks - {'response': [callable, ...]}
        :param stream: 流式相应 大文件请求
        :param verify: verify ssl
        :param cert: 请求证书
        :param json: json
        :param show_status: 请求显示 rich.status
        :param max_retries: 最大重试次数
        :param status_force_list: 状态码重试列表
        :param method_write_list: 请求方式白名单
        :return: requests.Response
        """
        return self.request(
            method='PATCH',
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            show_status=show_status,
            max_retries=max_retries,
            status_force_list=status_force_list,
            method_write_list=method_write_list
        )

    def delete(
        self,
        url: Url,
        *,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Headers = None,
        cookies: Cookies = None,
        files: Files = None,
        auth: Auth = None,
        timeout: Optional[Union[int, float]] = 5,
        allow_redirects: bool = True,
        proxies: Proxies = None,
        hooks: Hooks = None,
        stream: Optional[bool] = None,
        verify: Optional[Union[bool, str]] = None,
        cert: Cert = None,
        json: Json = None,
        show_status: bool = True,
        max_retries: Optional[int] = 10,
        status_force_list: Optional[List[int]] = None,
        method_write_list: Optional[List[str]] = None,
    ) -> Response:
        """request - delete

        :param url: url
        :param params: params
        :param data: data
        :param headers: 请求头
        :param cookies: cookies
        :param files: files
        :param auth: auth
        :param timeout: 超时时间
        :param allow_redirects: 请求重定向
        :param proxies: 请求代理
        :param hooks: hooks - {'response': [callable, ...]}
        :param stream: 流式相应 大文件请求
        :param verify: verify ssl
        :param cert: 请求证书
        :param json: json
        :param show_status: 请求显示 rich.status
        :param max_retries: 最大重试次数
        :param status_force_list: 状态码重试列表
        :param method_write_list: 请求方式白名单
        :return: requests.Response
        """
        return self.request(
            method='DELETE',
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            show_status=show_status,
            max_retries=max_retries,
            status_force_list=status_force_list,
            method_write_list=method_write_list
        )

    def options(
        self,
        url: Url,
        *,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Headers = None,
        cookies: Cookies = None,
        files: Files = None,
        auth: Auth = None,
        timeout: Optional[Union[int, float]] = 5,
        allow_redirects: bool = True,
        proxies: Proxies = None,
        hooks: Hooks = None,
        stream: Optional[bool] = None,
        verify: Optional[Union[bool, str]] = None,
        cert: Cert = None,
        json: Json = None,
        show_status: bool = True,
        max_retries: Optional[int] = 10,
        status_force_list: Optional[List[int]] = None,
        method_write_list: Optional[List[str]] = None,
    ) -> Response:
        """request - options

        :param url: url
        :param params: params
        :param data: data
        :param headers: 请求头
        :param cookies: cookies
        :param files: files
        :param auth: auth
        :param timeout: 超时时间
        :param allow_redirects: 请求重定向
        :param proxies: 请求代理
        :param hooks: hooks - {'response': [callable, ...]}
        :param stream: 流式相应 大文件请求
        :param verify: verify ssl
        :param cert: 请求证书
        :param json: json
        :param show_status: 请求显示 rich.status
        :param max_retries: 最大重试次数
        :param status_force_list: 状态码重试列表
        :param method_write_list: 请求方式白名单
        :return: requests.Response
        """
        return self.request(
            method='OPTIONS',
            url=url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            show_status=show_status,
            max_retries=max_retries,
            status_force_list=status_force_list,
            method_write_list=method_write_list
        )

    def downloader(
        self,
        url: Url,
        method: Method = 'GET',
        *,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Headers = None,
        cookies: Cookies = None,
        files: Files = None,
        auth: Auth = None,
        timeout: Optional[Union[int, float]] = 5,
        allow_redirects: bool = True,
        proxies: Proxies = None,
        hooks: Hooks = None,
        stream: Optional[bool] = True,
        verify: Optional[Union[bool, str]] = None,
        cert: Cert = None,
        json: Json = None,
        show_status: bool = True,
        max_retries: Optional[int] = 10,
        status_force_list: Optional[List[int]] = None,
        method_write_list: Optional[List[str]] = None,
        output: Optional[str] = None,
        threads: Optional[int] = None,
        restore: bool = False,
        transient: bool = False
    ):
        """request - 下载器

        :param url: url
        :param method: 请求方法 'GET', 'POST', 'HEAD', 'OPTIONS', 'DELETE', 'PUT', 'PATCH'
        :param params: params
        :param data: data
        :param headers: 请求头
        :param cookies: cookies
        :param files: files
        :param auth: auth
        :param timeout: 超时时间
        :param allow_redirects: 请求重定向
        :param proxies: 请求代理
        :param hooks: hooks - {'response': [callable, ...]}
        :param stream: 流式相应 大文件请求
        :param verify: verify ssl
        :param cert: 请求证书
        :param json: json
        :param show_status: 请求显示 rich.status
        :param max_retries: 最大重试次数
        :param status_force_list: 状态码重试列表
        :param method_write_list: 请求方式白名单
        :param output: 文件输出路径
        :param threads: 下载线程数量
        :param restore: 文件续传
        :param transient: 转瞬即逝
        :return: requests.Response
        """
        req_kwargs = dict(
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
            method_write_list=method_write_list,
            status_force_list=status_force_list,
            max_retries=max_retries,
        )

        # head
        head_response = self.head(url=url, show_status=show_status, **req_kwargs)

        req_kwargs['url'] = url
        req_kwargs['method'] = method
        req_kwargs['show_status'] = False

        # content length
        content_length = str_conversion_digit(head_response.headers.get('Content-Length')).result

        # invalid content length
        if not content_length:
            threads, content_length = 1, None

        # output
        output = os.path.normpath(os.path.abspath(output)).replace('\\', '/') \
            if output and isinstance(output, str) else None

        # threads
        threads = 1 \
            if not output or not isinstance(threads, int) or threads <= 0 \
            else threads

        # not output - exit
        if not output:
            panel = self._repr_downloader(
                url=url,
                output=output,
                length=content_length,
                threads=threads,
                file_type=head_response.headers.get('Content-Type'),
                response=head_response
            )

            self.console.print(panel['panel'])
            return head_response

        # 多线程下载
        panel = self._repr_downloader(
            url=url,
            output=output,
            length=content_length,
            threads=threads,
            file_type=head_response.headers.get('Content-Type'),
            response=head_response,
            add_progress=True
        )

        # output_list, threads_pool
        output_list, pool = [], ThreadPoolExecutor(max_workers=8)

        with _live.Live(panel['panel'], console=self.console, transient=transient):
            for index in range(threads):
                # start_byte, end_byte
                start_byte, end_byte = None, None

                if content_length:
                    start_byte = index * (content_length // threads)
                    end_byte = start_byte + content_length // threads - 1

                    if index == threads - 1:
                        end_byte = content_length - 1

                # threads output
                thread_output = f'{output}.{index + 1}_{threads}.tmp' if threads > 1 else output
                output_list.append(thread_output)

                # 开启线程下载
                pool.submit(
                    self._downloader_chunk,
                    output=thread_output,
                    progress=panel['progress'],
                    restore=restore,
                    start_byte=start_byte,
                    end_byte=end_byte,
                    **req_kwargs
                )
            pool.shutdown()
            # 合并文件
            self._file_merge(output, output_list)

        return head_response

    def _downloader_chunk(
        self,
        output: str,
        progress,
        restore: bool = False,
        start_byte: Optional[int] = None,
        end_byte: Optional[int] = None,
        **kwargs
    ):
        """下载器 - 下载块

        :param output: 文件下载路径
        :param progress: rich.progress.Progress
        :param restore: 文件续传
        :param start_byte: 文件下载开始部分
        :param end_byte: 文件下载结束部分
        :param kwargs: request params
        """
        # total
        total = end_byte - start_byte \
            if isinstance(start_byte, int) and isinstance(end_byte, int) \
            else None

        # restore
        restore = restore if isinstance(total, int) else False

        # 文件续传
        completed, chunk_size = 0, 1024

        if restore and os.path.isfile(output):
            completed = os.path.getsize(output)
            if completed > total + 1:
                restore, completed = False, 0
            else:
                start_byte += completed
        else:
            restore = False

        # rich.progress.Progress 创建 task
        task = progress.add_task(description='', total=total, completed=completed)

        # request headers
        if isinstance(start_byte, int) and isinstance(end_byte, int):
            headers = CaseInsensitiveDict(kwargs.pop('headers', {}))
            headers.update({'Range': f'bytes={start_byte}-{end_byte}'})
            kwargs['headers'] = headers

        # 开启流式下载
        response = self.request(**kwargs)
        # 状态码 416 请求超出 range范围
        if response.status_code == 416:
            return

        with make_open(output, "ab" if restore else "wb") as write_file_obj:
            for chunk in response.iter_content(chunk_size=chunk_size):
                write_file_obj.write(chunk)
                progress.update(task, advance=chunk_size)

    @staticmethod
    def _file_merge(output: str, merge_list: list):
        """多线程下载后文件合并

        :param output: 文件合并后的路径
        :param merge_list: 需要合并的文件列表
        """
        # 判断文件是否存在
        for file in merge_list:
            if not os.path.isfile(file):
                return
        os.rename(merge_list.pop(0), output)

        # 拼接文件
        if not merge_list:
            return

        with make_open(output, 'ab') as write_file_obj:
            for file in merge_list:
                for _chunk in read_file_by_generator(file, 'rb'):
                    write_file_obj.write(_chunk)

                # 合并完成 删除文件
                os.remove(file)

    @staticmethod
    def _repr_downloader(
        url: Url,
        output: Optional[str],
        length: Optional[int],
        threads: int,
        file_type: Optional[str],
        response: Response,
        add_progress: bool = False,
    ):
        """显示downloader结果 - rich.panel.Panel"""
        result = {'panel': None, 'progress': None}

        table = _table.Table(show_header=False, box=_box.SIMPLE_HEAD)
        table.add_column(justify='left', overflow='fold')
        table.add_row(f'<[cyan]Response[/] [{response.status_code}]> [blue u]{url}[/]')
        table.add_section()

        # invalid content length
        if not length:
            table.add_row('[red]content-length is not available![/]')
            table.add_section()

        table.add_row(f'[green]filetype[/]: [yellow]{file_type}[/]')
        table.add_row(f'[green]filesize[/]: [yellow]{units_conversion_from_byte(length).result}[/] ({length})')
        table.add_row(f'[green]filename[/]: [blue]{output}[/]')

        # 添加rich.progress.Progress
        if add_progress:
            table.add_section()
            progress = download_progress()
            table.add_row(progress)
            result['progress'] = progress

        panel = _panel.Panel(
            table,
            title='[red b]Downloader[/]',
            title_align='center',
            border_style='bright_blue',
            expand=False,
            subtitle=f'[dim i]thread: {threads}',
            subtitle_align='right'
        )

        result['panel'] = panel
        return result

    def build_url(self, url: Url) -> Url:
        """构造完整url"""
        # 无效 url
        if not url or not isinstance(url, (str, bytes)):
            raise InvalidURL(f'url must be a str or bytes, got {url!r}')

        url = self._get_string_url(url)

        # 拼接完整 url
        if self.base_url and not self.is_absolute_url(url):
            return urljoin(self.base_url, url)

        return url

    def is_absolute_url(self, url: Url) -> bool:
        """判断 url 是否为绝对路径

        :param url: url
        :return: bool
        """
        if not url or not isinstance(url, (str, bytes)):
            return False

        url = urlsplit(self._get_string_url(url))

        return bool(url.scheme and url.netloc)

    def _set_base_url(self, url: Url) -> Optional[str]:
        """设置 base url

        :param url: url
        :return: Optional[str]
        """
        url = self._get_string_url(url)
        if self.is_absolute_url(url):
            return url
        return None

    @staticmethod
    def _get_string_url(url: Url) -> str:
        """获取字符串url"""
        if not isinstance(url, bytes):
            return url
        return url.decode(chardet(url).encoding)

    @property
    def base_url(self):
        """Base Url"""
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = self._set_base_url(value)

    @property
    def console(self):
        """rich.console.Console"""
        return self._console

    @property
    def user_agent(self):
        """User-Agent"""
        return self.headers.get('User-Agent')

    @user_agent.setter
    def user_agent(self, value):
        self.headers.update({'User-Agent': value})
