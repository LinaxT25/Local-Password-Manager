import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id


class Encryption:

    def __init__(self, master_key: str, salt: bytes = None) -> None:
        self.salt = os.urandom(16) if salt is None else salt
        kdf = Argon2id(
            salt=self.salt,
            length=32,
            iterations=3,
            lanes=4,
            memory_cost=64 * 1024,
            ad=None,
            secret=None,
        )
        key = kdf.derive(master_key.encode())
        encoded_key = base64.urlsafe_b64encode(key)
        self.fernet_key = Fernet(encoded_key)

    def encrypt(self, value: str) -> str:
        return self.fernet_key.encrypt(value.encode()).decode("utf-8")

    def decrypt(self, value: str) -> str:
        return self.fernet_key.decrypt(value.encode()).decode("utf-8")
