l = ["The ghost of tom joad, ejfhejf"]
l = l[0].split(',')
print(l)
song = l[0]
song = song.split(' ')
print(song)
initials = ''
for word in song:
  initials += word[0] + (len(word) - 1)*'_' + ' '
print(initials)
