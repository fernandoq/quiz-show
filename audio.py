import time
import subprocess
import os

print os.uname()
if not os.uname()[0].startswith("Darw"):
	import pygame
	pygame.mixer.init()

# Plays a song    
def playSong(filename):
	print "play song"
	if not os.uname()[0].startswith("Darw"):
		pygame.mixer.music.fadeout(1000) #fadeout current music over 1 sec.
		pygame.mixer.music.load("music/" + filename)
		pygame.mixer.music.play()
	else:
		subprocess.call(["afplay", "music/" + filename])