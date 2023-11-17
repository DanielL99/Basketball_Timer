# Python Script to run different timers depending on the user's input
# Author: Daniel Löwen (DanielL99)

# Running on a Raspberry Pi Zero, this script waits for a button press and then starts a timer.
# The timer will be displayed on a connected HDML display window in fullscreen mode.
# Buttons:
#   - Button 1: 24 seconds
#   - Button 2: 12 seconds
#   - Button 3: Adding 1 second to the timer
#   - Button 4: Removing 1 second from the timer
#   - Button 5: Resetting the timer to 0

# Importing the necessary libraries
# import RPi.GPIO as GPIO
import threading
import time
import datetime
from tkinter import *

# GPIO-Pins für die Knöpfe definieren
COUNTDOWN_24_PIN = 17
COUNTDOWN_12_PIN = 18
PLUS_ONE_PIN = 22
MINUS_ONE_PIN = 23
RESET_PIN = 24

# Countdown-Zeiten in Sekunden
countdown_time = 0
pause = False
pause_start_time = None
countdown_thread = None

# GPIO initialisieren
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(COUNTDOWN_24_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(COUNTDOWN_12_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(PLUS_ONE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(MINUS_ONE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Tkinter-Fenster für die Anzeige erstellen
root = Tk()
# root.attributes('-fullscreen', True)
root.title("Countdown Timer")

# Label für die Countdown-Anzeige
countdown_label = Label(root, font=("Seven Segment", 100), text="")
countdown_label.pack()

# Funktion für das Aktualisieren der Anzeige
def update_display():
    if countdown_time < 0:
        seconds = 0
        milliseconds = 0
    else:
        seconds = int(countdown_time)
        milliseconds = int((countdown_time - int(countdown_time)) * 10)
    countdown_label.config(text=f"{seconds:02}:{milliseconds:01}")
    root.after(100, update_display)  # Update every 100 milliseconds

# Funktionen für die Button-Events
def start_countdown_24(channel):
    global countdown_time, stop_thread, countdown_thread
    stop_thread = True
    if countdown_thread is not None:
        countdown_thread.join()  # Wait for the existing thread to stop
    stop_thread = False
    countdown_time = 24
    update_display()
    start_countdown(None)

def start_countdown_14(channel):
    global countdown_time, stop_thread, countdown_thread
    stop_thread = True
    if countdown_thread is not None:
        countdown_thread.join()  # Wait for the existing thread to stop
    countdown_time = 14
    update_display()
    start_countdown(None)

def plus_one(channel):
    global countdown_time, stop_thread, countdown_thread
    stop_thread = True
    if countdown_thread is not None:
        countdown_thread.join()  # Wait for the existing thread to stop
    countdown_time += 1
    update_display()

def minus_one(channel):
    global countdown_time, stop_thread, countdown_thread
    stop_thread = True
    if countdown_thread is not None:
        countdown_thread.join()  # Wait for the existing thread to stop
    if countdown_time > 0:
        countdown_time -= 1
        update_display()

def reset(channel):
    global countdown_time
    countdown_time = 0
    update_display()

def run_countdown():
    global countdown_time, pause, pause_start_time, stop_thread
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=countdown_time)
    while countdown_time > 0 and not stop_thread:
        if pause:
            if pause_start_time is None:
                pause_start_time = datetime.datetime.now()
            time.sleep(.1)
            continue
        if pause_start_time is not None:
            end_time += datetime.datetime.now() - pause_start_time
            pause_start_time = None
        countdown_time = (end_time - datetime.datetime.now()).total_seconds()
        update_display()
        time.sleep(.1)  # Sleep for 100 milliseconds

def start_countdown(event):
    global pause, countdown_thread, pause_start_time
    if pause:
        pause = False
        # pause_start_time = None
        if countdown_thread is None or not countdown_thread.is_alive():
            countdown_thread = threading.Thread(target=run_countdown)
            countdown_thread.start()
    else:
        pause = True

# GPIO-Events zu den Funktionen verbinden
# GPIO.add_event_detect(COUNTDOWN_24_PIN, GPIO.FALLING, callback=start_countdown_24, bouncetime=300)
# GPIO.add_event_detect(COUNTDOWN_12_PIN, GPIO.FALLING, callback=start_countdown_12, bouncetime=300)
# GPIO.add_event_detect(PLUS_ONE_PIN, GPIO.FALLING, callback=plus_one, bouncetime=300)
# GPIO.add_event_detect(MINUS_ONE_PIN, GPIO.FALLING, callback=minus_one, bouncetime=300)
# GPIO.add_event_detect(RESET_PIN, GPIO.FALLING, callback=reset, bouncetime=300)

# Bind space key to start the countdown
root.bind('<space>', start_countdown)

# Bind keyboard events to the functions
root.bind('1', start_countdown_24)
root.bind('2', start_countdown_14)
root.bind('3', plus_one)
root.bind('4', minus_one)
root.bind('5', reset)

# Tkinter-Fenster starten
root.after(1000, update_display)
root.mainloop()

# GPIO-Cleanup beim Beenden des Programms
# GPIO.cleanup()
