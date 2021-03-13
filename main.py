import sqlite3
import random
from passlib.apps import custom_app_context as pwd_context

conn = sqlite3.connect("app.db", check_same_thread=False)
gUsername = None
gPassword = None
running = False


def authenticate(username, password):
  global gUsername
  global gPassword
  global running
  db = conn.cursor() 
  check = db.execute("""SELECT * FROM users WHERE username = ?""", [username]).fetchall()
  if not check:
    return "That username doesn't exist, dumbass."
  elif  not pwd_context.verify(password, check[0][1]):
    running = False
    return "Ha, wrong password."
  else:
    gUsername = username
    gPassword = password
    return "Logged in."

def signup(username, password):
  global gUsername 
  global gPassword
  global running
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
  db = conn.cursor()
  check = db.execute("""SELECT * FROM songs WHERE name = ? AND artist = ?;""", [name, artist]).fetchall()
  if check:
    return False
  else:
    db.execute("""INSERT INTO songs (name, artist) VALUES (?, ?);""", [name, artist])
    conn.commit()

def fetchsong():
  db = conn.cursor()
  ceiling = db.execute("""SELECT COUNT(0) FROM songs;""").fetchall()[0][0]
  songid = random.randrange(1, ceiling)
  song = db.execute("""SELECT * FROM songs WHERE id=?""", [songid]).fetchall()

  kya = ''
  for word in song[0][1].split(' '):
    kya += word[0] + ('_' * (len(word)-1)) + ' '
  kya = kya.rstrip()

  return song, kya

def leaderboard():
  db = conn.cursor()
  tards = db.execute("""SELECT * FROM users ORDER BY score;""").fetchall()
  return tards

def bank(user, score):
  db = conn.cursor()
  db.execute("""UPDATE users SET score=score+? WHERE username=?""", [score, user])
  conn.commit()

def main():
  running = True
  while running:
    if not gUsername:
      action = input("Login (l) or sign up (s): ")
      username = input("username: ")
      password = input("password: ")
      if action == "l":
        print(authenticate(username, password))
        continue
      elif action == 's':
        print(signup(username, password))
        continue
    else:
      action = input("""(p) start playing
(a) add song
(l) leaderboard
choose: """)
      if action == 'p':
        gameloop()
      elif action == 'a':
        song = input("Song name: ")
        artist = input("Artist: ")
        addsong(song, artist)
        print("Added.")
      elif action == 'l':
        tards = leaderboard()
        for singularTard in tards:
          print("{}: {}".format(singularTard[0], singularTard[2]))
        continue

def gameloop():
  score = 0
  attempted = 0
  playing = True
  while playing:
    tries = 0
    incorrect = True
    song = fetchsong()
    details = song[0][0]
    question = song[1]
    while incorrect and tries < 2: 
      answer = input("Guess this song: {} by {}\n".format(question, details[2]))
      if answer == 'n':
        playing = False
        break
      elif answer != details[1]:
        print("Nope, try again")
        tries += 1
      else:
        incorrect = False
    score += 2/(tries+1) * (not incorrect)
    attempted += 1
  bank(gUsername, score)
   
main()