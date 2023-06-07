import sys
from traceback import print_exception

import mariadb


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        try:
            self.conn = mariadb.connect(
                user="root",
                password="123456",
                host="172.23.0.2",
                port=3306,
                database="cloud",
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def query(self, stmt, param=None):
        try:
            if param:
                self.cursor.execute(stmt, param)
            else:
                self.cursor.execute(stmt)
            return self.cursor.fetchall()
        except Exception as e:
            print_exception(e)
            return []

    def update(self, stmt, param=None):
        try:
            if param:
                self.cursor.execute(stmt, param)
            else:
                self.cursor.execute(stmt)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print_exception(e)
            return False


db = Database()
db.connect()
