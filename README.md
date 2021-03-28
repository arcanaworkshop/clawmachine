# README RaspebrryPi Guide

## **CONNECTING TO RASPBERRY Pi (RPi)**

### **WINDOWS**

- Use PuTTY, found at [https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html). Download and install program

- Connect Ethernet cord from laptop to RPi

- Open PuTTY, under "Session" use Host Name "raspberrypi.local"
  
- Use credentials below

- To share internet with RPi, ensure internet sharing is active. Go to wifi settings and select "Alow other network users to connect ... "

### **MAC**

- Connect Ethernet cord from laptop to RPi

- Open Terminal

- type: ssh user@raspberrypi.local, where "user" is defined below"

To share internet with RPi, ensure internet sharing is active. Go to sharing settings and select "Internet Sharing"

## **CREDENTIALS**

user: **pi**

password: **** Redacted for Privacy

If using sudo commands, the password is listed above. The password will not appear while typing. That's normal.

## **UPDATING CODE**

Once connected to the Pi, you'll be using command line instructions. Go to the source code folder and use 'git' commands to pull the latest version of code.

- cd Documents/clawMachine/src
- git pull
- To rerun program: sudo python3 run_time.py
- NOTE: To see which branch you're on, type: "git branch"

To kill the existing program (required to update and re-run the program) do the following (in the command line):

- top
- Look for "python", should be near the top of the list. Take Note of the "PID" value.
- "CTL-C" to exit the list of information
- "sudo kill PID", where PID is the value you noted
- Now you can go to the source files as indicated above update and re-run the "run_time.py" script.

## **PROGRAM SETUP INFORMATION**

The following Sections cover setup, operation, and brief troubleshooting of the scripts.

## SETUP

Audio files are located on the USB Drive. The files should be in the main directory of the USB Drive. The naming scheme is "TRACK000.wav" Where "000" is the track number. Audio files must wav format with a frequency of 44100Hz, mono, and 16 bit.

The [setup.py](/src/setup.py) script has all the imports and most of the functions. Use this file to set the Beam Break Sensor(s) input Pin, start button input pin, claw machine count pin (if those ever changes, which they shouldn't). Chages to the matrix output can be changed in the "run_time.py" script

### TRACK NUMBERS

TRACK001.wav: Welcome Music, Idle Machine

TRACK002.wav: Game Music, In-Game Music

TRACK003.wav: Score, Normal Score Point

TRACK004.wav: Score, Bonus Score Point

TRACK005.wav: End Music, Game over

## OEPRATION

When the raspberry pi is powered on the "run_time.py" script should automatically start. The boot up time is ~30 seconds. This will play a welcome audio and display a message on the matrix. Once the start button is pressed, the matrix and music will change to game mode. The user will have a predetermined number of tries as defined in [setup.py](/src/setup.py). The number of tries should match the claw machine number of tries.

## GIT COMMANDS

A few important Git commands to use when logged into the RPi:\

For getting files from the repositoy:

- "git pull" get lasest information from repo

- "git fetch origin [remotBranch]:[localBranch]" where [remoteBranch] is a new branch that you need to pull. [localBranch] will be the same name

- "git branch" lists the branches on the repository. If you tried adding a branch, make sure it shows up in this list.

- "git checkout [branch]" where [branch] is the branch you want to switch to
  
For adding files to the repository:

- "git add [files]" where [files] are local files you want to add to the repo

- "git commit -m "*message*"" where *message* is user defined

- "git push" will push the commited files to the current repo

## EDITING FILES

To edit files on the RPi, you can use "nano".

To edit file type "nano [filename]" then follow instructions

**ONE TIME USE:**

Disable Auto Mount USB on startup: I think this will fix the auto assigning mount locations. First, remove USB flash drive.

"cd /media/pi"

"rm -r [directory]" where directory is the *AUDIO#* name. Repeat command until all *AUDIO* directories are removed.

"cd /etc/xdg/pcmanfm/LXDE-pi"

"nano pcmanfm.conf"

Find and change the following lines in the file to read:

[volume]

mount_on_startup=0

mount_removable=0

autorun=0

Once that's done, "sudo reboot" or power cycle, and re-insert USB.

## TROUBLE SHOOTING

### No Display on Power Up

- Does the Rapsberry Pi have Power? Does the LED matrix have Power?
- Check the "cronlog", log into RPi and type "cd ~/logs", type "cat cronlogs" to view error messages.

### No Audio

- Check power for audio amplifier
- Check volume on audio amplifier
- Check headphone output on RPi

### Restart Program

- Go to folder: "cd ~/Documents/clawMachine/src"
- "sudo python3 run_time.py"
- Assuming any error have been correct, a reboot will also restart the program.
  
### Run Diagnostic Script

- Go to folder: "cd ~/Documents/clawMachine/src"
- "sudo python3 diagnostic.py"
- error messages will appear on screen / command line

## ERROR MESSAGES

Messages will print to the command line and the display (if available)

Message Format is: Error #, File.Line.#

Example message-> ERR: 10 S.L.8 ==> Error 10 in setup file line 8

ERR 10 - Import module error. Check setup file

ERR 12 - Name Errors. Check Import Module declarations and usage

ERR 20 - Audio File Error. Check Name and Format
