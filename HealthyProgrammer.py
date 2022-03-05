from pynotifier import Notification
from datetime import datetime
from time import time, sleep
from random import choice
import pyttsx3
import glob
import sys
import os


# Exercise 7 - Healthy Programmer
# Objectives : 9AM - 5PM
#   Water (3.5 LTR) = water.mp3 - loops at every 34 min for 14 glass - input: Drank - stop mp3 - repeat
#   Eyes (Relief) = eyes.mp3 - loops at every 30 min - input: EyDone - stop mp3 - repeat
#   Physical Exercise (Free hands) = exercise.mp3 - loops at every 45 min - input: ExDone - stop mp3 - repeat
# Note: mp3 play through PyGame module, to be handle time clash


# ----------------------------- Static variables

# Regarding User
request = ["Please", "Kindly", "Excuse me", "Pardon me", "Sorry for disturbing you to", "I'm requesting you to",
           "You're requested to", "You're advised to"]
request_to = ["Hold on", "Take a break", "Have a break", "Have a leave", "Take a leave", "Take a rest", "Have a rest"]
greet = ["Thanks", "Great", "Thank you", "Excellent", "Brilliant", "Good", "Awesome", "Very good", "Done", "Fine"]

# Regarding date and time
cur_y = datetime.now().year
cur_m = datetime.now().month
cur_d = datetime.now().day
cur_H = datetime.now().hour
cur_M = datetime.now().minute
cur_S = datetime.now().second

time_shift = 9 if 9 < cur_H > 17 else 17
hour_start = 9
hour_end = 17

# Regarding water and glass
water_freq = 34 * 60  # (seconds)
water_total = 3500  # (milliliters)
water_drank = 0
water_remain = 3500
water_icon = "./icons/water.ico"

glass_total = 14  # (glasses)
glass_drank = 0
glass_remain = 14

# Regarding eye exercise
eye_freq = 30 * 60  # (minutes)
eye_done = 0  # (times)
eye_icon = "./icons/eye.ico"

# Regarding physical exercise
phe_freq = 45 * 60  # (minutes)
phe_done = 0  # (times)
phe_icon = "./icons/exercise.ico"


# ----------------------------- Functions

# 1. Windows push notifier
def notify(action):
    if action == "water":
        ttl = "Drink Water"
        dsc = "According to a number of studies, an adult human should drink 4 to 4.5 liters of water a day for the " \
              "optimum cellular functioning and keeping the body hydrated all the time."
        ico = water_icon
    elif action == "Drank":
        ttl = "Water Drank"
        dsc = "Thank you for drinking water. We saved it to keep a record of your health"
        ico = water_icon
    elif action == "eye":
        ttl = "Relax Eyes"
        dsc = "Continuous exposure to blue light that comes from computer's/mobile's screen effects human eyes and " \
              "strength of eyesight may reduce overtime. Take your eyes to things other than display to get rid off."
        ico = eye_icon
    elif action == "EyDone":
        ttl = "Eye Relaxed"
        dsc = "Thank you for relaxing your eyes. We saved it to keep a record of your health"
        ico = eye_icon
    elif action == "exercise":
        ttl = "Physical Exercise"
        dsc = "Programmers usually seat on a chair throughout the day in front of a computer. Some free hand physical" \
              " exercises must help them to stay healthier over the day long while programming."
        ico = phe_icon
    else:
        ttl = "Exercise Done"
        dsc = "Thank you! You have done some physical exercises. We saved it to keep a record of your health"
        ico = phe_icon

    Notification(
        title='REMINDER - ' + ttl.upper(),
        description=dsc,
        icon_path=ico,  # On Windows .ico is required, on Linux - .png
        duration=5,  # Duration in seconds
        urgency='normal'
    ).send()


# 2. Voice alert
def read(action):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(action)
    engine.runAndWait()
    engine.stop()


# 3. Logger
def log():
    with open(log_file, "a") as file:
        file.write(
            "- {} | At {}, you {}.\n".format(datetime.now().strftime("%Y.%m.%d"), datetime.now().strftime("%H:%M:%S"),
                                             write))


# 4. Reminder and audio player
def execute(action, switch):
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "True"  # (used for not showing PyGame auto support prompt)
    from pygame import mixer

    mixer.init()
    mixer.music.set_volume(0.7)
    mixer.music.load("./audios/" + action + ".mp3")
    mixer.music.play(-1)

    notify(action)
    print(statement_before)
    read(announce_before)
    while True:
        response = input("Did you? ")
        if response.strip().lower() == switch.lower():
            mixer.music.stop()
            log()
            notify(switch)
            print(statement_after)
            read(announce_after)
            break
        else:
            print("Please enter the correct keyword, i.e., {}.".format(switch))
            continue


# ----------------------------- Main Program

