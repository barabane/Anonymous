import sqlite3
from datetime import datetime
from loguru import logger


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('anonymous.db')
        self.cur = self.conn.cursor()

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
            f"SELECT * FROM user WHERE id={user['id']}")
        logger.info(is_exists)

        if is_exists.fetchone():
            return {'status': 'error', 'msg': 'такой пользователь уже существует!'}

        self.cur.execute(f'''INSERT INTO user(id, username, user_url, reg_date, sent_msgs, rec_msgs) VALUES(
            '{user['id']}',
            '{user['username']}',
            '{user['user_url']}',
            '{datetime.now()}',
            '{0}',
            '{0}'
        )''')
        self.conn.commit()

        return {'status': 'success', 'msg': 'пользователь успешно добавлен!'}

    def get_all_users(self) -> set:
        users = self.cur.execute('SELECT * FROM user')

        return users.fetchall()


db = DB()
