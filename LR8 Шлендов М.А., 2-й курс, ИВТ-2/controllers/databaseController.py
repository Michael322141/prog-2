import sqlite3
from typing import Iterable

from models.currency import Currency
from models.user import User
from models.user_currency import UserCurrency

from utils.currencies_api import get_currencies

class CurrencyDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Currencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num_code TEXT NOT NULL,
            char_code TEXT NOT NULL,
            name TEXT NOT NULL,
            value FLOAT,
            nominal INTEGER
        );""")
        self.conn.commit()
        
        self.insert_many(get_currencies())
        
    def insert(self, currency: Currency):
        self.cursor.execute("INSERT INTO Currencies(num_code, char_code, name, value, nominal) VALUES (?, ?, ?, ?, ?)",
                            (currency.num_code, currency.char_code, currency.name, currency.value, currency.nominal))
        self.conn.commit()
        
    def insert_many(self, currencies: Iterable[Currency]):
        self.cursor.executemany("INSERT INTO Currencies(num_code, char_code, name, value, nominal) VALUES (?, ?, ?, ?, ?)",
                            map(lambda c: (c.num_code, c.char_code, c.name, c.value, c.nominal), currencies))
        self.conn.commit()
        
    def get_all(self) -> list[Currency]:
        self.cursor.execute("SELECT * FROM Currencies")
        result = self.cursor.fetchall()
        return list(map(lambda row: Currency(row[1], row[2], row[3], row[4], row[5], id=row[0]), result))

    def get_by_id(self, id: int) -> Currency:
        self.cursor.execute("SELECT * FROM Currencies WHERE id = ?", (id,))
        row = self.cursor.fetchone()
        return Currency(row[1], row[2], row[3], row[4], row[5], id=row[0])
    
    def update_by_char_code(self, char_code: str, value: float):
        self.cursor.execute("UPDATE Currencies SET value = ? WHERE char_code = ?", (value, char_code))
        self.conn.commit()
        
    def delete(self, id: int):
        self.cursor.execute("DELETE FROM Currencies WHERE id = ?", (id,))
        self.conn.commit()
        
class UserDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );""")
        self.conn.commit()
        
        self.insertmany([
            User(1, "Вадим Козаков"),
            User(2, "Владимир Семенюк"),
            User(3, "Максим Попов"),
        ])
        
    def insert(self, user: User):
        self.cursor.execute("INSERT INTO Users(name) VALUES (?)", (user.name,))
        self.conn.commit()
        
    def insertmany(self, users: Iterable[User]):
        self.cursor.executemany("INSERT INTO Users(name) VALUES (?)", map(lambda u: (u.name,), users))
        self.conn.commit()
        
    def get_all(self) -> list[User]:
        self.cursor.execute("SELECT * FROM Users")
        result = self.cursor.fetchall()
        return list(map(lambda row: User(row[0], row[1]), result))
    
    def get_by_id(self, id: int) -> User | None:
        self.cursor.execute("SELECT * FROM Users WHERE id = ?", (id,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        return User(row[0], row[1])
        
    def delete(self, id: int):
        self.cursor.execute("DELETE FROM Users WHERE id = ?", (id,))
        self.conn.commit()
        
class UserCurrencyDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS UserCurrencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            currency_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES Users(id),
            FOREIGN KEY(currency_id) REFERENCES Currencies(id)
        );""")
        self.conn.commit()
        
        self.insert_many([
            UserCurrency(1, 2),
            UserCurrency(1, 5),
            UserCurrency(1, 10),
            
            UserCurrency(2, 10),
            UserCurrency(2, 23),
            UserCurrency(2, 12),
            
            UserCurrency(3, 42),
            UserCurrency(3, 34),
            UserCurrency(3, 19),
        ])
        
    def insert(self, user_currency: UserCurrency):
        self.cursor.execute("INSERT INTO UserCurrencies(user_id, currency_id) VALUES (?, ?)", (user_currency.user_id, user_currency.currency_id))
        self.conn.commit()
        
    def insert_many(self, user_currencies: Iterable[UserCurrency]):
        self.cursor.executemany("INSERT INTO UserCurrencies(user_id, currency_id) VALUES (?, ?)",
                                map(lambda uc: (uc.user_id, uc.currency_id), user_currencies))
        self.conn.commit()
        
    def get_all(self) -> list[UserCurrency]:
        self.cursor.execute("SELECT * FROM UserCurrencies")
        result = self.cursor.fetchall()
        return list(map(lambda row: UserCurrency(id=row[0], user_id=row[1], currency_id=row[2]), result))
        
    def get_by_user_id(self, user_id: int) -> list[UserCurrency]:
        self.cursor.execute("SELECT * FROM UserCurrencies WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchall()
        return list(map(lambda row: UserCurrency(id=row[0], user_id=row[1], currency_id=row[2]), result))
        
    def delete(self, id: int):
        self.cursor.execute("DELETE FROM UserCurrencies WHERE id = ?", (id,))
        self.conn.commit()