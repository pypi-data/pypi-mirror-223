import os
from typing import Optional, Union
from multidict import CIMultiDict

import m3u8

from pyxk.m3u8._initial import _M3U8Init
from pyxk.m3u8.downloader import Downloader
from pyxk import (
    chardet,
    normpath,
    LazyLoader,
    human_playtime,
    read_file_by_generator
)

_box = LazyLoader("_box", globals(), "rich.box")
_live = LazyLoader("_live", globals(), "rich.live")
_panel = LazyLoader("_panel", globals(), "rich.panel")
_table = LazyLoader("_table", globals(), "rich.table")


__all__ = ['M3u8Parser', 'load_url', 'load_content']


class M3u8Parser(_M3U8Init):

    def load_content(
        self,
        content: str,
        url: Optional[str] = None,
        output: Optional[str] = None,
        verify: Optional[bool] = None,
        headers: Union[dict, CIMultiDict, None] = None,
        user_agent: Optional[str] = None,
        reload: Optional[bool] = None,
        reserve: Optional[bool] = None,
        limit: Optional[int] = None
    ):
        """load m3u8 url

        :param content: m3u8 content
        :param url: m3u8 url
        :param output: 文件输出路径
        :param verify: verify ssl
        :param headers: Headers
        :param user_agent: User agent
        :param reload: 重载m3u8文件
        :param reserve: 下载完成保留m3u8文件
        :param limit: 异步下载limit
        """
        # 文件路径
        self.output = output

        # 初始化数据
        self._initialization(
            verify=verify,
            headers=headers,
            user_agent=user_agent,
            reload=reload,
            reserve=reserve,
            limit=limit
        )

        # 无效 m3u8 content
        if not isinstance(content, str) or not content:
            raise TypeError('Invalid m3u8 content')

        # 查看是否是本地文件
        file = normpath(os.path.join(self.store, content))
        if not self._is_m3u8(content) and os.path.isfile(file):
            _content = b''

            for index, chunk in enumerate(read_file_by_generator(file, 'rb')):
                # 检查是否是m3u8内容
                if index == 0 and not self._is_m3u8(chunk):
                    break
                _content += chunk
            content = _content.decode(
                chardet(_content).encoding or 'utf-8'
            )

        # 解析m3u8
        self.start_parse(content, url)

    def load_url(
        self,
        url: str,
        output: Optional[str] = None,
        verify: Optional[bool] = None,
        headers: Union[dict, CIMultiDict, None] = None,
        user_agent: Optional[str] = None,
        reload: Optional[bool] = None,
        reserve: Optional[bool] = None,
        limit: Optional[int] = None
    ):
        """load m3u8 url

        :param url: m3u8 url
        :param output: 文件输出路径
        :param verify: verify ssl
        :param headers: Headers
        :param user_agent: User agent
        :param reload: 重载m3u8文件
        :param reserve: 下载完成保留m3u8文件
        :param limit: 异步下载limit
        """
        # 文件路径
        self.output = output

        # 初始化数据
        self._initialization(
            verify=verify,
            headers=headers,
            user_agent=user_agent,
            reload=reload,
            reserve=reserve,
            limit=limit
        )
        content = self.get_m3u8_content(url)

        # 无效m3u8数据
        if not content:
            self.console.print(
                f'[red b]Invalid m3u8 url[/]: <{url}>'
            )
            return

        # 解析m3u8
        self.start_parse(content=content, url=url)

    def start_parse(self, content: str, url: Optional[str] = None):
        """开始解析m3u8数据

        :param content: m3u8内容
        :param url: m3u8 url
        """
        m3u8obj = m3u8.loads(content=content, uri=url)
        m3u8obj, new_url = self._parse_playlists(m3u8obj, url)
        m3u8keys = self._parse_m3u8keys(m3u8obj)
        segments, durations = self._parse_segments(m3u8obj, new_url)

        # 无效m3u8数据
        if not segments:
            self.console.print(f'[red b]Invalid m3u8 content[/], url: {url}')
            return

        # 可视化解析结果
        table = _table.Table(show_header=False, box=_box.SIMPLE_HEAD)

        table.add_column(overflow='fold')
        table.add_row(f'[blue u]{url}[/]')
        table.add_section()

        m3u8_info = [
            f'[yellow b]maximum[/]: {len(segments)}',
            f'[yellow b]durations[/]: {human_playtime(durations)}',
            f'[yellow b]output[/]: {self.output}'
        ]
        for row in m3u8_info:
            table.add_row(row)

        panel = _panel.Panel(
            table,
            box=_box.ASCII2,
            border_style='bright_blue',
            title='[red]M3U8 Downloader[/]',
            title_align='center',
            subtitle=f'[dim i]limit: {self.limit}[/]',
            subtitle_align='right',
            expand=False,
        )

        # 没有 output 展示解析结果即可
        if not self.output:
            self.console.print(panel)
            return

        # 创建segments文件夹
        os.makedirs(self._temp_segments, exist_ok=True)

        # 开启下载
        with _live.Live(panel, console=self.console):
            Downloader.run(
                start_urls=segments,
                m3u8keys=m3u8keys,
                semaphore=self.limit,
                headers=self.headers,
                user_agent=self.user_agent,
                verify=self._verify,
                output=self.output,
                table=table,
                console=self.console,
                temp=self._temp_segments,
            )

        # 删除m3u8文件
        if not os.path.isfile(self.output):
            self._reserve = False

        if self._reserve is True:
            import shutil
            shutil.rmtree(self.temp)
        # 清空请求历史
        self.history.clear()

    def _parse_segments(self, m3u8obj, url):
        """解析 m3u8 segments"""
        # 无效的 m3u8 文件
        if not m3u8obj.is_endlist:
            return None, None

        # all segments
        segments, durations = [], 0

        for index, segment in enumerate(m3u8obj.segments):
            # segments 绝对路径
            segment.uri = segment.absolute_uri

            # segment key
            key = segment.key.uri if segment.key else None

            # 保存 segment
            item = (
                segment.uri,
                {
                    'file': normpath(
                        os.path.join(self._temp_segments, str(index)+'.ts')
                    ) if self.output else None,
                    'key': key
                }
            )
            segments.append(item)
            # segment 时间累加
            durations += segment.duration

        # 保存 m3u8 文件
        self.sava_m3u8_content(url, m3u8obj.dumps())
        return segments, durations

    def _parse_m3u8keys(self, m3u8obj):
        """解析 m3u8 keys"""
        keys = {}

        for key in m3u8obj.keys:
            # 无效key
            if not key:
                continue

            key.uri = key.absolute_uri
            # 获取 密钥 和 偏移量
            secret = self.get_m3u8_content(key.uri, True)[:16]
            iv = key.iv.removeprefix('0x')[:16].encode() if key.iv else secret
            # 保存key
            keys[key.uri] = {'key': secret, 'iv': iv}

            # 保存密钥到本地
            self.sava_m3u8_content(key.uri, secret, True)

        return keys

    def _parse_playlists(self, m3u8obj, url=None):
        """解析 m3u8 playlists"""

        # 没有 playlists
        if not m3u8obj.is_variant:
            return m3u8obj, url

        def sorted_playlists(playlist):
            """对 playlists 进行排序"""
            playlist.uri = playlist.absolute_uri
            return playlist.stream_info.bandwidth

        # 对 playlists 进行排序
        playlists = sorted(m3u8obj.playlists, key=sorted_playlists)

        # 保存m3u8文件
        self.sava_m3u8_content(url, m3u8obj.dumps())

        # 获取带宽最大的 playlist
        new_url = playlists[-1].uri
        new_m3u8obj = m3u8.loads(self.get_m3u8_content(new_url), new_url)

        return self._parse_playlists(new_m3u8obj, new_url)


