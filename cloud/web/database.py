import sys
from traceback import print_exc

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
                host="db",
                port=3306,
                database="cloud",
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor(dictionary=True)
        except mariadb.Error:
            print_exc()
            sys.exit(1)

    def query(self, stmt, param=None):
        try:
            if param:
                self.cursor.execute(stmt, param)
            else:
                self.cursor.execute(stmt)
            return self.cursor.fetchall()
        except Exception:
            print_exc()
            return []

    def update(self, stmt, param=None):
        try:
            if param:
                self.cursor.execute(stmt, param)
            else:
                self.cursor.execute(stmt)
        except Exception as e:
            print_exc()
            self.conn.rollback()
            return e
        return ""

    def update_many(self, stmt, param=None):
        try:
            if param:
                self.cursor.executemany(stmt, param)
            else:
                self.cursor.executemany(stmt)
            return True
        except Exception:
            print_exc()
            self.conn.rollback()
            return False


db = Database()
db.connect()
