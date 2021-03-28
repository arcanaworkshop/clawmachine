#!/usr/bin/env/python3


from setup import *

#TODO: Add check if USB sound card is connected
#TODO: Change beam break sensor to interrupt detect

# global variable to see if matrix is working
MATRIX = False
displayTime = time.time()
regPoints = False
bonusPoints = False

class ScoreGraphics():
    def __init__(self, *args, **kwargs):
        global MATRIX
        try:
            options = RGBMatrixOptions()
        except NameError:
            errMsg.append("12 R.L.9")
        else:
            MATRIX = True
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
    

    def scrollRun(self):
        startTime = time.time()
        try:
            offscreen_canvas = self.matrix.CreateFrameCanvas()
        except AttributeError:
            errMsg.append("12 R.L.37")
        else:
            pos = offscreen_canvas.width

            while True:
                currTime = time.time()
                offscreen_canvas.Clear()
                len = graphics.DrawText(offscreen_canvas, self.font1, pos, 10, self.color1, WELCOME_TEXT1)
                len2 = graphics.DrawText(offscreen_canvas, self.font2, pos, 30, self.color2, WELCOME_TEXT2)
                pos -=1
                if (pos + len < 0):
                    pos = offscreen_canvas.width

                time.sleep(0.05)
                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

                # check button
                if GPIO.input(BUTTON_PIN) == BUTTON_EDGE:
                    # check every 1 second
                    if (currTime - startTime) > BUTTON_TIME:
                        # leave welcome screen
                        break


    def scoreRun(self, score, tries, scoreBoard, displayScore, bonusScore, gameOver, errorScore):
        canvas = self.matrix

        # draw on canvas
        canvas.Clear()
        
        # display error messages
        if errorScore:
            canvas.Clear()
            graphics.DrawText(canvas, self.font1, 0,10, self.red, tries)

        # Main score counter
        if scoreBoard:
            canvas.Clear()
            graphics.DrawText(canvas, self.font1, 0, 10, self.blue, "Score") 
            graphics.DrawText(canvas, self.font1, 2, 20, self.green, str(score))
            graphics.DrawText(canvas, self.font1, 35, 10, self.blue, "Tries")
            graphics.DrawText(canvas, self.font1, 37, 20, self.green, str(tries)) 
        # Score Message
        if displayScore:
            graphics.DrawText(canvas, self.font1, 0, 32, self.red, "Nice!")
        # Bonus Score message
        if bonusScore:
            graphics.DrawText(canvas, self.font1, 30, 32, self.red, "BONUS!")
        # Game Over Message
        if gameOver:
            graphics.DrawText(canvas, self.font1, 5, 32, self.red, "GAME OVER")
            # display message for duration. Accept no other input
            time.sleep(OVER_TIME)
            canvas.Clear()
    
    def clearScroll(self):
        self.matrix.Clear()

    def clearDisplay(self):
        self.matrix.CreateFrameCanvas().Clear()


# welcome scrolling text and music
def welcome_start():
    # always loop menu
    while True:
        # play intro music
        track1.playTrack()
        # scroll welcome message (has loop)
        displayScore.scrollRun()
        # exited menu -- time to start game
        game_start()