def load_content(
    content: str,
    url: Optional[str] = None,
    output: Optional[str] = None,
    verify: Optional[bool] = None,
    headers: Union[dict, CIMultiDict, None] = None,
    user_agent: Optional[str] = None,
    reload: Optional[bool] = None,
    reserve: Optional[bool] = None,
    limit: Optional[int] = None
):
    """load m3u8 url

    :param content: m3u8 content
    :param url: m3u8 url
    :param output: 文件输出路径
    :param verify: verify ssl
    :param headers: Headers
    :param user_agent: User agent
    :param reload: 重载m3u8文件
    :param reserve: 下载完成保留m3u8文件
    :param limit: 异步下载limit
    """
    m3u8parse = M3u8Parser()
    m3u8parse.load_content(
        content=content,
        url=url,
        output=output,
        verify=verify,
        headers=headers,
        user_agent=user_agent,
        reload=reload,
        reserve=reserve,
        limit=limit
    )


def load_url(
    url: str,
    output: Optional[str] = None,
    verify: Optional[bool] = None,
    headers: Union[dict, CIMultiDict, None] = None,
    user_agent: Optional[str] = None,
    reload: Optional[bool] = None,
    reserve: Optional[bool] = None,
    limit: Optional[int] = None
):
    """load m3u8 url

    :param url: m3u8 url
    :param output: 文件输出路径
    :param verify: verify ssl
    :param headers: Headers
    :param user_agent: User agent
    :param reload: 重载m3u8文件
    :param reserve: 下载完成保留m3u8文件
    :param limit: 异步下载limit
    """
    m3u8parse = M3u8Parser()
    m3u8parse.load_url(
        url=url,
        output=output,
        verify=verify,
        headers=headers,
        user_agent=user_agent,
        reload=reload,
        reserve=reserve,
        limit=limit
    )
