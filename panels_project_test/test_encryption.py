import pytest
from Crypto.Random import get_random_bytes

from modules.utils.encryption import Decryption, Encryption


class TestEncryptionLogic:
    @classmethod
    def setup_class(cls):
        cls.encryption = Encryption()
        cls.decryption = Decryption()
        cls.original_data = "Test data for AES encryption"
        cls.invalid_data = "invalid_encrypted_data"
        cls.another_original_data = "Another test data for AES encryption"
        cls.salt = get_random_bytes(cls.encryption.salt_size)

    def test_encryption_decryption(self):
        """Тестирование процесса шифрования и дешифрования."""

        # Шифрование
        encrypted_data = self.encryption.execute(self.original_data, self.salt).decode()
        assert encrypted_data is not None
        assert encrypted_data != self.original_data

        # Дешифрование
        decrypted_data = self.decryption.execute(encrypted_data.encode()).strip()
        assert decrypted_data == self.original_data

    def test_invalid_data_decryption(self):
        """Тестирование ошибки при попытке дешифрования с недействительными данными."""

        with pytest.raises(Exception):
            self.decryption.execute(self.invalid_data)

    def test_data_integrity(self):
        """Тестирование целостности данных при шифровании и дешифровании."""

        encrypted_data = self.encryption.execute(self.another_original_data, self.salt).decode()
        altered_data = encrypted_data[:-10] + "extra_data" + encrypted_data[-10:]

        with pytest.raises(Exception):
            self.decryption.execute(altered_data.encode())
