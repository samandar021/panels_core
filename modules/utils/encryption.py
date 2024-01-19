import base64
from abc import ABC, abstractmethod
from typing import Optional, Tuple

import Crypto.Hash.SHA256 as SHA256
import Crypto.Hash.SHA512 as SHA512
from Crypto.Cipher import AES
from Crypto.Hash.HMAC import HMAC as HMAC_HASH
from Crypto.Protocol.KDF import HKDF

from modules.config_manager.config_manager import get_configs


class EncryptionBase(ABC):
    """Абстрактный класс для шифрования и дешифрования данных."""

    def __init__(self):
        # Загрузка конфигураций
        config = get_configs()
        self.key_size = config['common']['encryption']['key_size']
        self.block_size = config['common']['encryption']['block_size']
        self.master_key = config['common']['encryption']['master_key'].encode()
        self.salt_size = config['common']['encryption']['salt_size']

    @abstractmethod
    def execute(self, data, salt: Optional[bytes] = None) -> bytes | str:
        pass

    def pad(self, s: str) -> str:
        if len(s) % 16 != 0:
            return s.ljust(len(s) + (self.block_size - (len(s) % self.block_size)))
        return s

    def encrypt(self, plain_text: str, key: bytes) -> Tuple[bytes, bytes]:
        """Шифрует и возвращает пару (IV, зашифрованный текст)."""

        cipher = AES.new(key, AES.MODE_CBC)
        return cipher.iv, cipher.encrypt(plain_text.encode("UTF-8"))

    def decrypt(self, enc_text: bytes, iv: bytes, key: bytes) -> str:
        """Дешифрует и возвращает расшифрованный текст."""

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        return cipher.decrypt(enc_text).decode()


class Encryption(EncryptionBase):
    def execute(self, plain_text: str, salt: Optional[bytes] = None) -> bytes:
        """Выполняет процедуру шифрования"""

        if self.master_key is None:
            raise TypeError('self.master_key is None')
        if salt is None:
            salt = b''
        key = HKDF(self.master_key, key_len=self.key_size, salt=salt, hashmod=SHA256)

        if isinstance(key, tuple):
            raise TypeError('key is tuple')
        iv, enc_text = self.encrypt(self.pad(plain_text), key)
        enc_data = iv + enc_text
        hash_auth_key = self.create_hash_auth_key(key)
        result_digest = HMAC_HASH(digestmod=SHA512, key=hash_auth_key, msg=enc_data).digest()
        complete_encrypted_data = salt + result_digest + enc_data
        return base64.b64encode(complete_encrypted_data)

    def create_hash_auth_key(self, key: bytes | bytearray | memoryview):
        return HKDF(key, key_len=self.key_size, hashmod=SHA256, salt=b'')


class Decryption(EncryptionBase):
    def execute(self, complete_encrypted_data: bytes, salt: Optional[bytes] = None) -> str:
        """Выполняет процедуру дешифрования"""

        data, iv, salt = self.split_encrypted_info(complete_encrypted_data)
        key = HKDF(self.master_key, key_len=self.key_size, salt=salt, hashmod=SHA256)

        if isinstance(key, tuple):
            raise TypeError('key is tuple')
        decrypted_text = self.decrypt(data, iv, key)
        return decrypted_text.rstrip() if decrypted_text.endswith(" ") else decrypted_text

    def split_encrypted_info(self, encrypted_info: bytes) -> Tuple[bytes, bytes, bytes]:
        """Разделяет зашифрованную информацию на составляющие: data, iv и salt."""

        decoded_raw_data = base64.b64decode(encrypted_info)
        all_encoded_info = decoded_raw_data[64 + self.key_size:]
        data = all_encoded_info[self.block_size:]
        iv = all_encoded_info[:self.block_size]
        salt = decoded_raw_data[:self.key_size]
        return data, iv, salt
