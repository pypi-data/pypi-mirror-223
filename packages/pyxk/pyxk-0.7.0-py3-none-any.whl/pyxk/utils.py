import io
import logging
from types import ModuleType
from importlib import import_module
from collections import namedtuple
from typing import IO, Any, Union, Optional


__all__ = [
    'LazyLoader', 'runtime', 'runtime_coro', 'make_open', 'Chardet',
    'get_user_agent', 'default_headers', 'md5', 'hash256', 'normpath',
    'is_base64_from_regex', 'base64_conversion_bytes', 'rename_file', 'rename_folder', 'rename',
    'str_conversion_digit', 'human_playtime', 'pycode_conversion_lazy_loader', 'pyfile_conversion_lazy_loader',
    'units_conversion_from_byte', 'download_progress', 'tasks_progress', 'chardet', 'read_file_by_generator'
]


class LazyLoader(ModuleType):
    """模块延迟加载"""

    def __init__(
        self,
        local_name: str,
        parent_module_globals: dict,
        name: Optional[str] = None,
        warning: Optional[str] = None
    ):
        """模块延迟加载 init

        :param local_name: 父模块引用名称
        :param parent_module_globals: 父模块全局变量
        :param name: 导入模块名称
        :param warning: 警告信息
        """
        self._local_name = local_name
        self._parent_module_globals = parent_module_globals
        self._warning = warning
        super().__init__(name or local_name)

    def _load(self):
        """加载模块并将其插入父模块的全局变量中"""
        # 导入模块
        module = import_module(self.__name__)
        self._parent_module_globals[self._local_name] = module

        # 如果指定了警告，则发出警告
        if self._warning:
            logging.warning(self._warning)
            # 确保只警告一次
            self._warning = None

        # 将模块的方法和变量注册到当前对象下
        self.__dict__.update(module.__dict__)
        return module

    def __getattr__(self, item):
        module = self._load()
        return getattr(module, item)

    def __dir__(self):
        module = self._load()
        return dir(module)


# 延迟加载模块
os = LazyLoader('os', globals(), 'os')
re = LazyLoader('re', globals(), 're')
time = LazyLoader('time', globals(), 'time')
base64 = LazyLoader('base64', globals(), 'base64')
hashlib = LazyLoader('hashlib', globals(), 'hashlib')
difflib = LazyLoader('difflib', globals(), 'difflib')
_chardet = LazyLoader('_chardet', globals(), 'chardet')
warnings = LazyLoader('warnings', globals(), 'warnings')
functools = LazyLoader('functools', globals(), 'functools')
itertools = LazyLoader('itertools', globals(), 'itertools')
collections = LazyLoader('collections', globals(), 'collections')
_console = LazyLoader('_console', globals(), 'rich.console')


# 命名元组
_md5_nametuple = namedtuple('MD5NameTuple', 'ciphertext,plaintext')
_hash256_nametuple = namedtuple('Hash256NameTuple', 'ciphertext,plaintext')
_base64_nametuple = namedtuple('Base64NameTuple', 'result,is_base64')
_rename_nametuple = namedtuple('RenameNameTuple', 'result,dirname,basename')
_str_conversion_digit_nametuple = namedtuple('StrConversionDigitNameTuple', 'result,raw,is_digit')
_units_conversion_nametuple = namedtuple('UnitsConversionNameTuple', 'result,raw,units')
_chardet_nametuple = namedtuple('ChardetNameTuple', 'encoding,language,confidence')


