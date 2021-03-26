import sqlite3

conn = sqlite3.connect("app.db", check_same_thread=False)

db = conn.cursor()

conn.commit()