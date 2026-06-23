from pathlib import Path
import sqlite3
from .models import PasswordEntry

class Database:

    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        self.db_path = self.data_dir / "vault.db"

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            site TEXT NOT NULL,
                            login TEXT NOT NULL,
                            password TEXT NOT NULL, 
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                            """)
        self.connection.commit()

    def add_password(self, entry: PasswordEntry):
        self.cursor.execute(
            """
            INSERT INTO passwords (site, login, password)
            VALUES (?, ?, ?)
            """,
            (entry.site, entry.login, entry.password)
        )
        self.connection.commit()

    def get_all_passwords(self):
        self.cursor.execute("""
            SELECT id, site, login, password FROM passwords
        """)
        rows = self.cursor.fetchall()


        return[
            PasswordEntry(
                site = row[1],
                login = row[2],
                password = row[3] 
            )
            for row in rows
        ]
    
    def delete_password(self, password_id: int):
        self.cursor.execute(
            """
            DELETE FROM passwords WHERE id = ?
            """,
            (password_id,)
        )

        self.connection.commit()