def runtime(func):
    """装饰器: 计算函数运行时间"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        con = _console.Console()
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            con.print(f'{func.__name__!r} [magenta]running time[/]: {end_time - start_time}')
        return result

    return wrapper


def runtime_coro(func):
    """装饰器: 计算异步函数运行时间"""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        con = _console.Console()
        start_time = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            con.print(f'{func.__name__!r} [magenta]running time[/]: {end_time - start_time}')
        return result

    return wrapper


def _make_open(func):
    """内置方法open装饰器 - 文件模式 w/a 下，创建不存在的目录"""

    @functools.wraps(func)
    def wrapper(
        file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None
    ) -> IO:
        if not isinstance(mode, str):
            raise TypeError(f"{func.__name__}() argument the 'mode' type must be str, got: {type(mode)}")

        # collections.Counter 统计可迭代对象 每项出现的次数 & itertools.product 求多个可迭代对象的笛卡尔积
        mode_list = [collections.Counter(i + j) for i, j in itertools.product('wa', ('b', 'b+', '', '+'))]
        if collections.Counter(mode) in mode_list:
            os.makedirs(os.path.dirname(file), exist_ok=True)

        # 二进制模式下 encoding=None
        if mode.find('b') != -1 and encoding is not None:
            logging.warning("binary mode doesn't take an encoding argument")
            encoding = None

        return func(file, mode, buffering, encoding, errors, newline, closefd, opener)
    return wrapper


make_open = _make_open(io.open)


def get_user_agent(ua: Optional[str] = 'android', overwrite: bool = False) -> str:
    """获取 UserAgent，默认 Android

    :param ua: 模糊查找内置字典User-Agent (android, windows, mac, iphone, ipad, symbian, apad)
    :param overwrite: 若为True, 直接返回  User-Agent
    :return: str
    """
    user_agent_dict = {
        'android': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/90.0.4430.91 Mobile Safari/537.36',
        'windows': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/86.0.4240.198 Safari/537.36',
        'mac': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
               'Chrome/86.0.4240.198 Safari/537.36',
        'iphone': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) '
                  'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'ipad': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                'CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
        'symbian': 'Mozilla/5.0 (Symbian/3; Series60/5.2 NokiaN8-00/012.002; Profile/MIDP-2.1 Configuration/CLDC-1.1 ) '
                   'AppleWebKit/533.4 (KHTML, like Gecko) NokiaBrowser/7.3.0 Mobile Safari/533.4 3gpp-gba',
        'apad': 'Mozilla/5.0 (Linux; Android 11; Phh-Treble vanilla Build/RQ3A.211001.001;) '
                'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.91 Safari/537.36',
    }

    if not isinstance(ua, str):
        if ua is not None:
            raise TypeError(f"'ua' type must be a str, got: {type(ua)}")

        return user_agent_dict['android']

    # 重写 UserAgent
    if overwrite:
        return ua

    # 模糊查找 UserAgent
    ua = difflib.get_close_matches(ua.lower(), user_agent_dict.keys(), 1)
    if not ua:
        return user_agent_dict['android']
    return user_agent_dict[ua[0]]


def default_headers(ua: Optional[str] = 'android', **kwargs) -> dict:
    """Headers

    :param ua: user-agent
    :return: dict -> {'User-Agent': str}
    """
    _headers = {'User-Agent': get_user_agent(ua)}
    _headers.update(kwargs)
    return _headers


def md5(
    plaintext: Union[str, bytes],
    encoding: str = 'utf-8',
    default: Any = None
) -> _md5_nametuple:
    """MD5加密

    :param plaintext: 需加密明文
    :param encoding: plaintext编码
    :param default: ciphertext默认值
    :return: tuple -> (plaintext: 'plaintext', ciphertext: 'ciphertext')
    """
    result = _md5_nametuple(default, plaintext)

    if not isinstance(plaintext, (str, bytes)):
        return result

    # plaintext type str
    if isinstance(plaintext, str):
        plaintext = plaintext.encode(encoding=encoding)

    # md5加密
    result = result._replace(
        ciphertext=hashlib.md5(plaintext).hexdigest()
    )
    return result


def hash256(
    plaintext: Union[str, bytes],
    encoding: str = 'utf-8',
    default: Any = None
) -> _hash256_nametuple:
    """HASH_256加密

    :param plaintext: 需加密明文
    :param encoding: plaintext编码
    :param default: ciphertext默认值
    :return: tuple -> (plaintext: 'plaintext', ciphertext: 'ciphertext')
    """

    result = _hash256_nametuple(default, plaintext)

    if not isinstance(plaintext, (str, bytes)):
        return result

    # plaintext type str
    if isinstance(plaintext, str):
        plaintext = plaintext.encode(encoding=encoding)

    # hash256加密
    result = result._replace(
        ciphertext=hashlib.sha256(plaintext).hexdigest()
    )
    return result


def is_base64_from_regex(data: Union[str, bytes]) -> bool:
    """判断是否为base64数据类型

    :param data: 需检测的数据
    :return: bool
    """
    # base64 数据类型 正则表达式判断
    if isinstance(data, bytes):
        pattern_from_bytes = re.compile(rb'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$')
        return bool(pattern_from_bytes.match(data))

    # base64 数据类型 正则表达式判断
    if isinstance(data, str):
        pattern_from_string = re.compile(r'^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)?$')
        return bool(pattern_from_string.match(data))

    # str 或 bytes 以外类型返回 False
    return False


def base64_conversion_bytes(
    data: Union[str, bytes],
    encoding: str = 'utf-8',
    default: Any = None
) -> _base64_nametuple:
    """base64数据类型 转化为bytes

    :param data: data: data
    :param encoding: data数据编码
    :param default: 返回默认值
    :return: tuple -> (result: 'result', is_base64: 'is_base64')
    """
    result = _base64_nametuple(default, False)

    if (
        not isinstance(data, (str, bytes))
        or not is_base64_from_regex(data)
    ):
        return result

    if isinstance(data, str):
        data = data.encode(encoding)


    result = result._replace(
        result=base64.b64decode(data),
        is_base64=True
    )

    return result


def normpath(_path) -> str:
    """规范文件路径"""
    if not isinstance(_path, str):
        raise TypeError(f"'_path' type must be a str, got: {type(_path)}")

    return os.path.normpath(_path.strip()).replace('\\', '/')


def rename_file(file: str, suffix: Optional[str] = None, create: bool = False) -> _rename_nametuple:
    """重命名本地存在的文件

    :param file: 文件路径
    :param suffix: 文件后缀名
    :param create: 创建文件
    :return: tuple -> (result, dirname, basename)
    """
    # file 绝对路径
    file = normpath(os.path.abspath(file))
    if not os.path.basename(file):
        raise ValueError('file missing basename')

    # file 后缀名
    if suffix and isinstance(suffix, str):
        suffix = '.' + suffix.removeprefix('.')
    else:
        basename = os.path.basename(file).rsplit('.', 1)
        if len(basename) == 2 and 2 <= len(basename[1]) <= 8:
            suffix = '.' + basename[1].removeprefix('.')
        else:
            suffix = ''

    # 拼接完整file
    if not file.endswith(suffix):
        file += suffix

    # 重命名文件
    def _rename(f):
        """rename a file"""

        if create:
            from pathlib import Path
            Path(f).touch()
        return _rename_nametuple(f, *os.path.split(f))

    if not os.path.isfile(file):
        return _rename(file)

    for index in itertools.count(1):
        newfile = file.removesuffix(suffix) + f'.{index}{suffix}'
        if not os.path.isfile(newfile):
            return _rename(newfile)


rename = rename_file


def rename_folder(folder: str, create: bool = False) -> _rename_nametuple:
    """重命名本地存在的文件夹

    :param folder: 文件夹路径
    :param create: 创建文件夹
    :return: Tuple(result, dirname, basename)
    """
    # 获取folder绝对路径
    folder = normpath(os.path.abspath(folder))

    def get_folder(f):
        """获取重命名文件数据"""

        if create:
            os.makedirs(f, exist_ok=True)
        return _rename_nametuple(f, *os.path.split(f))

    if not os.path.isdir(folder):
        return get_folder(folder)

    # 重命名folder
    for index in itertools.count(1):
        new_folder = folder + f".{index}"
        if not os.path.isdir(new_folder):
            return get_folder(new_folder)


def str_conversion_digit(target: Union[str, int, float], default: Any = None) -> _str_conversion_digit_nametuple:
    """字符串转换为数字

    :param target: 需要转换的目标
    :param default: 返回默认值
    :return: tuple -> (result: digits, raw, is_digit: bool)
    """
    result = _str_conversion_digit_nametuple(default, target, False)

    # target type = `int` or `float`
    if isinstance(target, (int, float)):
        return result._replace(
            is_digit=True, result=target
        )

    # target type != `str`
    if not isinstance(target, str):
        return result

    # 判断字符串是否为数字
    def is_digits(string):
        pattern = re.match(r"^(?P<symbol>-)?(?P<int>\d+)(?P<float>\.\d+)?$", string)
        if not pattern:
            return {"is_digits": False, "type": lambda x: x}
        return {"is_digits": True, "type": float if pattern.groupdict()["float"] is not None else int}

    # 转换为数字
    _result = is_digits(target)
    if _result["is_digits"]:
        result = result._replace(
            is_digit=True, result=_result["type"](target)
        )
    return result


def human_playtime(playtime: Union[str, int, float], default: Any = None) -> Union[str, Any]:
    """人类直观时间展示

    :param playtime: 传入一个时间(秒), 返回人类能理解的时间格式
    :param default: 返回默认值
    :return: str
    """
    digit = str_conversion_digit(playtime)

    if not digit.is_digit:
        return default

    playtime = digit.result
    symbol, playtime = "-" if playtime < 0 else "", round(abs(playtime))

    hour, second = divmod(playtime, 3600)
    minute, second = divmod(second, 60)

    return f"{symbol}{hour}:{minute:0>2}:{second:0>2}"


def pycode_conversion_lazy_loader(string: str) -> str:
    """python代码中的导入模块转换为懒加载

    :param string: python代码
    :return: str
    """
    if not isinstance(string, str):
        raise TypeError(f"'string' type must be a str, got: {type(string)}")

    def repl_string(match):
        """替换懒加载"""
        match_dict, import_name, alias = match.groupdict(), None, None
        repl = '{alias} = LazyLoader("{alias}", globals(), "{import_name}")'

        # from导入
        if match_dict["from_name"]:
            import_name = f'{match_dict["from_name"]}.{match_dict["from_import_name"]}'
            alias = match_dict["from_import_name"]
        else:
            import_name = f'{match_dict["import_name"]}'
            alias = match_dict["import_name"]

        # alias
        if match_dict["from_import_alias"]:
            alias = match_dict["from_import_alias"]
        elif match_dict["import_alias"]:
            alias = match_dict["import_alias"]
        return repl.format(alias=alias, import_name=import_name)

    # 替换懒加载
    pattern = [
        r'^from\s+?(?P<from_name>\S+)\s+?import\s+?(?P<from_import_name>\S+)'
        r'\s*?(as\s+?(?P<from_import_alias>\S+))?$',
        r'^import\s+?(?P<import_name>\S+)(\s+?as\s+(?P<import_alias>\S+?))?\s*?$',
    ]
    return re.sub(pattern='|'.join(pattern), repl=repl_string, string=string, flags=re.M)


def pyfile_conversion_lazy_loader(read_file: str, write_file: str, encoding: Optional[str] = None) -> None:
    """python文件中的导入模块转换为懒加载

    :param read_file: 读取python代码文件
    :param write_file: 写入转换后的python代码文件
    :param encoding: 文件编码
    """
    with open(read_file, "r", encoding=encoding) as read_file_obj:
        content = pycode_conversion_lazy_loader(read_file_obj.read())
    with open(write_file, "w", encoding=encoding) as write_file_obj:
        write_file_obj.write(content)


def units_conversion_from_byte(target: Union[str, int, float], default: Any = None) -> _units_conversion_nametuple:
    """字节单位自动换算

    :param target: 换算目标(Bytes)
    :param default: 返回默认值
    :return: tuple -> (result, raw, units)
    """
    result = _units_conversion_nametuple(default, target, None)
    _temp = str_conversion_digit(target)

    if not _temp.is_digit:
        return result

    target = abs(_temp.result)
    target_units = 'Bytes'

    units_dict = {
        'Bytes': 1, 'KB': 1024, 'MB': 1024,
        'GB': 1024, 'TB': 1024, 'PB': 1024,
        'EB': 1024, 'ZB': 1024, 'YB': 1024, 'BB': 1024
    }

    for units, rate in units_dict.items():
        if target >= rate:
            target, target_units = target/rate, units
            continue
        break

    result = result._replace(
        units=target_units,
        result= f'{round(target, 2)}{target_units}'

    )
    return result


class Chardet:
    """字符集编码探测"""

    def __init__(self, should_rename_legacy: bool = False):
        """Chardet初始化

        :param should_rename_legacy: should_rename_legacy
        """
        # 编码探测器
        self.detector = _chardet.UniversalDetector(
            should_rename_legacy=should_rename_legacy
        )

    @classmethod
    def chardet(
        cls,
        byte_str: Union[bytes, bytearray],
        should_rename_legacy: bool = False
    ) -> _chardet_nametuple:
        """字符编码探测

        :param byte_str: bytes数据
        :param should_rename_legacy: should_rename_legacy:
        :return: tuple -> (encoding: str, language: str, confidence: float)
        """
        # 无效数据类型
        if not isinstance(byte_str, bytearray):
            if not isinstance(byte_str, bytes):
                raise TypeError(
                    f"'byte_str' type must be a bytes or bytearray, got: {type(byte_str)}"
                )
            byte_str = bytearray(byte_str)

        self = cls(
            should_rename_legacy=should_rename_legacy
        )
        self.feed(byte_str)
        return self.close()

    def feed(self, byte_str: Union[bytes, bytearray]) -> None:
        self.detector.feed(bytearray(byte_str))

    def reset(self) -> None:
        self.detector.reset()

    @property
    def done(self) -> bool:
        return self.detector.done

    def close(self) -> _chardet_nametuple:
        """字符集编码结果

        :return: tuple -> (encoding: str, language: str, confidence: float)
        """
        ret = self.detector.close()
        return _chardet_nametuple(
            encoding=ret.get("encoding"),
            language=ret.get("language"),
            confidence=ret.get("confidence")
        )

    def __enter__(self):
        self.reset()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset()


def chardet(
    byte_str: Union[bytes, bytearray],
    should_rename_legacy: bool = False
) -> _chardet_nametuple:
    """字符编码判断

    :param byte_str: bytes数据
    :param should_rename_legacy: should_rename_legacy
    :return: tuple -> (encoding: str, language: str, confidence: float)
    """
    return Chardet.chardet(byte_str, should_rename_legacy)


def download_progress(
    *,
    transient: bool = False,
    console: object = None,
    text_column: Optional[str] = '[progress.description]{task.description}',
    task_progress_column: Optional[str] = '[progress.percentage]{task.percentage:>6.2f}%',
    show_transfer_speed: bool = True
):
    """rich.progress.Progress - 下载进度条

    :param transient: 转瞬即逝
    :param console: rich.console.Console
    :param text_column: text column 文本格式 [progress.description]{task.description}
    :param task_progress_column: 任务进度格式 [progress.percentage]{task.percentage:>6.2f}%
    :param show_transfer_speed: 显示任务下载速度
    :return: rich.progress.Progress default: True
    """
    from rich import progress as _progress
    columns = [
        _progress.TextColumn(text_column),
        _progress.TaskProgressColumn(task_progress_column),
        _progress.BarColumn(),
        _progress.DownloadColumn(),
        _progress.TransferSpeedColumn(),
        _progress.TimeElapsedColumn()
    ]
    # 不显示下载速度
    if not show_transfer_speed:
        columns.pop(-2)
    return _progress.Progress(*columns, transient=transient, console=console)


def tasks_progress(
    *,
    transient: bool = False,
    console: object = None,
    text_column: Optional[str] = '[progress.description]{task.description}',
    task_progress_column: Optional[str] = '[progress.percentage]{task.percentage:>6.2f}%',
    task_progress_column_2: Optional[str] = '[cyan]{task.completed}/{task.total}[/]',
    show_transfer_speed: bool = False
):
    """rich.progress.Progress - 任务进度条

    :param transient: 转瞬即逝
    :param console: rich.console.Console
    :param text_column: text column 文本格式 [progress.description]{task.description}
    :param task_progress_column: 任务进度格式 [progress.percentage]{task.percentage:>6.2f}%
    :param task_progress_column_2: 任务进度格式 [cyan]{task.completed}/{task.total}[/]
    :param show_transfer_speed: 显示任务下载速度 default: False
    :return:
    """
    from rich import progress as _progress
    columns = [
        _progress.TextColumn(text_column),
        _progress.TaskProgressColumn(task_progress_column),
        _progress.BarColumn(),
        _progress.TaskProgressColumn(task_progress_column_2),
        _progress.TimeElapsedColumn(),
    ]
    # 显示下载速度
    if show_transfer_speed:
        columns.insert(-1, _progress.TransferSpeedColumn())
    return _progress.Progress(*columns, transient=transient, console=console)


def read_file_by_generator(file: str, mode: str = 'r', *, chunk_size: int = 1024, **kwargs):
    """基于生成器的文件读取

    :param file: file path
    :param mode: file open mode
    :param chunk_size: chunk size
    :param kwargs: open arguments
    """
    with open(file, mode, **kwargs) as read_file_obj:
        while True:
            chunk = read_file_obj.read(chunk_size)
            if not chunk:
                return
            yield chunk
