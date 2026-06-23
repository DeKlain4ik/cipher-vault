from .database import Database
from .models import PasswordEntry
from .crypto import CryptoManager

class Vault:
    def __init__(self, master_password: str, salt: bytes):
        self.db = Database()
        self.crypto = CryptoManager(master_password, salt)

    def add_password(self, site: str, login: str, password: str):

        encrypted_password = self.crypto.encrypt(password)

        entry = PasswordEntry(
            site=site,
            login=login,
            password=encrypted_password
        )
        self.db.add_password(entry)

    def get_all_passwords(self):
        
        entries = self.db.get_all_passwords()

        decrypted = []

        for e in entries:
            decrypted.append({
                "site": e.site,
                "login": e.login,
                "password": self.crypto.decrypt(e.password)
            })
    
        return decrypted
    
    def delete_password(self, password_id: int):
        self.db.delete_password(password_id)