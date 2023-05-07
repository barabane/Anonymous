import sqlite3
from datetime import datetime
from loguru import logger


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DB(metaclass=Singleton):
    def __init__(self):
        try:
            self.conn = sqlite3.connect('anonymous.db')
            self.cur = self.conn.cursor()
        except sqlite3.Error as Error:
            logger.error(f'SQL error: {Error}')

    def init(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS user(
            id INT PRIMARY KEY,
            username VARCHAR(40),
            user_url TEXT,
            reg_date VARCHAR(20),
            sent_msgs INT,
            rec_msgs INT
        )''')

    def add_user(self, user):
        is_exists = self.cur.execute(
            f"SELECT count(1) FROM user WHERE id={user['id']}")

        if is_exists.fetchone():
            return False

        self.cur.execute(f'''INSERT INTO user(id, username, user_url, reg_date, sent_msgs, rec_msgs) VALUES(
            ?,?,?,?,?,?
        )''', (user['id'], user['username'], user['user_url'], datetime.now(), 0, 0))
        self.conn.commit()

        return True

    def get_all_users(self) -> set:
        users = self.cur.execute('SELECT * FROM user')

        return users.fetchall()


db = DB()
