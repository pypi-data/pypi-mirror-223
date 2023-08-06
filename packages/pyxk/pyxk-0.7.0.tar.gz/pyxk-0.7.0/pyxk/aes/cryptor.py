from typing import Union
from collections import namedtuple

from Crypto.Cipher import AES


__all__ = ['Crypto', 'encrypt', 'decrypt', 'MODES']


class Crypto:
    """AES加解密

    from pyxk.aes.cryptor import Crypto, MODES

    cipher = Crypto(
        key=b'1234567890123456',
        mode=MODES.CBC,
        iv=b'1234567890123456'
    )
    raw_text = 'Hello World'
    ciphertext = cipher.encrypt(raw_text)
    plaintext = cipher.decrypt(ciphertext)

    print('raw text:', raw_text)
    print('ciphertext:', ciphertext)
    print('plaintext:', plaintext)

    >>>
    raw text: Hello World
    ciphertext: b'\xf7\x16\x85)|,\x91\x8c\xdbd\xaef\xc3Wbu'
    plaintext: b'Hello World'
    """
    MODES = frozenset(
        (
            ('ECB', 1), ('CBC', 2), ('CFB', 3),
            ('OFB', 5), ('CTR', 6), ('OPENPGP', 7),
            ('EAX', 9), ('CCM', 8), ('SIV', 10),
            ('GCM', 11), ('OCB', 12)
        )
    )

    def __init__(
        self,
        key: Union[str, bytes],
        mode: Union[str, int] = 'CBC',
        encoding: str = 'utf-8',
        **kwargs
    ):
        """Crypto Init

        :param key: 加密/解密 密钥
        :param mode: 加密/解密 模式
        :param encoding: encoding
        :param kwargs: kwargs
        """
        self._encoding = encoding
        self._key = self._init_key(key)
        self._mode = self._init_mode(mode)
        self._cipher_attrs = kwargs

        self._cipher = None
        self._padding = b'\x00'

    def encrypt(self, plaintext: Union[str, bytes], new_cipher=True) -> bytes:
        """加密

        :param plaintext: 加密明文
        :param new_cipher: 是否重新创建cipher
        :return: bytes
        """
        # Invalid plaintext
        if not isinstance(plaintext, (str, bytes)):
            raise TypeError(f'plaintext must be a str or bytes, got {type(plaintext).__name__!r}')

        if isinstance(plaintext, str):
            plaintext = plaintext.encode(self._encoding)

        # 填充字符
        remainder = len(plaintext) % AES.block_size or AES.block_size
        plaintext += self._padding * (AES.block_size - remainder)

        # 加密
        cipher = self.new_cipher if new_cipher else self.cipher
        ciphertext = cipher.encrypt(plaintext)

        return ciphertext

    def decrypt(self, ciphertext: bytes, new_cipher=True) -> bytes:
        """解密

        :param ciphertext: 解密密文
        :param new_cipher: 是否重新创建cipher
        :return: bytes
        """
        # Invalid ciphertext
        if not isinstance(ciphertext, bytes):
            raise TypeError(f'ciphertext must be a bytes, got {type(ciphertext).__name__!r}')

        # 解密
        cipher = self.new_cipher if new_cipher else self.cipher
        plaintext = cipher.decrypt(ciphertext)

        return plaintext.rstrip(self._padding)

    def _init_key(self, key) -> bytes:
        """cipher key initialization"""
        # Invalid key
        if not isinstance(key, (str, bytes)):
            raise TypeError(f'key must be str or bytes, got {type(key).__name__!r}')

        if isinstance(key, str):
            key = key.encode(self._encoding)

        if len(key) not in AES.key_size:
            raise ValueError(f'Invalid key length {len(key)}, must length be {AES.key_size}')
        return key

    def _init_mode(self, mode) -> int:
        """cipher mode initialization"""
        return self._get_mode_value(mode)

    def _get_mode_value(self, _mode: Union[str, int]) -> int:
        """获取mode对应的int值

        :param _mode: mode
        :return: int
        """
        # Invalid mode
        if not isinstance(_mode, (int, str)):
            raise TypeError(f'mode must be a str or int, got {type(_mode).__name__!r}')

        # mode type str
        if isinstance(_mode, str):
            _mode = _mode.upper()
            if _mode not in self.all_modes:
                raise ValueError(f'Invalid mode {_mode!r}, effective modes: {", ".join(self.all_modes.keys())}')
            return self.all_modes[_mode]

        # mode type int
        if _mode not in self.all_modes.values():
            raise ValueError(
                f'Invalid mode {_mode!r}, effective modes: '
                f'{", ".join([str(i) for i in sorted(self.all_modes.values())])}'
            )
        return _mode

    def create_cipher(self):
        """创建 AES.cipher"""
        return AES.new(key=self.key, mode=self.mode, **self.attrs)

    @property
    def all_modes(self) -> dict:
        """all modes"""
        return dict(self.__class__.MODES)

    @property
    def cipher(self):
        """AES Crypto Cipher"""
        if not self._cipher:
            self._cipher = self.create_cipher()
        return self._cipher

    @property
    def new_cipher(self):
        """每次调用新建 AES Crypto Cipher"""
        self._cipher = self.create_cipher()
        return self._cipher

    @property
    def key(self):
        """AES Crypto key"""
        return self._key

    @property
    def mode(self):
        """AES Crypto mode"""
        return self._mode

    @property
    def attrs(self):
        """AES Crypto Cipher attributes"""
        return self._cipher_attrs

    @attrs.setter
    def attrs(self, value):
        self._cipher_attrs.update(dict(value))


def encrypt(
    key: Union[str, bytes],
    plaintext: Union[str, bytes],
    mode: Union[str, int] = 'CBC',
    **kwargs
) -> bytes:
    """加密

    :param key: 加密密钥
    :param plaintext: 加密明文
    :param mode: 加密模式
    :param kwargs: kwargs
    :return: bytes
    """
    cipher = Crypto(key=key, mode=mode, **kwargs)
    return cipher.encrypt(plaintext, new_cipher=True)


def decrypt(
    key: Union[str, bytes],
    ciphertext: bytes,
    mode: Union[str, int] = 'CBC',
    **kwargs
) -> bytes:
    """解密

    :param key: 解密密钥
    :param ciphertext: 解密密文
    :param mode: 解密模式
    :param kwargs: kwargs
    :return: bytes
    """
    cipher = Crypto(key=key, mode=mode, **kwargs)
    return cipher.decrypt(ciphertext, new_cipher=True)


_tuple = namedtuple('AESModeNameTuple', 'ECB,CBC,CFB,OFB,CTR,OPENPGP,EAX,CCM,SIV,GCM,OCB')


MODES = _tuple(
    ECB=1, CBC=2, CFB=3, OFB=5, CTR=6,
    OPENPGP=7, EAX=9, CCM=8, SIV=10,GCM=11, OCB=12
)
