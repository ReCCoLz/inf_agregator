import sqlite3

conn = sqlite3.connect('sqlite_python.db')
cur = conn.cursor()

def add_user_to_db(id_user):
    cur.execute('INSERT INTO users VALUES (?);', (id_user, ))
    conn.commit()

def get_user_id():
    return list(map(lambda x: x[0], cur.execute('SELECT user_id FROM users').fetchall()))
