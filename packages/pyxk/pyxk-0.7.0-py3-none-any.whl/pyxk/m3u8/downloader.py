import os
import shlex
import subprocess
from typing import Optional
from concurrent.futures import ThreadPoolExecutor

import aiofiles

from pyxk import (
    Client,
    Response,
    tasks_progress,
    download_progress
)
from pyxk.aes import Crypto, MODES


class Downloader(Client):

    limit = 1000
    timeout = 100
    warning = False
    status_error_list = list(range(400, 411))
    until_request_succeed = [200]

    def __init__(
        self,
        table: object,
        output: str,
        m3u8keys: dict,
        start_urls: list,
        console: object,
        temp: str,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.ciphers = {
            url: Crypto(keys['key'], MODES.CBC, iv=keys['iv'])
            for url, keys in m3u8keys.items()
        }
        self.table = table
        self.output = output
        self.start_urls = start_urls

        # 进度条
        self.progress = tasks_progress()
        self.task = self.progress.add_task('', total=len(self.start_urls))

        # 添加进度条到live
        self.table.add_section()
        self.table.add_row(self.progress)

        self.temp = temp
        self.console = console

    async def start_request(self):

        ret = []
        for item in self.start_urls.copy():
            file = item[1]['file']
            ret.append(file)

            # 本地存在文件
            if os.path.isfile(file) and os.path.getsize(file) > 0:
                self.start_urls.remove(item)
                continue

        # 更新进度条
        self.progress.update(
            self.task,
            completed=len(ret)-len(self.start_urls)
        )

        # 没有下载数据
        if not self.start_urls:
            return ret

        await super().start_request()
        return ret

    async def parse(self, response: Response, file: str, key: Optional[str]):
        """解析segment数据"""
        # 获取segment内容
        content = await response.content.read()
        # 解密
        if key:
            content = self.ciphers[key].decrypt(content)

        async with aiofiles.open(file, 'wb') as write_file_obj:
            # 本地存储
            await write_file_obj.write(content)

        # 更新进度条
        self.progress.update(self.task, advance=1)

    async def completed(self, ret: list):
        """使用模块ffmpeg合并m3u8"""
        if not ret:
            return

        # 创建 filelist 文件
        filelist, filesize = os.path.join(self.temp, "filelist.txt"), 0

        with open(filelist, "w", encoding="utf-8") as write_fileobj:
            for file in ret:
                write_fileobj.write(f"file '{file}'\n")
                filesize += (os.path.getsize(file) - 16400)

        # ffmpeg 视频合并代码, 监测合并完成状态
        args = shlex.split(
            f"ffmpeg -loglevel quiet -f concat -safe 0 -i {filelist} -c copy {self.output} -y"
        )
        merge_completed = False

        # ffmpeg 合并函数
        def merge_segments():
            try:
                subprocess.run(args=args, check=True)
            except FileNotFoundError:
                self.console.log("[red]ffmpeg is not available![/]")
            finally:
                nonlocal merge_completed
                merge_completed = True

        # 合并进度条
        def merge_progress():
            from time import sleep

            sleep(0.2)
            if merge_completed:
                return

            completed_filezise = lambda :os.path.getsize(self.output) if os.path.isfile(self.output) else 0
            progress = download_progress(transient=True)
            task = progress.add_task(
                description="", total=filesize, visible=False
            )
            self.table.add_row(progress)

            while True:
                # 停止循环
                if merge_completed:
                    progress.update(task, completed=filesize, visible=False)
                    break

                progress.update(task, completed=completed_filezise(), visible=True)
                sleep(0.25)

        # 开启多线程
        pool = ThreadPoolExecutor()
        pool.submit(merge_segments)
        pool.submit(merge_progress)
        pool.shutdown()
