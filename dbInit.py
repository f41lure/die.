import sqlite3

conn = sqlite3.connect("app.db", check_same_thread=False)

db = conn.cursor()

db.execute("""CREATE TABLE IF NOT EXISTS users (
  username TEXT PRIMARY KEY,
  hash TEXT,
  score INTEGER)""")

db.execute("""CREATE TABLE IF NOT EXISTS songs (
  id INTEGER PRIMARY KEY,
  name TEXT,
  artist TEXT)""")

conn.commit()