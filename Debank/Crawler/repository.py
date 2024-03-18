import sqlite3
from datetime import datetime


class Repository:
    def __init__(self, db_path: str):
        self.connection = self.create_connection(db_path=db_path)

    def create_connection(self, db_path):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_path)
        except Exception as e:
            print(e)

        return conn

    def write_status(self, profile_id, status):
        format = '%Y-%m-%d %H:%M:%S'
        new_row = (profile_id, status, datetime.now().strftime(format))
        sql = ''' INSERT INTO profile(status,profile_id,create_at)
                      VALUES(?,?,?) '''

        cur = self.connection.cursor()
        cur.execute(sql, new_row)
        self.connection.commit()
        return cur.lastrowid


if __name__ == '__main__':
    repo = Repository(db_path='db')
    with repo.connection:
        repo.write_status(profile_id="100", status=1)
