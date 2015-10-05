import time
import pygame
pygame.mixer.init()

# Plays a song    
def playSong(filename):
	print "play song"
	pygame.mixer.music.fadeout(1000) #fadeout current music over 1 sec.
	pygame.mixer.music.load("music/"+filename)
	pygame.mixer.music.play()
	#pygame.mixer.music.unpause()
