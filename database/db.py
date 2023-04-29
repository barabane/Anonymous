import sqlite3


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('anonymous.db')
        self.cur = self.conn.cursor()

    def init(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS user(
            id INT PRIMARY KEY,
            username VARCHAR(40),
            reg_date VARCHAR(20),
        )''')
