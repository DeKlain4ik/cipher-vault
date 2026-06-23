from app.vault import Vault


password = input("Enter password: ")

vault = Vault(password)

if not vault.unlock():
    print("Wrong password!")
    exit()

print("Vault unlocked!")

vault.add_password("Steam", "test@gmail.com", "1231112456")

print(vault.get_all_passwords())