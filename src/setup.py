#!/usr/bin/env/python3

#Script is used to setup various sensors and functions

errMsg = [] # initalize empty list for error messages

try:
    #imports for all modules #DELETE ALL UNUSED MODULES
    # import os
    # import signal
    import sys
    # import threading
    import time

    # import board
    # import busio
    # import adafruit_tcs34725

    import RPi.GPIO as GPIO
    # import simpleaudio as sa
    # import simpleaudio.functionchecks as fc
    from pygame import mixer
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
    # from samplebase import SampleBase
except ModuleNotFoundError:
    errMsg.append('10 S.L.8')

# Matrix defaults
LED_ROWS = 32
LED_COLS = 64
LED_BRIGHTNESS = 80
LED_SLOWDOWN = 3
WELCOME_TEXT1 = "Recy-Claw"
WELCOME_TEXT2 = "Press Start"

# callback debounce time for buttons
DEBOUNCE = 0.06

# Amount of time for claw to complete last run
CYCLE_TIME = float(10)

# clawTime keeps track of each claw button press
clawTime = float(0)

# Break Beam Sensor Input Pin
BEAM_PIN = 25 #BCM Pin Value

# Break Beam Bonus Sensor Input Pin
BONUS_PIN = 24 #BCM Pin Value

# Start Button Input Pin
BUTTON_PIN = 19 #BCM Pin Value

# Start Button Timeout
BUTTON_TIME = float(1)

# Claw Button, Game Counter Input Pin
CLAW_PIN = 18 # BCM Pin Value

# master volume for pygame
VOLUME = 0.8

# starting score
score = 0

# Time for score message to be displayed
SCORE_TIME = 1

# Default Number of tries per gamePlay
DEFAULT_TRIES = 5
tries = DEFAULT_TRIES

# end time initilization
try:
    endtime = time.time()
except NameError:
    errMsg.append("2 S.L.78")

# Time for game over message to be displayed
OVER_TIME = 15

# Error message Time to display on Board
ERROR_TIME = 15

# Points for getting ball into funnel
DEFAULT_SCORE = 1000

# Points for scoring in bonus area
BONUS_SCORE = 500

# Audio Directory location
DIRECTORY = '/media/pi/AUDIO/'

# Audio Setup
FILETYPE = '.wav'
FREQ = 44100
SIZE = 16
AUDIO_CHANNELS = 1 # mono playback
BUFFER = 4096

# Track Declarations
WELCOME_AUDIO = '001' #play on power up
GAME_AUDIO = '002' #play during game, after start button is pressed
SCORE_AUDIO = '003' # normal score point
BONUS_AUDIO = '004' # bonus score point
END_AUDIO = '005' # End Game Music

# GPIO Setup
try:
    GPIO.setwarnings(False) # ignore warnings
    GPIO.cleanup() # Clean up dirty pins
    GPIO.setmode(GPIO.BCM) # set Pin Mode
    BEAM_EDGE = GPIO.LOW # Break Beam Triggers Low if broken
    BUTTON_EDGE = GPIO.LOW # GPIO.HIGH if Button is NC PUD_UP, GPIO.LOW if Button is NO
    BONUS_EDGE = GPIO.LOW # Break Beam Triggers Low if broken
    CLAW_EDGE = GPIO.LOW # Claw Button Input. PUD_UP, GPIO.LOW if triggered
except NameError:
    errMsg.append("12 S.L.115")


# Signal handler for graceful program exit
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

#Audio Setup
class playAudio():
    
    def __init__(self, trackNum, loop, channel):
        try:
            self.trackNum = trackNum
            self.loop = loop
            self.channel = channel
            mixer.init(channels=AUDIO_CHANNELS) 
            trackFile = DIRECTORY + 'TRACK' + self.trackNum + '.wav'
            self.soundFile = mixer.Sound(trackFile)
            mixer.Channel(self.channel)
            mixer.Channel(self.channel).set_volume(VOLUME)
        except:
            errMsg.append("20 S.L.162")
    
    def playTrack(self):
        try:
            mixer.Channel(self.channel).play(self.soundFile,loops=self.loop)
        except NameError:
            errMsg.append("12 S.L.162")
        except AttributeError:
            errMsg.append("20 S.L.162")

    def pauseTrack(self):
        try:
            mixer.Channel(self.channel).pause()
        except NameError:
            errMsg.append("12 S.L.170")

    def resumeTrack(self):
        try:
            mixer.Channel(self.channel).unpause()
        except NameError:
            errMsg.append("12 S.L.176")

    def stopTrack(self):
        try:
            mixer.Channel(self.channel).stop()
        except NameError:
            errMsg.append("12 S.L.182")

    def busy(self):
        try:
            mixer.Channel(self.channel).get_busy()  
        except NameError:
            errMsg.append("12 S.L.188")


# give message to user if main is run
if __name__=="__main__":
    print("Setup file, use 'run_time' for execution")
