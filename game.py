import time
from os import listdir
from os.path import isfile
from random import randint
import threading
import audio
import rf

red_score = 0
red_team_size = 0
blue_score = 0
blue_team_size = 0

round_duration = 60 # seconds
song_filepaths = []
currentSongIndex = -1 # index of current song playing.
currentRound = {}
correct_answers_this_round = 0
previously_played_songs = []

# Initialize  the game.
def init():
	print "init game"
	global red_score
	global red_team_size
	global blue_score
	global blue_team_size
	global song_filepaths
	global currentSongIndex
	global previously_played_songs
	red_score = 0
	red_team_size = 0
	blue_score = 0
	blue_team_size = 0
	currentSongIndex = -1
	previously_played_songs = [-1]
	# Read in full list of files.
	song_filepaths = [ f for f in listdir("music/") ]
	print "done init"

#TODO: currently not called anywhere
def celebrate():
	global red_score
	global blue_score

	red_score = 0
	blue_score = 0
	# turn on spotlight
	rf.on(3)
	# sleep time in seconds
	time.sleep(60)
	#turn off spotlight
	rf.off(3)


def joinTeam(team):
	global red_team_size
	global blue_team_size
	print "join team" + team
	if team == "red":
		red_team_size += 1
	else:
		blue_team_size += 1
	if red_team_size > 0 and blue_team_size > 0 and currentSongIndex == -1:
		prepareRound()


def prepareRound():
	num_of_wrong_songs = 5
	# just call celebrate to test.
	# Choose a song from the list.
	# Choose some wrong answers.
	# Choose a start time.
	global red_score
	global red_team_size
	global blue_score
	global blue_team_size
	global currentSongIndex
	global song_filepaths
	global round_duration
	global currentRound
	global previously_played_songs

	# reset previously_played_songs if all are played
	if (len(previously_played_songs) == len(song_filepaths)):
		previously_played_songs = [currentSongIndex]

	# find a previously unplayed song
	while (currentSongIndex in previously_played_songs):
		currentSongIndex = randint(0, len(song_filepaths) - 1)
		print previously_played_songs
	previously_played_songs.append(currentSongIndex)

	currentRound = {}
	currentRound["startTime"] = (time.time() * 1000) + (1000 * round_duration)
	currentRound["correctAnswer"] = song_filepaths[currentSongIndex]
	currentRound["duration"] = 1000 * round_duration
	currentRound["wrongAnswers"] = []
	currentRound["redScore"] = red_score
	currentRound["blueScore"] = blue_score

	# populating wrong answers
	while (len(currentRound["wrongAnswers"]) < num_of_wrong_songs):
		index = randint(0, len(song_filepaths) - 1)
		if index != currentSongIndex and song_filepaths[index] not in currentRound["wrongAnswers"]:
			currentRound["wrongAnswers"].append(song_filepaths[index])


	# start round in 'duration' from now.
	print "prepare rpound"
	threading.Timer(round_duration, startRound).start()
	return currentRound

def getRound():
	global currentRound
	global red_score
	global blue_score
	currentRound["redScore"] = red_score
	currentRound["blueScore"] = blue_score
	return currentRound

def getScore():
	global red_score
	global blue_score
	response = {}
	response["redScore"] = red_score
	response["blueScore"] = blue_score
	return response

def startRound():
	global currentSongIndex
	global currentRound
	global song_filepaths
	global previously_played_songs
	global correct_answers_this_round
	correct_answers_this_round = 0
	print "todo uncomment play music."

	print "drs"+str(len(previously_played_songs)+1%6)
	if (((len(previously_played_songs)+1) % 6) == 0):
		print "celebrate!!"
		celebrate()

	audio.playSong(song_filepaths[currentSongIndex])
	prepareRound()


def correct(team):
	global red_score
	global red_team_size
	global blue_score
	global blue_team_size
	print "correct team " + team
	global correct_answers_this_round
	correct_answers_this_round += 1
	MAX_SCORE = 8
	if team == "red":
		red_score += MAX_SCORE - correct_answers_this_round
	else:
		blue_score += MAX_SCORE - correct_answers_this_round

	# TODO do all the scoring, and then flip shot glass.
