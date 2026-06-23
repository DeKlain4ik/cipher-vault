from dataclasses import dataclass



"""

тоже самое что и снизу 

class PasswordEntry:
    def __init__(self, site, login, password):
        self.site = site
        self.login = login
        self.password = password

"""

@dataclass
class PasswordEntry:
    site: str
    login: str
    password: str