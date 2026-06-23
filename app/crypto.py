import os 
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet


class CryptoManager:
    
    def __init__(self, master_password: str, salt: bytes):
        self.salt = salt
        self.key = self._derive_key(master_password)
        self.fernet = Fernet(self.key)

    def _derive_key(self, password: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=390000,
        )

        key = base64.urlsafe_b64encode(
            kdf.derive(password.encode())
        )

        return key
    
    def encrypt(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt(self, token: str) -> str:
        return self.fernet.decrypt(token.encode()).decode()