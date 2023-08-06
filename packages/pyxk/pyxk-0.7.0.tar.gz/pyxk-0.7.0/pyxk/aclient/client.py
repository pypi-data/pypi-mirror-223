import asyncio
from types import MethodType
from typing import (
    Any, List, Tuple, Union, Optional, Mapping, Callable
)

from multidict import CIMultiDict
from pyxk.aclient.typedef import (
    URL, Session, Response, EventLoop, CIMDict, Timeout, URLS
)
from pyxk.utils import (
    LazyLoader, get_user_agent, default_headers, chardet
)

copy = LazyLoader('copy', globals(), 'copy')
yarl = LazyLoader('yarl', globals(), 'yarl')
urllib = LazyLoader('urllib', globals(), 'urllib.parse')
aiohttp = LazyLoader('aiohttp', globals(), 'aiohttp')
logging = LazyLoader('logging', globals(), 'logging')
selector = LazyLoader('selector', globals(), 'parsel.selector')
aiohttp_exceptions = LazyLoader('aiohttp_exceptions', globals(), 'aiohttp.client_exceptions')


__all__ = ['Client', 'Response']


class Client:
    """异步下载器

    explain:
    from pyxk import Client, Response

    class Download(Client):
        start_urls = ['http://www.baidu.com' for _ in range(10)]

        async def parse(self, response: Response, **kwargs):
            print(response.url)

    Download.run()
    """

    limit: int = 100
    timeout: Timeout = None
    verify: bool = True
    warning: bool = True
    headers: Union[dict, CIMDict] = CIMultiDict(default_headers())
    semaphore: Union[int, asyncio.Semaphore] = 32
    user_agent: Optional[str] = None
    req_kwargs: dict = {}
    start_urls: Union[List[str], List[Tuple[str, dict]]] = []
    async_sleep: Union[int, float] = 0
    max_retries: int = 15
    aiohttp_kwargs: dict = {}
    status_retry_list: List[int] = []
    status_error_list: List[int] = []
    until_request_succeed: Union[bool, List[int]] = False
    ATTRS = {
        'timeout': 10,
        'semaphore': 16,
        'user_agent': get_user_agent(),
    }

    def __init__(self, *, base_url: URL = None, **kwargs):
        """异步下载器

        :param limit: aiohttp 并发控制
        :param timeout: 请求超时时间
        :param verify: ssl验证
        :param warning: 警告信息
        :param headers: 请求头
        :param semaphore: asyncio并发控制
        :param user_agent: User-Agent
        :param req_kwargs: start_request请求参数
        :param start_urls: 请求入口urls
        :param async_sleep: 异步休眠时间
        :param max_retries: 异步请求最大重试次数
        :param aiohttp_kwargs: aiohttp.ClientSession 实例化参数
        :param status_retry_list: 请求状态码，包含在列表中的进行重新发送
        :param status_error_list: 请求状态码，包含在列表中直接抛出错误
        :param until_request_succeed: 请求状态码，直到请求响应成功(可自定义响应状态码)
        :param base_url: base_url 每个请求URL进行拼接
        """
        # 动态生成实例变量
        for key, val in kwargs.items():
            setattr(self, key, val)

        # event loop
        self._loop: EventLoop = None

        # aiohttp session
        self._session: Session = None

        # base_url
        self._base_url: URL = self.set_base_url(base_url)

    @classmethod
    def run(cls, **kwargs):
        """程序运行入口 - 应该调用该方法运行"""
        self = cls(**kwargs)

        # 创建新的 event loop
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # 运行
        self.loop.run_until_complete(self.async_start())

        # 关闭 EventLoop
        if self.loop:
            self.loop.close()
            asyncio.set_event_loop(None)

        return self

    async def async_start(self):
        """开启异步下载器"""
        await self.open()

        # 无效 event loop
        if not isinstance(self.loop, asyncio.AbstractEventLoop):
            raise TypeError(f'Event loop must be an instance of AbstractEventLoop, not {type(self.loop).__name__!r}')

        # event loop 已经关闭
        if self.loop.is_closed():
            raise ValueError('Event loop is not closed')

        # 配置 asyncio semaphore
        if isinstance(self.semaphore, int) and self.semaphore > 0:
            self.semaphore = asyncio.Semaphore(self.semaphore)
        elif not isinstance(self.semaphore, asyncio.Semaphore):
            self.semaphore = asyncio.Semaphore(self.__class__.ATTRS['semaphore'])

        # aiohttp.Session 实例化参数
        aiohttp_kwargs = copy.deepcopy(dict(self.aiohttp_kwargs))

        # 为 aiohttp.Session 设置超时时间
        if isinstance(self.timeout, int) and self.timeout >= 0:
            aiohttp_kwargs['timeout'] = aiohttp.ClientTimeout(total=self.timeout)
        elif not aiohttp_kwargs.__contains__('timeout'):
            aiohttp_kwargs['timeout'] = aiohttp.ClientTimeout(total=self.__class__.ATTRS['timeout'])
        self.timeout = aiohttp_kwargs['timeout'].total

        # 为 aiohttp.Session 设置连接器
        if not aiohttp_kwargs.__contains__('connector'):
            if not isinstance(self.limit, int) or self.limit <= 0:
                raise ValueError(f'Limit must be a positive integer(正整数), got {self.limit!r}')

            aiohttp_kwargs['connector'] = aiohttp.TCPConnector(
                limit=self.limit, ssl=bool(self.verify), loop=self.loop
            )

        # 为 aiohttp.Session 设置 headers(user_agent)
        self.headers = CIMultiDict(self.headers)
        # user_agent
        if self.user_agent and isinstance(self.user_agent, str):
            self.headers['User-Agent'] = self.user_agent
        elif not self.headers.__contains__('User-Agent'):
            self.headers['User-Agent'] = self.__class__.ATTRS['user_agent']
        self.user_agent = self.headers.get('User-Agent')
        aiohttp_kwargs['headers'] = self.headers

        # 创建 aiohttp.ClientSession
        self._session = aiohttp.ClientSession(loop=self.loop, **aiohttp_kwargs)

        # 初始化变量
        self._init_attrs()

        # 开启请求
        try:
            await self.start()
            ret = await self.start_request()
            await self.completed(ret)
        finally:
            await self.async_close()

    async def async_close(self):
        """关闭异步下载器"""
        await self.stop()
        # 关闭 aiohttp session
        if self.session:
            await self.session.close()
        # 关闭 aiohttp session 之后调用
        await self.close()

    async def start_request(
        self,
        callback: Optional[Callable] = None,
        set_base_url: bool = True,
        **kwargs
    ):
        """start_urls 默认运行方法

        :param callback: 回调函数
        :param set_base_url: 设置base url
        :param kwargs: 请求可选关键字参数
        """
        if not self.start_urls or not isinstance(self.start_urls, (list, tuple)):
            raise NotImplementedError(
                f'Invalid start_urls, got {self.start_urls!r}'
            )

        kw = copy.deepcopy(dict(self.req_kwargs))
        kw.update(kwargs)

        return await self.gather(
            self.start_urls,
            callback if callable(callback) else self.parse,
            set_base_url=set_base_url,
            **kw
        )

    async def request(
        self,
        url: URL,
        callback: Optional[Callable] = None,
        *,
        method: str = "GET",
        cb_kwargs: Optional[dict] = None,
        **kwargs
    ) -> Union[Response, Any]:
        """异步请求发送以及回调

        :return:
        :param url: URL
        :param callback: 响应response 回调函数(函数是异步的)
        :param method: 请求方法(default: GET)
        :param cb_kwargs: 传递给回调函数的关键字参数
        :param kwargs: 异步请求 request参数
            params, data, json, cookies, headers,
            skip_auto_headers, auth, allow_redirects,
            max_redirects, compress, chunked, expect100,
            raise_for_status, read_until_eof, proxy, proxy_auth,
            timeout, verify_ssl, fingerprint,
            ssl_context, ssl, proxy_headers,
            trace_request_ctx, read_bufsize
        :return: Response, Any
        """
        status_retry_list, status_error_list = self.status_retry_list.copy(), self.status_error_list.copy()
        url, response, result, exc_from_request = self.build_url(url), None, None, None
        warning = {
            'status_retry_list': True,
            'status_error_list': True,
            'until_request_succeed': True,
            'timeout': True,
            'client': True,
            'server_disconnected': True
        }

        async with self.semaphore:
            for _ in range(1, self.max_retries+1):
                try:
                    response = result = await self.session.request(method=method, url=url, **kwargs)

                    # 直到请求成功
                    if self.until_request_succeed:
                        if response.status in self.until_request_succeed:
                            status_retry_list, status_error_list = [], []
                        else:
                            # 状态码错误
                            if response.status in status_error_list:
                                raise aiohttp_exceptions.ClientError(f'<Response[{response.status}] {url}>')

                            # 提示信息
                            await self._warning('until_request_succeed', url, warning, response)
                            continue

                    # 状态码错误
                    if response.status in status_error_list:
                        raise aiohttp_exceptions.ClientError(f'<Response[{response.status}] {url}>')

                    # 状态码重试
                    if response.status in status_retry_list:
                        # 提示信息
                        await self._warning('status_retry_list', url, warning, response)
                        continue

                    # 添加 aiohttp.ClientResponse 实例方法
                    add_instance_method(response)

                    # 开启回调函数
                    if callable(callback):
                        cb_kwargs = dict(cb_kwargs or {})
                        result = await callback(response, **dict(cb_kwargs or {}))
                    break

                # 请求超时 重试
                except asyncio.exceptions.TimeoutError as exc:
                    # 提示信息
                    await self._warning('timeout', url, warning, response)
                    exc_from_request = exc

                # 连接错误 重试
                except (
                    aiohttp_exceptions.ClientOSError,
                    aiohttp_exceptions.ClientPayloadError,
                    aiohttp_exceptions.ClientConnectorError,
                ) as exc:
                    # 提示信息
                    await self._warning('client', url, warning, response)
                    exc_from_request = exc

                # 服务器拒绝连接
                except aiohttp_exceptions.ServerDisconnectedError as exc:
                    # 提示信息
                    await self._warning('server_disconnected', url, warning, response)
                    exc_from_request = exc

                finally:
                    # 关闭连接
                    if response and callable(callback):
                        response.close()

            else:
                # 抛出错误
                if exc_from_request:
                    raise exc_from_request
                # 达到最大请求次数
                raise RuntimeError(
                    f'<Response[{response.status if response else None}] '
                    f'{url}>, max_retries: {self.max_retries}'
                )

        return result

    def _init_attrs(self):
        # 最大重试次数
        if not isinstance(self.max_retries, int) or self.max_retries <= 0:
            raise ValueError(f'max_retries must be a positive integer(正整数), got {self.max_retries!r}')

        # 状态码重试列表
        if not isinstance(self.status_retry_list, (list, tuple)):
            raise ValueError(f'status_retry_list must be a list, got {self.status_retry_list!r}')

        # 状态码错误列表
        if not isinstance(self.status_error_list, (list, tuple)):
            raise ValueError(f'status_retry_list must be a list, got {self.status_error_list!r}')

        # 直到请求成功
        if not isinstance(self.until_request_succeed, (list, tuple)):
            self.until_request_succeed = [200] if self.until_request_succeed else []

    async def _warning(self, who: str, url: str, warning: dict, response: Response):
        """打印警告信息"""
        # 状态码
        status = response.status if response else None
        # 全部警告信息
        who_list = {
            'status_retry_list':
                f'<Response[{status}] {url}> be in '
                f'status_retry_list:{self.status_retry_list!r}',
            'until_request_succeed':
                f'<Response[{status}] {url}> be in '
                f'until_request_succeed:{self.until_request_succeed!r}',
            'timeout': f'{url}> Timeout',
            'client': f'{url}> client error',
            'server_disconnected': f'{url}> server disconnected'
        }

        # 确保 每个链接每个警告类型 只会打印一次
        if self.warning and warning[who]:
            logging.warning(who_list[who])
            warning[who] = False

        await self.sleep()

    async def gather(
        self,
        urls: URLS,
        callback: Optional[Callable] = None,
        *,
        method: str = "GET",
        cb_kwargs_list: Union[List[dict], dict] = None,
        return_exceptions: bool = False,
        set_base_url: Union[bool, str] = False,
        **req_kwargs
    ) -> list:
        """发送url列表，创建异步任务 并发发送

        :param urls: Url List
        :param callback: 响应response 回调函数(函数是异步的)
        :param method: 请求方法(default: GET)
        :param cb_kwargs_list: 回调函数关键字参数列表
        :param return_exceptions: 错误传递(default: False)
        :param req_kwargs: 异步请求 request参数
        :param set_base_url: 是否设置base_url
        :return: list
        """
        if not isinstance(urls, (list, tuple)):
            raise TypeError(f'urls must be a list, not {type(urls).__name__!r}')

        length = len(urls)
        cb_kwargs_list = self._parse_gather_cb(length, cb_kwargs_list)

        for index, item in enumerate(urls):
            url, cb_kwargs = item, {}
            # 解析 url 和 回调参数
            if isinstance(item, (list, tuple)):
                if len(item) >= 2:
                    url, cb_kwargs = item[0], dict(item[1]).copy()
                elif len(item) == 1:
                    url, cb_kwargs = item[0], {}
                else:
                    raise ValueError(f'urls invalid, got {item!r}')

            # 更新数据
            urls[index] = url
            cb_kwargs.update(cb_kwargs_list[index])
            cb_kwargs_list[index] = cb_kwargs

        # 设置base_url
        if set_base_url:
            if isinstance(set_base_url, str):
                self.base_url = set_base_url
            elif not self.base_url:
                self.base_url = urllib.urljoin(urls[0], '.')

        # 提交异步任务
        tasks = [
            self.request(
                url=url,
                callback=callback,
                method=method,
                cb_kwargs=cb_kwargs,
                **req_kwargs
            )
            for url, cb_kwargs in zip(urls, cb_kwargs_list)
        ]
        return await asyncio.gather(*tasks, return_exceptions=return_exceptions)

    @staticmethod
    def _parse_gather_cb(length, cb_kwargs_list):
        """解析 gather 的回调参数"""
        # 设置 cb_kwargs_list
        if isinstance(cb_kwargs_list, (list, tuple)):
            cb_kwargs_list = cb_kwargs_list[:length]
            cb_kwargs_list.extend(
                [{}] * (length - len(cb_kwargs_list))
            )

        elif isinstance(cb_kwargs_list, dict):
            cb_kwargs_list = [cb_kwargs_list] * length

        else:
            cb_kwargs_list = [{}] * length
        # 将每项转化为字典
        cb_kwargs_list = [dict(item) for item in cb_kwargs_list]
        return cb_kwargs_list

    async def parse(self, response: Response, **kwargs):
        """默认解析函数"""
        raise NotImplementedError(f'{self.__class__.__name__}.parse not implemented')

    async def completed(self, result: list):
        """运行完成结果回调函数"""

    async def open(self):
        """创建 aiohttp session 之前调用"""

    async def close(self):
        """关闭 aiohttp session 之后调用"""

    async def start(self):
        """创建 aiohttp session 之后调用"""

    async def stop(self):
        """关闭 aiohttp session 之前调用"""

    async def sleep(self, delay: Union[int, float, None] = None, result: Any = None):
        """异步休眠

        :param delay: 休眠时间
        :param result: 返回值
        :return: result
        """
        if delay is None:
            if not isinstance(self.async_sleep, (int, float)) or self.async_sleep < 0:
                raise ValueError(f'async_sleep must be a positive integer(正整数), got {self.async_sleep!r}')
            delay = self.async_sleep

        elif not isinstance(delay, (int, float)) or delay < 0:
            raise ValueError(f'delay must be a positive integer(正整数), got {delay!r}')

        return await asyncio.sleep(delay, result=result)

    def build_url(self, _url) -> URL:
        """构造完整url地址"""
        if not isinstance(_url, (str, yarl.URL)):
            return _url
        _url = yarl.URL(_url)
        if _url.is_absolute():
            return _url
        if self._base_url and isinstance(self._base_url, yarl.URL):
            return self._base_url.join(_url)
        return _url

    @staticmethod
    def set_base_url(url: URL) -> URL:
        """设置 base_url"""
        if not url or not isinstance(url, (str, yarl.URL)):
            return None
        url = yarl.URL(url)
        if not url.is_absolute():
            # 不是绝对路径
            return None
        return url

    @property
    def loop(self) -> EventLoop:
        """event loop"""
        return self._loop

    @property
    def session(self) -> Session:
        """aiohttp session"""
        return self._session

    @property
    def base_url(self) -> URL:
        """base_url"""
        return self._base_url

    @base_url.setter
    def base_url(self, _url: URL):
        self._base_url = self.set_base_url(_url)


