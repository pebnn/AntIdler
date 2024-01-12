import os
from os import path
import yaml
import pwinput
import subprocess
import cryptocode
#import requests
from curl_cffi import requests
import time
import json
import warnings

warnings.filterwarnings("ignore")
os.system("cls")
def Info():
    print("    ___          __  ____    ____         ")
    print("   /   |  ____  / /_/  _/___/ / /__  _____")
    print("  / /| | / __ \/ __// // __  / / _ \/ ___/")
    print(" / ___ |/ / / / /__/ // /_/ / /  __/ /    ")
    print("/_/  |_/_/ /_/\__/___/\__,_/_/\___/_/     \nmade by pebnn\n")


Info()

config_path = "dependencies/config.yml"
if path.exists(config_path) == False:
    if path.exists("dependencies") == False:
        os.mkdir("dependencies")
    with open(config_path, "w") as conf: # Create config file if one does not exist
            conf.write("login_token: ''\n"
                       "security_question1: None\n"
                       "security_question2: None\n"
                       "remember_login: None\n"
                       "record_client: True\n"
                       "avoid_idle: False\n"
                       r"install_path: default"
                       )

def yaml_read(path):
    yaml_file = open(path, "r")
    return yaml_file

# Load the config file into a dictionary
yaml_config = yaml.full_load(yaml_read(config_path))
config = yaml_config

# Convert the values in the dictionary to their respective data types
login_token = str(config["login_token"])
remember_login = bool(config["remember_login"])
install_path = str(config["install_path"])
security_question1 = str(config["security_question1"])
security_question2 = str(config["security_question2"])

def update_config():
    # Open config.yml in Write
    with open(config_path, "w") as yaml_file:
        # Write the updated dictionary to the config file
        yaml.dump(yaml_config, yaml_file)

def Sleep(seconds, text):
    count = 0
    while True:
        if count == seconds:
            break
        print(str(round((seconds - count) / 60)) + text)
        time.sleep(1)
        count += 1
        # Clear previous console line
        print("\033[A                             \033[A")


if remember_login == True and len(login_token) <= 4:
    valid_response_pos = ("Y", "YES")
    valid_response_neg = ("N", "NO")
    while True:
        first_login = input("Would you like to remember your login for next time? Y/N: ")

        if first_login.upper() in valid_response_pos or first_login.upper() in valid_response_neg:
            username = input("Username: ")
            password = pwinput.pwinput("Password: ")

            if first_login.upper() in valid_response_neg:
                yaml_config["remember_login"] = False
            else:
                yaml_config["remember_login"] = True

            update_config()
            break

        else:
            print('"' + first_login + '"', "is not a valid answer!")

# Grab hardware ID
hwid = str(subprocess.check_output("wmic csproduct get uuid"), "utf-8").split("\n")[1].strip()


if remember_login == True and len(login_token) <= 4:
    # Encrypt login details for remembering login for next time.
    encrypted_login = cryptocode.encrypt(username + " " + password, hwid)

    # Update the login_token item in the dictionary
    yaml_config["login_token"] = encrypted_login
    update_config()

if remember_login == True and len(login_token) > 4:
    try:
        login_details = cryptocode.decrypt(login_token, hwid).split()
    except AttributeError:
        print("Saved login details cannot be retrieved\nPlease delete config.yml and try again.\nProgram will shutdown in 10 seconds...")
        time.sleep(10)
        quit()
    username, password = login_details[0], login_details[1]


# Define the URLs
login_url = "https://www.habbo.com/api/public/authentication/login"
authentication_url = "https://www.habbo.com/api/client/clientnative/url"
unlock_url = "https://www.habbo.com/api/safetylock/unlock"

# Define the login credentials
payload = {
    "email": username,
    "password": password,}

# The UA can be changed if you have issues with being flagged as a bot, but keep the Chrome version the same as the impersonated version in post requests
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.3"

headers = {"User-Agent": user_agent,
           "Referer": "https://www.habbo.com/",
           "Host": "www.habbo.com",
           "Accept": "application/json, text/plain, */*",
           "Accept-Encoding": "gzip, deflate, br",
           "Connection": "keep-alive"}

unlock_payload = {"answer1": security_question1,
                  "answer2": security_question2,
                  "trust": "true"}

# Open requests session
while True:
    with requests.Session() as session:

        while True:
            # Send a post request to login
            print("Attempting to login...")
            response = session.post(login_url, headers=headers, data=payload)
            #print(response.text)
            time.sleep(0.5)

            if response.status_code == 429:
                print("Login failed...\n"
                      "If you continue seeing this message after waiting for the retry, close any VPNs or Proxy connections and try again later.\n"
                      "You may also need to enter your security questions in config.yml. Make sure to enter them in the correct order.\n"
                      "If the issue persists, delete the 'login_token' value in config.yml or alternatively delete the config.yml file and try again.\n"
                      "Automatically retrying in 30 minutes...")
                Sleep(1800, " minutes remaining.")
                continue
                quit()
            elif response.status_code == 200:
                print("Login was successful!")

                if security_question1 != "None":
                    response = session.post(unlock_url, headers=headers, data=unlock_payload, impersonate="chrome110")
                    time.sleep(1)

                response = session.post(authentication_url, headers=headers, impersonate="chrome110")
                json_response = json.loads(response.text) # Convert response type to dictionary
                ticket = json_response["ticket"]
                break
            else:
                print("[" + str(response.status_code) + "]ERROR...\n" + str(response.text))
                time.sleep(60)
                continue

    if len(install_path) < 10:
        user = os.getlogin()
        install_path = f"C:\\Users\\{user}\\AppData\\Local\\Programs\\habbo-electron-launcher\\Habbo Launcher.exe"

    # Open Habbo client
    from client import Habbo_client
    Habbo_client(ticket, install_path)