from app.vault import Vault
import os

salt = os.urandom(16)

vault = Vault(
    master_password="1234",
    salt = salt
)

vault.add_password(
    site="Steam",
    login="test@gmail.com",
    password="123456"
)

print(vault.get_all_passwords())