async def xpath(
    self,
    query: str,
    text: Optional[str] = None,
    type: Optional[str] = None,
    encoding: Optional[str] = None,
    base_url: Optional[str] = None,
    namespaces: Optional[Mapping[str, str]] = None,
    **kwargs: Any,
):
    """aiohttp.ClientResponse - selector.xpath

    :param self: aiohttp.ClientResponse 实例
    :param query: xpath查询字符串
    :param text: str对象
    :param type: 文件类型 - "html"(default), "json", or "xml"
    :param encoding: text encoding
    :param base_url: 为文档设置URL
    :param namespaces: `namespaces` is an optional `prefix: namespace-uri` mapping (dict)
        for additional prefixes to those registered with `register_namespace(prefix, uri)`.
        Contrary to `register_namespace()`, these prefixes are not
        saved for future calls.
    :param kwargs: xpath kwargs
    """
    try:
        if not text:
            text = await self.text(encoding, errors='ignore')

    except UnicodeError:
        text = await self.read()
        encoding = chardet(text).encoding
        text = text.decode(encoding, errors="ignore")

    # selector
    sel = selector.Selector(
        text=text,
        type=type,
        base_url=base_url,
        encoding=encoding or self.get_encoding(),
        namespaces=namespaces
    )
    # xpath
    return sel.xpath(query=query, **kwargs)


