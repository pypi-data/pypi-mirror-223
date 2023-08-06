import os
from typing import Optional, Union
from multidict import CIMultiDict

from pyxk import (
    md5,
    rename,
    chardet,
    Session,
    normpath,
    make_open,
    default_headers,
    read_file_by_generator
)


class _M3U8Init:

    def __init__(
        self,
        store: Optional[str] = None,
        verify: bool = True,
        headers: Union[dict, CIMultiDict] = default_headers(),
        user_agent: Optional[str] = None,
        reload: bool = False,
        reserve: bool = False,
        limit: int = 16,
    ):
        """m3u8解析器

        :param store: m3u8文件 保存文件夹路径
        :param verify: verify ssl
        :param headers: Headers
        :param user_agent: User agent
        :param reload: 重载m3u8文件
        :param reserve: 下载完成保留m3u8文件
        :param limit: 异步下载limit
        """
        # 存储文件夹
        self._store = self._norm_store(store)
        # verify ssl
        self._verify = bool(verify)
        # headers
        self._headers = CIMultiDict(headers)
        # user agent
        if user_agent and isinstance(user_agent, str):
            self._headers['User-Agent'] = user_agent
        else:
            user_agent = None
        # reload 重载m3u8文件
        self._reload = bool(reload)
        # 保留m3u8文件
        self._reserve = bool(reserve)
        # 异步下载limit
        self._limit = limit
        # request session
        self._session = Session(headers=headers, user_agent=user_agent)
        # 文件名称
        self._output = None
        # 网络访问历史记录
        self.history = []

    @property
    def store(self) -> Optional[str]:
        """文件保存文件夹"""
        return self._store

    @store.setter
    def store(self, value):
        self._store = self._norm_store(value)

    @staticmethod
    def _norm_store(value) -> Optional[str]:
        """输入文件夹路径"""
        if value is None:
            return normpath(os.getcwd())

        # store 类型无效
        if not isinstance(value, str) or not value:
            raise TypeError(f'store must be a str, got {value!r}')

        return normpath(os.path.abspath(normpath(value)))

    @property
    def output(self) -> Optional[str]:
        """m3u8文件保存路径"""
        return self._output

    @output.setter
    def output(self, value):
        self._output = self._norm_output(value)

    def _norm_output(self, value, suffix='mp4') -> Optional[str]:
        """输入文件"""
        # 没有output
        if value is None or not value:
            return None

        # output 类型无效
        if not isinstance(value, str):
            raise TypeError(f'output must be a str, got {value!r}')

        # 绝对路径
        value = normpath(value)
        if not os.path.isabs(value):
            value = os.path.join(self.store, value)

        rename_file = rename(value, suffix=suffix)
        self._store = rename_file.dirname
        return rename_file.result

    @property
    def temp(self) -> Optional[str]:
        """m3u8 临时文件夹"""
        if not self.output:
            return None

        dir_name, basename = os.path.split(self.output)
        return normpath(os.path.join(dir_name, basename.removesuffix('mp4') + 'temp'))

    @property
    def _temp_segments(self) -> Optional[str]:
        """segments保存临时文件夹"""
        if not self.temp:
            return None

        return normpath(os.path.join(self.temp, 'segments'))

    @property
    def user_agent(self) -> str:
        """user agent string"""
        return self._headers.get('User-Agent')

    @user_agent.setter
    def user_agent(self, value):
        if not isinstance(value, str):
            raise ValueError(f'user_agent must be a str, got {value!r}')

        self._headers.update({'User-Agent': value})
        self.session.user_agent = value

    @property
    def headers(self) -> Union[dict, CIMultiDict]:
        """Request Headers"""
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers.update(dict(value))
        self._session.headers.update(self._headers)

    @property
    def limit(self) -> int:
        """download limit"""
        return self._limit

    @limit.setter
    def limit(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f'limit must be a positive integer(正整数), got {value!r}')

        self._limit = value

    @property
    def session(self):
        """requests session"""
        return self._session

    @property
    def console(self):
        """rich console"""
        return self._session.console

    def _initialization(
        self, verify, headers, user_agent, reload, reserve, limit
    ):
        """初始化变量"""
        if verify is not None:
            self._verify = bool(verify)
        if headers is not None:
            self.headers = headers
        if user_agent is not None:
            self.user_agent = user_agent
        if reload is not None:
            self._reload = bool(reload)
        if reserve is not None:
            self._reserve = bool(reversed)
        if limit is not None:
            self.limit = limit

    def generate_filename(self, url: Optional[str], is_key: bool = False) -> Optional[str]:
        """生成文件名称

        :param url: m3u8 url
        :param is_key: 是否为m3u8密钥
        :return:
        """
        if not self.output or not url:
            return None

        # 加密后的文件名称
        basename = md5(url).ciphertext + ('.key' if is_key else '.m3u8')
        return normpath(os.path.join(self.temp, basename))

    def get_m3u8_content(self, url: Optional[str], is_key: bool = False):
        """获取 m3u8 内容

        :param url: m3u8 链接
        :param is_key: 是否为m3u8密钥
        :return:
        """
        # 获取文件名称
        filename = self.generate_filename(url, is_key)

        if self._reload or not filename or not os.path.isfile(filename):
            return self._content_from_url(url, is_key)

        return self._content_from_file(filename, is_key)

    def _content_from_url(self, url: str, is_key: bool = False) -> Union[str, bytes]:
        """获取网络资源 - m3u8 content

        :param url: m3u8 url
        :param is_key: 是否为m3u8密钥
        :return: Union[str, bytes]
        """

        content = b''
        response = self.session.get(url, verify=self._verify, timeout=10, stream=True)
        response.raise_for_status()
        self.history.append(response)

        for index, chunk in enumerate(response.iter_content(1024)):
            # 检查是否是m3u8内容
            if not is_key and index == 0 and not self._is_m3u8(chunk):
                break
            content += chunk

        # m3u8 content 编码转换
        if not is_key:
            content = content.decode(
                chardet(content).encoding or 'utf-8'
            )

        return content

    def _content_from_file(self, file: str, is_key: bool = False) -> Union[str, bytes]:
        """获取本地资源 - m3u8 content

        :param file: m3u8 file
        :param is_key: 是否为m3u8密钥
        :return: Union[str, bytes]
        """
        # 获取本地文件
        content = b'' if is_key else ''

        for index, chunk in enumerate(
            read_file_by_generator(
                file=file,
                mode='rb' if is_key else 'r',
                encoding=None if is_key else 'utf-8'
            )
        ):
            # 检查是否是m3u8内容
            if not is_key and index == 0 and not self._is_m3u8(chunk):
                break
            content += chunk

        return content

    def sava_m3u8_content(self, url: Optional[str], content: Union[str, bytes], is_key: bool = False):
        """保存m3u8文件到本地

        :param url: m3u8 url
        :param content: m3u8 content
        :param is_key: 是否为m3u8密钥
        :return:
        """
        filename = self.generate_filename(url, is_key)

        # 无效文件
        if not filename:
            return

        # 保存文件
        if self._reload or not os.path.isfile(filename):
            with make_open(
                file=filename,
                mode='wb' if is_key else 'w',
                encoding=None if is_key else 'utf-8'
            ) as write_file_obj:
                write_file_obj.write(content)

    @staticmethod
    def _is_m3u8(_data: Union[str, bytes], /) -> bool:
        """检查是否是m3u8文本

        :param _data: content
        :return: bool
        """
        if isinstance(_data, str):
            return _data.startswith('#EXTM3U')

        if isinstance(_data, bytes):
            return _data.startswith(b'#EXTM3U')

        return False
