import secrets

from argon2 import PasswordHasher

ph = PasswordHasher()


def generate_salt():
    return secrets.token_hex(16)  # Генерируйте соль


def hash_password(raw_password: str, salt: str):
    return ph.hash(f"{raw_password}.{salt}")