async def css(
    self,
    query: str,
    text: Optional[str] = None,
    type: Optional[str] = None,
    encoding: Optional[str] = None,
    base_url: Optional[str] = None,
    namespaces: Optional[Mapping[str, str]] = None,
):
    """aiohttp.ClientResponse - selector.css

    :param self: aiohttp.ClientResponse 实例
    :param query: xpath查询字符串
    :param text: str对象
    :param type: 文件类型 - "html"(default), "json", or "xml"
    :param encoding: text encoding
    :param base_url: 为文档设置URL
    :param namespaces:
        `namespaces` is an optional `prefix: namespace-uri` mapping (dict)
        for additional prefixes to those registered with `register_namespace(prefix, uri)`.
        Contrary to `register_namespace()`, these prefixes are not
        saved for future calls.
    """
    try:
        if not text:
            text = await self.text(encoding, errors='ignore')

    except UnicodeError:
        text = await self.read()
        encoding = chardet(text).encoding
        text = text.decode(encoding, errors="ignore")

    # selector
    sel = selector.Selector(
        text=text,
        type=type,
        base_url=base_url,
        encoding=encoding or self.get_encoding(),
        namespaces=namespaces
    )
    # css
    return sel.css(query=query)


async def re(
    self,
    regex: str,
    text: Optional[str] = None,
    type: Optional[str] = None,
    encoding: Optional[str] = None,
    base_url: Optional[str] = None,
    namespaces: Optional[Mapping[str, str]] = None,
    replace_entities: bool = True,
):
    """aiohttp.ClientResponse - selector.re

    :param self: aiohttp.ClientResponse 实例
    :param regex: 编译的正则表达式 或者 字符串
    :param text: str对象
    :param type: 文件类型 - "html"(default), "json", or "xml"
    :param encoding: text encoding
    :param base_url: 为文档设置URL
    :param namespaces:
        `namespaces` is an optional `prefix: namespace-uri` mapping (dict)
        for additional prefixes to those registered with `register_namespace(prefix, uri)`.
        Contrary to `register_namespace()`, these prefixes are not
        saved for future calls.
    :param replace_entities:
        By default, character entity references are replaced by their
        corresponding character (except for ``&amp;`` and ``&lt;``).
        Passing ``replace_entities`` as ``False`` switches off these
        replacements.
    """
    try:
        if not text:
            text = await self.text(encoding, errors='ignore')

    except UnicodeError:
        text = await self.read()
        encoding = chardet(text).encoding
        text = text.decode(encoding, errors="ignore")

    # selector
    sel = selector.Selector(
        text=text,
        type=type,
        base_url=base_url,
        encoding=encoding or self.get_encoding(),
        namespaces=namespaces
    )
    # re
    return sel.re(regex=regex, replace_entities=replace_entities)


def urljoin(self, _url):
    """urljoin

    :param self: aiohttp.ClientResponse 实例
    :param _url: url
    :return: url
    """
    if isinstance(_url, str):
        _url = yarl.URL(_url)
    elif not isinstance(_url, yarl.URL):
        return _url

    if _url.is_absolute():
        return _url

    return self.url.join(_url)


def add_instance_method(response):
    """为异步response添加实例方法 - re, css, xpath, urljoin"""
    setattr(response, 're', MethodType(re, response))
    setattr(response, 'css', MethodType(css, response))
    setattr(response, 'xpath', MethodType(xpath, response))
    setattr(response, 'urljoin', MethodType(urljoin, response))
