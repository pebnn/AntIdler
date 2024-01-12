import psutil
import os
import time
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from animation import Animation_create
import win32gui
import yaml
import random
import subprocess
from Actions import action_Data
import threading

# Grab config only if file is run through AntIdler.py
if __name__ != "__main__":
    def yaml_read(path):
        yaml_file = open(path, "r")
        return yaml_file

    config_path = config_path = "dependencies/config.yml"

    # Load the config file into a dictionary
    yaml_config = yaml.full_load(yaml_read(config_path))
    config = yaml_config

    # Convert the values in the dictionary to their respective data types
    screenshot = bool(config["record_client"])
    avoid_idle = bool(config["avoid_idle"])

def set_window_rect(hwnd, x, y, width, height):
    win32gui.MoveWindow(hwnd, x, y, width, height, True)

# Check if process is running then kill if it is. two process names given due to packages handling names differently
def kill_process(process_name, process_name_2):
    habbo_running = process_name_2 in (p.name() for p in psutil.process_iter())
    if habbo_running == True:
        print("Stopping " + process_name_2)
        os.system("taskkill /f /im " + process_name)

# Main function for client control
def Habbo_client(ticket="habboticket", path="Habbo Launcher path"):
    kill_process("Habbo.exe", "Habbo.exe")
    kill_process("\"Habbo Launcher.exe\"", "Habbo Launcher.exe")
    habbo_client_running = False
    while True:
        if habbo_client_running == True:
            break
        # Open Habbo Launcher using pywinauto
        app = Application(backend="uia").start(path)

        # Wait for potential updates to finish, increase number if habbo ticket is not being entered
        time.sleep(4)

        # Press TAB to select habbo token input box in launcher
        send_keys("{TAB}")

        # Copy ticket to clipboard
        subprocess.run("clip", text=True, input=ticket)

        # Paste clipboard to login
        send_keys('^v')

        time.sleep(1)
        # Press TAB twice to select Flash version, Then press enter to run Flash client.
        send_keys("{TAB}")
        send_keys("{TAB}")
        send_keys("{ENTER}")

        # Wait for Habbo.exe to start
        count = 0
        while habbo_client_running == False:
            # Retry after 60 seconds
            if count == 60:
                send_keys("{TAB}")
                send_keys("{ENTER}") # Press hotel key again in case update occurred (requires two enter key presses)
                break
            habbo_client_running = "Habbo.exe" in (p.name() for p in psutil.process_iter())
            time.sleep(1)
            count += 1
    # Kill Habbo Launcher process when Habbo.exe has started
    kill_process("\"Habbo Launcher.exe\"", "Habbo Launcher.exe")
    time.sleep(5)

    app.connect(path="Habbo.exe") # Connect pywinauto to habbo client
    main_window = app.window(title_re=".*")  # Use a regular expression to match any title
    window_title = main_window.texts() # Get the window title
    window_control = app.window(control_id=0)

    # Get habbo username (for whisper to self to avoid idle kick)
    habbo_username = str(window_title).split("|")[1].strip()[:-2]

    # Get the window handle (hwnd)
    hwnd = window_control.handle

    # Set the new size and position using set_window_rect
    set_window_rect(hwnd, 0, 0, 900, 700)

    # Click away alerts
    from Alerts import detectAlert
    detectAlert(win=app[window_title])

    # How many seconds should each idle session be set as (21600 = 6 hours)
    idle_time = 21600

    # Function for sleeping until relog, also handles screenshots through the idle period
    def Idle_func(seconds, text, screenshot=True, kill_client=False, window_title="none", screenshot_interval_sec=60):

        def client_Action(type, message="Automated chat message!", coords=(0, 0), click_button="left", delay=1):
            if type == "click":
                time.sleep(delay)
                app.MainDialog.click_input(button=click_button, coords=coords)

            if type == "chat":
                time.sleep(delay)
                # Click message box
                app.MainDialog.click_input(button="left", double=False, coords=(280, 610))

                # Copy message to clipboard
                subprocess.run("clip", text=True, input=message)

                # Paste message to chat
                send_keys('^v')

                # Press enter to send message
                send_keys("{ENTER}")

            else:
                pass


        from os import path
        count = 0
        screenshot_count = 0
        screenshot_name = 0
        screenshot_path = "dependencies/screenshots"
        # Check if screenshots folder exists. If not, Create one
        if path.exists(screenshot_path) == False:
            os.mkdir(screenshot_path)
        else:
            # Check if image files exists in path to avoid overwriting screenshots
            screenshot_files = os.listdir(screenshot_path)
            for i in screenshot_files:
                screenshot_name += 1

        # List of messages to whisper to yourself to avoid getting idle kicked from rooms (Most lines generated by ChatGPT)
        wakeup_message = ("Can't.. stay.. awake.. much.. longer...", "Good morning sunshine!",
                          "Sooo sleepy...", "How many hours left?",
                          "I ƒ AntIdler!", "Plot twist: What if I'm just a character in someone else's pixelated dream?",
                          "I wonder if my virtual plants are getting enough virtual sunlight...",
                          "If I were a pixel, where would I hide in this room? Hmm...",
                          "If only I could exchange duckets for virtual snacks right now...",
                          "Wondering if virtual plants have virtual feelings. Should I water them?",
                          "Contemplating the mysteries of the virtual universe while sitting here.",
                          "Planning an epic escape from this room...",
                          "Did I leave the stove on in my virtual kitchen?",
                          "If thoughts had sounds, this room would be a symphony of silence.",
                          "Considering a virtual vacation to a tropical pixel-free island.",
                          "If I close my eyes in the virtual world, do I dream in ones and zeros?",
                          "Virtual fortune teller predicted a great adventure today. Currently waiting...",
                          "What if my reality is just a simulation...",
                          "Zzz... How much longer until virtual sunrise?",
                          "Listening to the silence, wondering if walls share secrets.",
                          "If walls could talk, would they tell tales of my virtual musings?",
                          "Unraveling the mysteries woven into the fabric of this space.",
                          "Could someone open up a window.. please?",
                          "Why do we park in driveways and drive on parkways? Mind-boggling.",
                          "Do fish get thirsty? What if they do, and we just don't know?",
                          "If the room had a soundtrack, what song would be playing now?",
                          "Curious if the furniture judges my taste in room aesthetics.",
                          "Considering renting a room with a better view.",
                          "If I were a detective, what secrets would this room reveal?",
                          "Daydreaming about the next unexpected plot twist in the room saga.",
                          "Thinking about a caffeinated infusion for my pixelated soul.",
                          "Engaging in a staring contest with the virtual walls.",
                          "Considering a dramatic monologue to combat the sleepy vibes.",
                          "My bed is whispering sweet nothings, but I must resist.",
                          "Counting imaginary sheep but they keep turning into pixel llamas.",
                          "If boredom were a sport, I'd be the reigning champion.",
                          "Wondering if yawning has a sound effect.",
                          "A sleepy Habbo is a losing Habbo.",
                          "Mentally reciting the alphabet backward to stay sharp.",
                          "If thoughts had volume, mine would be at full blast.",
                          "Hatching a plan to turn boredom into a pixelated adventure.",
                          "Daydreaming about a virtual caffeine waterfall. Perk me up!",
                          "If I were a superhero, my power would be anti-snooze beams.",
                          "You can do it, stay wide awake!",
                          "Virtual acrobatics: flipping through random thoughts mid-air.",
                          "If playtime was a currency, I'd be a billionaire by now.",
                          "Imagining a virtual world where coffee rains and yawns are outlawed.",
                          "If sleep were a video game boss, I'd be the undefeated champion.")

        idle_count = 0
        def self_Whisper(message):
            # Click message box
            app.MainDialog.click_input(button="left", double=False, coords=(280, 610))
            time.sleep(0.2)
            whisper_message = ":whisper " + habbo_username + " " + message

            # Copy message to clipboard
            subprocess.run("clip", text=True, input=whisper_message)

            # Paste message to chat
            send_keys('^v')

            # Send message and remove whisper toggle from chat to avoid chat bubble above user
            send_keys("{ENTER}" + "{BACK}")

        try:
            # Grab data from customActions.yml
            custom_actions_data = action_Data()

            for action_name, action_details in custom_actions_data.items():
                action_type = action_details.get('type', '')
                if action_type == "click":
                    action_coords = tuple(map(int, action_details.get('coords', '0, 0').split(',')))
                    action_click_button = action_details.get('click_button', 'left')
                    action_delay = int(action_details.get('delay', 1))

                    # Set chat variables to None for click function
                    action_message = None

                elif action_type == "chat":
                    action_message = action_details.get('message', 'Automated chat message!')
                    action_delay = int(action_details.get('delay', 1))

                    # Set click variables to None for chat function
                    action_coords = None
                    action_click_button = None

                # If delay is more than idle_time, skip action. (main idling loop is set to 6 hours as default, longer action_delay could cause errors)
                if action_delay >= idle_time:
                    continue

                # Runs custom actions in threads to avoid idle time delaying main loop timer
                x = threading.Thread(target=client_Action, args=(action_type, action_message, action_coords, action_click_button, action_delay))
                x.start()

                # Print raw action details for each action being run (for testing purposes)
                #print(action_details)

        # No custom actions are set in customActions.yml
        except AttributeError:
            pass


        while True:
            if count == seconds:
                if kill_client == True:
                    kill_process("Habbo.exe", "Habbo.exe") # Kill habbo process and restart entire login process
                break
            print(str(round((seconds - count) / 60)) + text)
            time.sleep(1)
            count += 1

            # Prevent player from entering idle mode (240 seconds = 4 minutes)
            idle_count += 1
            if avoid_idle == True and idle_count > 240:
                self_Whisper(message=wakeup_message[random.randrange(0, len(wakeup_message))])
                idle_count = 0

            # Clear previous console line
            print("\033[A                             \033[A")
            if screenshot == True:
                screenshot_count += 1
                if screenshot_count == screenshot_interval_sec:  # Take screenshot at a set interval (seconds)
                    screenshot_count = 0
                    screenshot_name += 1
                    win = app[window_title]
                    # Take screenshot and save it in screenshot path with unique name
                    try:
                        win.capture_as_image().save(screenshot_path + "/screenshot" + str(screenshot_name) + ".png")
                    except:
                        print("Error: Screenshot failed!")


    # Run idle function for set amount of seconds
    Idle_func(seconds=idle_time,
              text=" minutes until relog.",
              screenshot=screenshot,
              kill_client=True,
              window_title=window_title,
              screenshot_interval_sec=30)


    time.sleep(2)
    Animation_create(fps=15)


if __name__ == "__main__":
    Habbo_client()