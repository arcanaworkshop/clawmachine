# Dianostics Script
# George Spearing

# Script will test each function and output an error message on errors

# import settings from setup
from setup import *

MATRIX = False # default matrix as not working

def main():
    global MATRIX
    
    try:
        # initialize graphic display
        display = ScoreGraphics()
        MATRIX = True # if it made it here, the matrix is working
    except NameError:
        errMsg.append("12 D.L.18") # Module Doesn't Exist

    try:    
        # display welcome message
        display.message("Starting...")
        time.sleep(3)
    except NameError:
        errMsg.append("12 D.L.24") # Module Doesn't Exist

    track1 = playAudio(WELCOME_AUDIO,0, 1)
    track2 = playAudio(GAME_AUDIO, 0, 1)

    # play audio track
    track1.playTrack() # play once

    # display accumulated error messages (on terminal)
    for msg in errMsg:
        print(f"ERR: {msg}")
    
    # If the matrix is working, print errors to matrix
    if MATRIX:
        for msg in errMsg: 
            errorMsg = "ERR: " + msg   
            print("see display")
            display.scoreRun(0,errorMsg,False,False,False, False, True)
            time.sleep(2)

    

# Class to setup matrix display
class ScoreGraphics():
    def __init__(self, *args, **kwargs):
        options = RGBMatrixOptions()

        options.rows = LED_ROWS
        options.cols = LED_COLS
        options.brightness = LED_BRIGHTNESS
        options.gpio_slowdown = LED_SLOWDOWN

        self.matrix = RGBMatrix(options = options)

        self.font1 = graphics.Font()
        self.font2 = graphics.Font()
        self.font1.LoadFont("fonts/6x10.bdf")
        self.font2.LoadFont("fonts/5x7.bdf")
        
        # colors
        self.red = graphics.Color(255, 0, 0)
        self.green = graphics.Color(0, 255, 0)
        self.blue = graphics.Color(0, 0, 255)
        self.color1 = graphics.Color(105, 255,100)
        self.color2 = graphics.Color(78, 109, 255)

    def message(self, errorMsg):
        canvas = self.matrix
    
        # draw on canvas
        canvas.Clear()

        graphics.DrawText(canvas, self.font1, 0, 10, self.red, errorMsg)



if __name__=="__main__":
    main()