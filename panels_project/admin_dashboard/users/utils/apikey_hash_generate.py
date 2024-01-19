import hmac
from hashlib import sha256


def hash_apikey_generate(salt: str, apikey: str) -> str:
    """Хеширование API ключа."""
    return hmac.new(salt.encode(), apikey.encode(), sha256).hexdigest()
