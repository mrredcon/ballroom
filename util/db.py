import atexit
import sqlite3

#conn = sqlite3.connect('ballroom.db')

def unicode_nocase_collation(a: str, b: str):
    if a.casefold() == b.casefold():
        return 0
    if a.casefold() < b.casefold():
        return -1
    return 1

conn = sqlite3.connect(':memory:')
conn.create_collation("UNICODE_NOCASE", unicode_nocase_collation)

def app_exit():
    conn.commit()
    conn.close()

atexit.register(app_exit)