# Game Play with score and tries count
def game_start():
    global score; score = 0
    global tries; tries = DEFAULT_TRIES
    global endtime
    regPoints = False
    bonusPoints = False
    
    # Stop welcome audio 
    track1.stopTrack()
    # start game music
    track2.playTrack()

    gameTime = time.time()
    displayTime = time.time()
    beamTime = time.time()

    while True:
        # current time in loop
        currenttime = time.time()

        if (regPoints or bonusPoints):
            if (currenttime - displayTime) > SCORE_TIME:
                regPoints = False
                bonusPoints = False
            
        # keep score on display
        displayScore.scoreRun(score, tries, True, regPoints, bonusPoints, False, False)

        # If ball drops into pit add points
        if GPIO.input(BEAM_PIN) == BEAM_EDGE:
            if (currenttime - displayTime) > DEBOUNCE:
                #play score music and add score
                track3.playTrack()
                score = score + DEFAULT_SCORE
                # update Score board
                regPoints = True
                displayTime = time.time()
                # displayScore.scoreRun(score, tries, True, True, False, False, False)
                # time.sleep(SCORE_TIME)
        
        # if ball go into Bonus Section add points
        if GPIO.input(BONUS_PIN) == BONUS_EDGE:
            if (currenttime - displayTime) > DEBOUNCE:
                track4.playTrack()
                score = score + BONUS_SCORE
                # update Score Board
                bonusPoints = True
                displayTime = time.time()
                # displayScore.scoreRun(score, tries, True, True, True, False, False)
                # time.sleep(SCORE_TIME)

        # # if game tries is 0 and final try time is over, then GAME OVER
        if tries<=0 and currenttime - endtime > CYCLE_TIME:
            # Stop game music
            track2.stopTrack()
            # Play end game music
            track5.playTrack()
            # display "game over message"
            displayScore.scoreRun(score, tries, True, False, False, True, False)
            # display message for duration. Accept no other input
            # go back to menu
            break

        # If start button is pressed again, add more tries
        if GPIO.input(BUTTON_PIN) == BUTTON_EDGE:
            if (currenttime - gameTime) > BUTTON_TIME:
                # go back to menu
                break

        # sleep 10mS during each test    
        time.sleep(0.01)


# Claw Button Count
def clawCount(self):
    time.sleep(DEBOUNCE)
    global tries
    global endtime
    global clawTime

    # get current time
    currTime = time.time()
    # if claw button is pressed and time from last call is > cycle time
    if (GPIO.input(CLAW_PIN) == CLAW_EDGE) and (currTime - clawTime >CYCLE_TIME):
        clawTime = time.time() # get time of claw drop
        if tries > 0:
            tries = tries-1 # reduce tries
        if tries == 0:
            endtime = time.time() # if last try, get time of last try
            # print(endtime)


if __name__=="__main__":
    print("Starting Program")

    # Load Audio Tracks
    track1 = playAudio(WELCOME_AUDIO,-1,0) # Welcome Music -1 plays in an infinite loop
    track2 = playAudio(GAME_AUDIO,-1, 0) # In-Game Music -1 plays in an infinite loop
    track3 = playAudio(SCORE_AUDIO, 0, 1) # Score Music plays once
    track4 = playAudio(BONUS_AUDIO, 0, 1) # Bonus Score Music Plays Once
    track5 = playAudio(END_AUDIO, 0,0) # End Game Music


    try:
        # setup button and beam sensor pins
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BONUS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(CLAW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(CLAW_PIN, GPIO.FALLING, callback=clawCount, bouncetime=200)
        # GPIO.add_event_detect(BEAM_PIN, GPIO.FALLING, callback=beamTrigger, bouncetime=100)
        # GPIO.add_event_detect(BONUS_PIN, GPIO.FALLING, callback=bonusTrigger, bouncetime=100)

    except NameError:
        errMsg.append("12 R.L.210")

    # initialize matrix
    displayScore = ScoreGraphics()

    # print any error messages
    # If no errors here, then script should be fine
    print(f"There are {len(errMsg)} Error Messages")
    for msg in errMsg:
        errorMsg = "ERR: " + msg
        print(errorMsg)
    # If the matrix is working, print errors to matrix
    if MATRIX:
        count = 0
        for i in range(len(errMsg)): 
            errorMsg = "ERR: " + errMsg[i]
            print("see display")
            displayScore.scoreRun(0,errorMsg,False,False,False, False, True)
            if count != 0:
                if errMsg[i] != errMsg[count-1]:
                    time.sleep(ERROR_TIME)
                    count+=1
                
                else:
                    time.sleep(1)
                    count+=1
            else:
                time.sleep(ERROR_TIME)
                count+=1
            

   
    # go to welcome menu
    print("Continuing with Program")
    welcome_start()
    

