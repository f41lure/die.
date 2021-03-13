import sqlite3
import random
import curses
from passlib.apps import custom_app_context as pwd_context

conn = sqlite3.connect("app.db", check_same_thread=False)
gUsername = None
gPassword = None
running = False

screen = curses.initscr()

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
  global screen
  running = True
  while running:
    if not gUsername:
      screen.addstr(0, 0, "Login (l) or sign up (s): ")
      action = chr(screen.getch())
      screen.clear()
      screen.addstr(0, 0, action)
      screen.addstr(0, 0, "username: ")
      username = screen.getstr().decode(encoding='utf-8')
      screen.addstr(1, 0, "password: ")
      password = screen.getstr().decode(encoding='utf-8')
      screen.clear()
      if action == "l":
        screen.addstr(0, 0, authenticate(username, password))
        continue
      elif action == 's':
        screen.addstr(0, 0, signup(username, password))
        continue
    else:
      screen.clear()
      screen.addstr(0, 0, "(p) start playing")
      screen.addstr(1, 0, "(a) add song")
      screen.addstr(2, 0, "(l) leaderboard")
      screen.addstr(3, 0, "choose: ")
      action = chr(screen.getch())
      if action == 'p':
        gameloop()
      elif action == 'a':
        screen.clear()
        screen.addstr(0, 0, "Song name (be exact, dingus): ")
        song = screen.getstr().decode(encoding='utf-8')
        screen.addstr(1, 0, "Artist (be consistent, dingus): ")
        artist = screen.getstr().decode(encoding='utf-8')
        addsong(song, artist)
        screen.addstr(2, 0, "Added.")
      elif action == 'l':
        screen.clear()
        tards = leaderboard()
        for tardLocation, singularTard in enumerate(tards):
          yeah = "{}: {}".format(singularTard[0], singularTard[2])
          screen.addstr(tardLocation, 0, yeah)
        screen.addstr(6, 0, "Press any key to go back: ")
        screen.getch()
        continue

def gameloop():
  screen.clear()
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
      display = "Guess this song: {} by {}\n".format(question, details[2])
      screen.addstr(0, 0, ' ')
      screen.addstr(0, 0, display)
      curses.setsyx(1, 0)
      screen.clrtoeol()
      answer = screen.getstr().decode(encoding='utf-8')
      if answer == 'n':
        playing = False
        break
      elif answer != details[1]:
        screen.addstr(3, 0, "Nope, try again.")
        tries += 1
      else:
        incorrect = False
    score += 2/(tries+1) * (not incorrect)
    attempted += 1
    display = 'score: {}'.format(str(score))
    screen.clear()
    screen.addstr(2, 0, display)
    screen.addstr(1, 0, '')
  bank(gUsername, score)
   
main()