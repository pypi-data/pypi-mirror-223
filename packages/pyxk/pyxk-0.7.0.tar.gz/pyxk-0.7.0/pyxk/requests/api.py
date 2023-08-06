from typing import List, Union, Optional

from pyxk.requests import Session
from pyxk.requests.sessions import (
    Url,
    Method,
    Params,
    Auth,
    Cert,
    Json,
    Hooks,
    Files,
    Headers,
    Cookies,
    Proxies,
    Data,
    Response
)


def request(
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
    user_agent: Optional[str] = None,
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
    :param user_agent: User Agent
    :return: requests.Response
    """
    with Session(user_agent=user_agent) as session:
        return session.request(
            method=method,
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
            method_write_list=method_write_list,
        )


def get(
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
    user_agent: Optional[str] = None,
) -> Response:
    """get

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
    :param user_agent: User Agent
    :return: requests.Response
    """
    with Session(user_agent=user_agent) as session:
        return session.request(
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
            method_write_list=method_write_list,
        )


def post(
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
    user_agent: Optional[str] = None,
) -> Response:
    """post

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
    :param user_agent: User Agent
    :return: requests.Response
    """
    with Session(user_agent=user_agent) as session:
        return session.request(
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
            method_write_list=method_write_list,
        )


def head(
    url: Url,
    *,
    params: Params = None,
    data: Data = None,
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
    user_agent: Optional[str] = None,
) -> Response:
    """head

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
    :param user_agent: User Agent
    :return: requests.Response
    """
    with Session(user_agent=user_agent) as session:
        return session.request(
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
            method_write_list=method_write_list,
        )


def delete(
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
    user_agent: Optional[str] = None,
) -> Response:
    """delete

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
    :param user_agent: User Agent
    :return: requests.Response
    """
    with Session(user_agent=user_agent) as session:
        return session.request(
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
            method_write_list=method_write_list,
        )


def put(
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
    user_agent: Optional[str] = None,
) -> Response:
    """put

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
    :param user_agent: User Agent
    :return: requests.Response
    """
    with Session(user_agent=user_agent) as session:
        return session.request(
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
            method_write_list=method_write_list,
        )


def patch(
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
    user_agent: Optional[str] = None,
) -> Response:
    """patch

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
    :param user_agent: User Agent
    :return: requests.Response
    """
    with Session(user_agent=user_agent) as session:
        return session.request(
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
            method_write_list=method_write_list,
        )


def options(
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
    user_agent: Optional[str] = None,
) -> Response:
    """options

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
    :param user_agent: User Agent
    :return: requests.Response
    """
    with Session(user_agent=user_agent) as session:
        return session.request(
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
            method_write_list=method_write_list,
        )


def downloader(
    url: Url,
    method: Method = 'GET',
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
    stream: Optional[bool] = True,
    verify: Optional[Union[bool, str]] = None,
    cert: Cert = None,
    json: Json = None,
    show_status: bool = True,
    max_retries: Optional[int] = 10,
    status_force_list: Optional[List[int]] = None,
    method_write_list: Optional[List[str]] = None,
    user_agent: Optional[str] = None,
    output: Optional[str] = None,
    threads: Optional[int] = None,
    restore: bool = False,
    transient: bool = False
) -> Response:
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
    :param user_agent: User Agent
    :param output: 文件输出路径
    :param threads: 下载线程数量
    :param restore: 文件续传
    :param transient: 转瞬即逝
    :return: requests.Response
    """
    with Session(user_agent=user_agent) as session:
        return session.downloader(
            method=method,
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
            method_write_list=method_write_list,
            output=output,
            threads=threads,
            restore=restore,
            transient=transient
        )
