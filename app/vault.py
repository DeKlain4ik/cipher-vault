import os
from cryptography.fernet import InvalidToken

from .database import Database
from .models import PasswordEntry
from .crypto import CryptoManager


class Vault:
    VAULT_VERSION = 1
    VERIFY_TEXT = "vault_ok"

    def __init__(self, master_password: str):
        self.db = Database()
        self.master_password = master_password

        self.salt_path = "data/salt.bin"

        self.crypto = None
        self.unlocked = False

        self._ensure_initialized()

        self.salt = self._load_salt()

    # ---------------- PASSWORD API ----------------

    def add_password(self, site: str, login: str, password: str):
        self._require_unlocked()

        encrypted = self.crypto.encrypt(password)

        entry = PasswordEntry(
            site=site,
            login=login,
            password=encrypted
        )

        self.db.add_password(entry)

    def get_all_passwords(self):
        self._require_unlocked()

        entries = self.db.get_all_passwords()

        return [
            {
                "site": e.site,
                "login": e.login,
                "password": self.crypto.decrypt(e.password)
            }
            for e in entries
        ]

    def delete_password(self, password_id: int):
        self._require_unlocked()
        self.db.delete_password(password_id)

    # ---------------- INIT ----------------

    def _ensure_initialized(self):
        if self.db.get_verification() is None:
            self._create_new_vault()

    def _create_new_vault(self):
        print("Creating new vault...")

        os.makedirs("data", exist_ok=True)

        self.salt = os.urandom(16)

        with open(self.salt_path, "wb") as f:
            f.write(self.salt)

        crypto = CryptoManager(self.master_password, self.salt)

        verification = crypto.encrypt(self.VERIFY_TEXT)

        self.db.create_verification(self.VAULT_VERSION, verification)

        print("Vault created")

    def _load_salt(self):
        with open(self.salt_path, "rb") as f:
            return f.read()

    # ---------------- UNLOCK ----------------

    def unlock(self) -> bool:
        try:
            row = self.db.get_verification()

            if row is None:
                raise Exception("Vault corrupted")

            version, verification = row

            if version != self.VAULT_VERSION:
                raise Exception("Unsupported vault version")

            crypto = CryptoManager(self.master_password, self.salt)

            result = crypto.decrypt(verification)

            if result != self.VERIFY_TEXT:
                raise Exception("Invalid password")

            self.crypto = crypto
            self.unlocked = True

            print("Vault unlocked")
            return True

        except InvalidToken:
            print("Wrong password")
            return False

        except Exception as e:
            print("Error:", e)
            return False

    # ---------------- HELPERS ----------------

    def _require_unlocked(self):
        if not self.unlocked:
            raise Exception("Vault is locked")