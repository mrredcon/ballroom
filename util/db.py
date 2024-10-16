import atexit
import sqlite3

#conn = sqlite3.connect('ballroom.db')
conn = sqlite3.connect(':memory:')

def app_exit():
    conn.commit()
    conn.close()

atexit.register(app_exit)
