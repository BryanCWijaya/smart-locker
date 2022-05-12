import sqlite3
from sqlite3 import Error

from matplotlib.pyplot import connect

class FaceDB:
    def __init__(self) -> None:
        self.cursor = self.connect_db("FaceBase.db")

    def connect_db(self, db_file):
        """ create a database connection to a SQLite database """
        conn = sqlite3.connect(db_file)
        sql_create_table = """ CREATE TABLE IF NOT EXISTS People (
                                    name text NOT NULL PRIMARY KEY,
                                    password text NOT NULL); 
                        """
        c = conn.cursor()
        c.execute(sql_create_table)
        print("Table Created")
        return c

    def insert_people(self, regis_info):
        conn = sqlite3.connect("FaceBase.db")
        cur = conn.cursor()
        
        name = regis_info['name']
        locker_no = regis_info['locker_no']
        matrix = regis_info['matrix']

        query = 'INSERT INTO People (name, locker_no, matrix) VALUES(?,?,?);'
        cur.execute(query, (name, locker_no, matrix,))
        conn.commit()

    def get_members_info(self):
        conn = sqlite3.connect("FaceBase.db")
        cur = conn.cursor()
        query = "SELECT * FROM People"
        cur.execute(query)
        rows = cur.fetchall()

        result = [list(x) for x in rows]

        return result

    def get_locker_no(self, name):
        conn = sqlite3.connect("FaceBase.db")
        cur = conn.cursor()
        query = "SELECT locker_no FROM People WHERE name=?"
        cur.execute(query, (name,))
        rows = cur.fetchall()
        return rows[0][0]
    
    def get_admin_password(self, username):
        conn = sqlite3.connect("FaceBase.db")
        cur = conn.cursor()
        query = "SELECT password FROM admins WHERE username=?"
        cur.execute(query, (username,))
        rows = cur.fetchall()
        return rows[0][0]

    def update_members_info(self, update_info):
        conn = sqlite3.connect("FaceBase.db")
        cur = conn.cursor()
        query = "UPDATE People SET locker_no=? WHERE name=?"
        name = update_info['member_name']
        locker_no = update_info['locker_no']
        cur.execute(query, (locker_no, name,))
        conn.commit()

    def delete_member(self, member_name):
        conn = sqlite3.connect("FaceBase.db")
        cur = conn.cursor()
        query = "DELETE FROM People WHERE name=?"
        cur.execute(query, (member_name,))
        conn.commit()

    def get_member(self, member_name):
        conn = sqlite3.connect("FaceBase.db")
        cur = conn.cursor()
        query = "SELECT * FROM People WHERE name=?"
        cur.execute(query, (member_name,))
        rows = cur.fetchall()
        return rows