# Welcome tile
title = "Exercise 7 - Healthy Programmer"
subtitle = "[Note: Takes care of health for the programmers]"
underline = int(len(subtitle)) * "-"
print("\n{}\n{}\n{}\n".format(title, underline, subtitle))

# Checking for existing user and user file, or creating new
if glob.glob("HealthyProgrammer*.log"):
    user = str(glob.glob("HealthyProgrammer*.log")).strip("['']").split(".")[0][25:]
    log_file = "HealthyProgrammer_Record_{}.log".format(user)
    print("WELCOME BACK, {}!\n".format(user))
else:
    print("HELLO! Welcome here to make you healthier while you busy in programming.")
    user = input("In which name I can call you for? Let me know your nick name: ")
    if len(user.strip()) != 0:
        print("OK! We call you in the name of {} later on.\n".format(user))
    else:
        print("We're taking the default name.\n")
        user = "Alias"
    with open("./HealthyProgrammer_Record_{}.log".format(user), "w"):
        pass
    log_file = "HealthyProgrammer_Record_{}.log".format(user)

# Program runs in due time
while True:
    if hour_start <= datetime.now().hour <= hour_end:
        print("The program is started.\n")
        break
    else:
        start_in = datetime(cur_y, cur_m, cur_d, hour_start) - datetime.now()
        start_in = str(start_in).split(".")[0].split(":") if str(start_in)[0:2] != "-1" else \
            str(start_in).split(", ")[1].split(".")[0].split(":")
        sys.stdout.write("\rThe program will start in {} hours {} minutes {} seconds.".format(start_in[0], start_in[1],
                                                                                              start_in[2])),
        sys.stdout.flush()
        sleep(1)
        continue

# Setting the timer for water, eye and exercise
time_water = time()
time_eye = time()
time_phe = time()

# Warning
print("WARNING! DON'T CLOSE THIS WINDOW.\nMinimize it and keep working...\n"
      "We'll remind you to drink water, relax eyes and physical exercise in time.\n")

# Program termination and record review
while True:
    if datetime.now().hour < hour_end:
        # sys.stdout.write(f"{str(time() - time_water).split('.')[0]} time to drink water"),  # for debugging...
        # sys.stdout.flush()

        if time() - time_water >= water_freq:
            water_drank += 250
            water_remain -= 250
            glass_remain -= 1

            statement_before = f"Drink 250ml glass of water and type 'Drank' to save record and reset the reminder."
            statement_after = f"{choice(greet)} {user}, you drank {water_drank} ml (or, {water_drank / 1000} L) of water." \
                              f"\nMoreover, you have to drink about {glass_remain} glass(es) of {water_remain} ml water more today."
            announce_before = f"{choice(request)} {choice(request_to)} {user}. It's time to have a drink a 250 ml glass of" \
                              f" water. keep hydrating, keep working."
            announce_after = f"{choice(greet)} {user}, you fuel up your body. Restart your journey with even a bit more " \
                             f"speed and we'll take a snapshot of it."
            write = "drank a 250 ml glass of water"

            execute("water", "Drank")
            time_water = time()

        if time() - time_eye >= eye_freq:
            eye_done += 1

            statement_before = f"Relax your eyes and type 'EyDone' to save record and reset the reminder."
            statement_after = f"{choice(greet)} {user}, {eye_done} time(s) you let your eyes a break for relaxing."
            announce_before = f"{choice(request)} {choice(request_to)} for a few seconds {user}. Relax your eyes. " \
                              f"Place your inner fingers gently on your eyes for a while, and see away from computer screen"
            announce_after = f"{choice(greet)} {user}, your eyes are refreshed. Do this when we remind you. We saved it for now."
            write = "relaxed your eyes"

            execute("eye", "EyDone")
            time_eye = time()

        if time() - time_phe >= phe_freq:
            phe_done += 1

            statement_before = f"Do some physical activities and type 'ExDone' to save record and reset the reminder."
            statement_after = f"{choice(greet)} {user}, you exercised {phe_done} time(s) till now for the day."
            announce_before = f"{choice(request)} {choice(request_to)} for some minutes {user}. And now you have to do " \
                              f"some physical activities like free hands, push ups, or dons. Stay energetic all the time."
            announce_after = f"{choice(greet)} {user}, you're charged up. Resume your work with a new vigour and we recorded it for review."
            write = "done some physical activities"

            execute("exercise", "ExDone")
            time_phe = time()

        sleep(1)
        continue
    else:
        print(f"{user}, your working hour has ended.")
        os.system("notepad.exe {}".format(log_file)) if input(
            "Wanna review your saved records? [Type, 1 for Yes]: ") == "1" else None
        print(f"OK, Come again tomorrow for continuation of these healthier habits.\nGood Night, {user}!")
        break
