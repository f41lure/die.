import sqlite3
from passlib.apps import custom_app_context as pwd_context

conn = sqlite3.connect("app.db", check_same_thread=False)
global gUsername
global gPassword

def authenticate(username, password):
  db = conn.cursor() 
  check = db.execute("""SELECT * FROM users WHERE username = ?""", [username]).fetchall()
  if not check:
    return "That username doesn't exist, dumbass."
  elif pwd_context.verify(password) != check[0][1]:
    return "Ha, wrong password."
  else:
    gUsername = username
    gPassword = password
    return True

def signup(username, password):
  db = conn.cursor()
  taken = db.execute("""SELECT * FROM users WHERE username = ?""", [username]).fetchall()
  if not taken:
    db.execute("""INSERT INTO users (username, hash, score) VALUES (?, ?, ?)""", [username, pwd_context.hash(password), 0])
    conn.commit()
    gUsername = username
    gPassword = password
    return True  
  else:
    return False

def addsong(name, artist):
  check = 1

print(authenticate("yes", "yes"))
