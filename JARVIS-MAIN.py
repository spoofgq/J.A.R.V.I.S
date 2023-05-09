#!/usr/bin/env python3
# JARVIS-MAIN v2
import openai
import gtts
import speech_recognition as sr
import playsound
import pyaudio
import pygame 
import uuid
import argparse
import io
import time
import re
import requests
import os
import google.cloud.texttospeech as texttospeech
import random
import pygetwindow as gw
from subprocess import Popen
from pathlib import Path
from datetime import datetime
from tempfile import NamedTemporaryFile

###########
## SETTINGS - CHANGE THESE
###########
use_ui = 'true'     # leave empty if you don't want the jarvis ui
openai_key = ''     # enter your openai api key here
########### HOME ASSISTANT SETTINGS ###########
hass_name = ''  # the name of your HASS instance (anything you want)
hass_dns = ''   # (ex. https://yourhassdomain.duckdns.org:443)
hass_local = '' # the local ip address/port (ex. http://192.168.1.1:8123)
host_server = ''   # only set if you're running hass on a VM - this is your VM's host IP
hass_key = '' # your hass auth key

### HASS Devices (change to your actual device ids on your hass instance)
main_lights = 'light.mainlights'
alt_lights = 'light.altlights' 
fan = 'switch.fan'
fridge = 'switch.fridge'
security_mode = 'switch.securitymode'
## HASS Scripts (custom scripts you may want Jarvis to control)
script_1 = ''
script_2 = ''
script_3 = ''
script_4 = ''
script_5 = ''

########### DEVICE SETTINGS ###########
microphone_device = 7               #    1 = default

###########
## DO NOT TOUCH
###########
dir = os.path.dirname(os.path.realpath(__file__))
directory = dir.replace("\\", "/")
tts_dir = Path("./sound/tts/")
tts_dir = directory + "/" + str(tts_dir) + "/"
tts_dir = tts_dir.replace("\\", "/")
soundeffects_dir = Path("./sound/effects/")
soundeffects_dir = "/" + str(soundeffects_dir) + "/"
soundeffects_dir = soundeffects_dir.replace("\\", "/")



###### Check Server Status Physical
def check_ping_physical():
    hostname = host_server
    response = os.system("ping -n 1 " + hostname)

    if response == 0:
        pingstatus = "Online"
    else:
        pingstatus = "Offline"
    
    return pingstatus

###### Check Server Status Hass
def check_ping_hass(host):
    try:
        r = requests.get(host)
        if r.status_code != 200:
            hass_status = "Offline"
        else:
            hass_status = "Online"

    except requests.ConnectionError:
        hass_status = "Offline"

    return hass_status

################ OPENAI SETUP ##################
openai.api_key = openai_key
core_convo = Path('./data/char/core_convo.txt').read_text()
def generate_response(prompt):
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": core_convo},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2096,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = completions.choices[0].message["content"].strip()
    return message

###############################################################################
#grab something inbetween ``` (used for grabbing generated code from openai)
def getSubstringBetweenTwoChars(ch1,ch2,str):
    return s[s.find(ch1)+1:s.find(ch2)]

###############################################################################

################ SPEECH RECOGNIZER SPEECH 2 TEXT ################

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("J.A.R.V.I.S Listening...")
        audio = recognizer.listen(source)

    try:
        print("Analyzing speech...")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from integrated recognition service; {e}")

################### WAVENET FUNCTIONS #######################

speak_rate = 1.1


def synthesize_text(text, client):
  """Synthesizes speech from the input string of text."""

  # input format
  input_text = texttospeech.SynthesisInput(text=text)
  # Note: the voice can also be specified by name.
  # Names of voices can be retrieved with client.list_voices().
  voice = texttospeech.VoiceSelectionParams(
      name='en-GB-Wavenet-B',
      language_code='en-GB',
      ssml_gender=texttospeech.SsmlVoiceGender.MALE)

  audio_config = texttospeech.AudioConfig(
      audio_encoding=texttospeech.AudioEncoding.MP3,
      speaking_rate=speak_rate, pitch=-4)

  response = client.synthesize_speech(
      request={"input": input_text, "voice": voice, "audio_config": audio_config})

  return response.audio_content


def play_mp3(audio):
  
  # The response's audio_content is binary. Write to temp
  name = "temp.mp3"
  with open(name, 'wb') as out:
    out.write(audio)
  p = playsound.playsound(name)
  os.remove("./temp.mp3")
  print("Finished Response.")

############### GET DATE/TIME ###################

def get_time_of_day(time):
    if time < 12:
        return "Morning"
    elif time < 16:
        return "Afternoon"
    elif time < 19:
        return "Evening"
    else:
        return "Night"
    
def ui(type):
    if use_ui == "true":
        if type == "main":
            jarvisBlue.restore()
            jarvisGreen.minimize()
            jarvisPurple.minimize()
            jarvisRed.minimize()
            jarvisYellow.minimize()
            jarvisTalking.minimize()
        elif type == "green":
            jarvisGreen.restore()
            jarvisBlue.minimize()
            jarvisPurple.minimize()
            jarvisRed.minimize()
            jarvisYellow.minimize()
            jarvisTalking.minimize()
        elif type == "red":
            jarvisRed.restore()
            jarvisBlue.minimize()
            jarvisPurple.minimize()
            jarvisGreen.minimize()
            jarvisYellow.minimize() 
            jarvisTalking.minimize()
        elif type == "yellow":
            jarvisYellow.restore()
            jarvisBlue.minimize()
            jarvisPurple.minimize()
            jarvisRed.minimize()
            jarvisGreen.minimize()
            jarvisTalking.minimize()
        elif type == "purple":
            jarvisPurple.restore()
            jarvisBlue.minimize()
            jarvisGreen.minimize()
            jarvisRed.minimize()
            jarvisYellow.minimize() 
            jarvisTalking.minimize()
        elif type == "talking":
            jarvisTalking.restore()
            jarvisPurple.minimize()
            jarvisBlue.minimize()
            jarvisGreen.minimize()
            jarvisRed.minimize()
            jarvisYellow.minimize()                  
        else:
            jarvisBlue.minimize()
            jarvisGreen.minimize()
            jarvisPurple.minimize()
            jarvisRed.minimize()
            jarvisYellow.minimize()
            jarvisTalking.minimize()

############### PRESET RANDOMIZED RESPONSES ###################

def response_randomizer(type):
    global random_response_say
    ## AGREEMENT RESPONSE
    if type in ['agreement']:
        random_response = random.randint(0,3)
        if random_response == 0:
            random_response_say = tts_dir + 'agreement/noproblem1.mp3'
        if random_response == 1:
            random_response_say = tts_dir + 'agreement/cverywell.mp3'
        if random_response == 2:
            random_response_say = tts_dir + 'agreement/certainly.mp3'
        if random_response == 3:
            random_response_say = tts_dir + 'agreement/asyouwish.mp3'
              
    ## GREETING RESPONSE
    if type in ['welcoming']:
        now = datetime.now()
        time_of_day = get_time_of_day(now.hour)
        if time_of_day == "Morning":
            random_response_say = tts_dir + 'welcoming/goodmorningsir2.mp3'
        if time_of_day == "Afternoon":
            random_response_say = tts_dir + 'welcoming/goodafternoonsir2.mp3'
        if time_of_day == "Evening":
            random_response_say = tts_dir + 'welcoming/goodeveningsir2.mp3'
        if time_of_day == "Night":
            random_response_say = tts_dir + 'welcoming/goodeveningsir2.mp3'

    ## INTRODUCTION
    if type in ['introduction']:
        random_response = random.randint(0,2)
        if random_response == 0:
            random_response_say = tts_dir + 'greeting/mynameis1.mp3'
        if random_response == 1:
            random_response_say = tts_dir + 'greeting/mynameis2.mp3'
        if random_response == 2:
            random_response_say = tts_dir + 'greeting/mynameis3.mp3'
    
    
    ## say response
    playsound.playsound(f"{random_response_say}")
        
###########
## REQUEST HASS PRIVATE AND PUBLIC STATUS
###########        
hass_local_status = check_ping_hass(hass_local)
hass_dns_status = check_ping_hass(hass_dns)
if hass_local_status == "Online":
    hass_url = hass_local
else:
    hass_url = hass_dns
    print("<#!>WARN: Local HASS Connection failed, using Public URL instead . . .")

## SET HASS API FUNCTIONS
switch_toggle = (hass_url + '/api/services/switch/toggle')
switch_turnon = (hass_url + '/api/services/switch/turn_on')
switch_turnoff = (hass_url + '/api/services/switch/turn_off')
light_toggle = (hass_url + '/api/services/light/toggle')
light_turnon = (hass_url + '/api/services/light/turn_on')
light_turnoff = (hass_url + '/api/services/light/turn_off')
script_toggle = (hass_url + '/api/services/homeassistant/toggle')

## START UI
if use_ui == "true":
    ui_dir = directory + "/data/ui"
    Popen(["python", "ui.py"], cwd=ui_dir)
    print("Loading UI . . .")
    time.sleep(8)
    jarvisRed=gw.getWindowsWithTitle('red_orb')[0]
    jarvisGreen=gw.getWindowsWithTitle('green_orb')[0]
    jarvisYellow=gw.getWindowsWithTitle('yellow_orb')[0]
    jarvisPurple=gw.getWindowsWithTitle('purple_orb')[0]
    jarvisBlue=gw.getWindowsWithTitle('J.A.R.V.I.S')[0]

                                ################## RUN JARVIS MAIN FUNCTION ####################

def main():

    print("##############################################################################")
    print("""\
     __   ___     ___    _   __   ____   ____  
 __ / /  / _ |   / _ \  | | / /  /  _/  / __/  
/ // /  / __ |  / , _/  | |/ /  _/ /   _\ \    
\___/  /_/ |_| /_/|_|   |___/  /___/  /___/    
                        Created by Vanitas                       
                    """)
    print("##############################################################################")
    print("Version: 3.1 | " + "<#>Detected Directory: " + directory)
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=microphone_device)
    print("##############################################################################")
    print("                 Powered by Jarvis Integrations Network.")
    print("Private HASS Status: " + hass_local_status + " | " + "Public HASS Status: " + hass_dns_status)
    print("##############################################################################")
    ui('main')
    response_randomizer(type='welcoming')
    history = []
    
    ## get cred .json for wavenet TTS
    pwd = os.getcwd()
    credential = ""
    for f in os.listdir("./credentials/"):
        if ".json" in f:
            credential = f
        if credential == "":
            print("No credentials json found in 'credentials' dir")
            quit()
        else:
            credential = os.path.join(pwd, "credentials", credential)
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential
            from google.cloud import texttospeech
            client = texttospeech.TextToSpeechClient()

    #loop for listening
    while True:
        user_input = recognize_speech_from_mic(recognizer, microphone)
        if user_input is None:
            continue
        
        print(f"You: {user_input}")
        history.append(f"User: {user_input}")



                                                ############### COMMANDS START ##################

        ## CURRENT TIME
        if re.search(r"(?:what |what's |tell me )(?:the|time)(?: is it| time)", user_input):
             ui('green')
             import time
             t = time.strftime("%I:%M %p")
             #V2 TTS
             audio = synthesize_text(t, client)
             play_mp3(audio)
             del history[-1]
             ui('main')
             continue
        
        ## TODAYS DATE  
        if re.search(r"what(?:'s)?(?: )(?:today's date|day is it(?: today)?)", user_input): 
             ui('green')   
             from datetime import date
             day3 = datetime.today().strftime('%A, %B %d, %Y')
             audio = synthesize_text(day3, client)
             play_mp3(audio)
             del history[-1]
             ui('main')
             continue

        ## Server Status
        if re.search(r"((?:what(?:'s| is)?)(?: the|your )(?: server status| service status)|is (?:the|your) server(?: )(?:online|offline)(?: right now)?)", user_input):    
             ui('green')
             if check_ping_physical() == "Online":
                if check_ping_hass(hass_local) == "Online":
                    response = "Both the " + hass_name + " and Physical Host Server are online and functional, sir."
                else:
                    response = "The Physical Host Server is online and functional, however the " + hass_name + " is offline, sir."
             else:
                ui('red')
                response = "Both the " + hass_name + " and Physical Host Server are offline, sir."

             audio = synthesize_text(response, client)
             play_mp3(audio)
             del history[-1]
             ui('main')
             continue        
        
##################### SMART DEVICE CONTROL #########################

########################### LIGHTS #################################

        if re.search(r'.*lights on.*|.*lights off.*', user_input):
             ui('green')
             hass_function = light_toggle
             entity_id = main_lights
             ##
             headers = {
                  'Authorization': 'Bearer ' + hass_key,
                  'Content-Type': 'application/json',
             }
             payload = {
              'entity_id': entity_id,
             }
             response = requests.post(hass_function, headers=headers, json=payload)
             del history[-1]
             ui('main')
             continue
         
######################### INTERIOR #############################
        if re.search(r'.*interior.*on.*', user_input):
             ui('green')
             hass_function = light_toggle
             entity_id = alt_lights
             headers = {
                  'Authorization': 'Bearer ' + hass_key,
                  'Content-Type': 'application/json',
             }
             payload = {
              'entity_id': entity_id,
             }
             response = requests.post(hass_function, headers=headers, json=payload)

             del history[-1]
             ui('main')
             continue

######################### FAN ################################

        if re.search(r'.*fan on.*|.*fan off.*', user_input):

             ui('green')
             hass_function = switch_toggle
             entity_id = fan
             headers = {
                  'Authorization': 'Bearer ' + hass_key,
                  'Content-Type': 'application/json',
             }
             payload = {
              'entity_id': entity_id,
             }
             response = requests.post(hass_function, headers=headers, json=payload)

             del history[-1]
             ui('main')
             continue

######################## FRIDGE ############################

        if re.search(r'.*fridge on.*|.*fridge off.*', user_input):
             
             ui('green')
             hass_function = switch_toggle
             entity_id = fridge
             headers = {
                  'Authorization': 'Bearer ' + hass_key,
                  'Content-Type': 'application/json',
             }
             payload = {
              'entity_id': entity_id,
             }
             response = requests.post(hass_function, headers=headers, json=payload)
             
             del history[-1]
             ui('main')
             continue

            ## you can add more commands using a similar format ^

            

############################################## END OF SMART DEVICE CONTROL ##############################################
        
        # close Jarvis
        if user_input.lower() in ["quit", "exit", "bye"]:
            break
        ############################################## END OF COMMANDS ##############################################
       
        # CALLING OPENAI RESPONSES (say jarvis with your query), you can change this if you want jarvis to always respond without saying its name
        if not re.search(r'.*jarvis.*|.*Jarvis.*', user_input): #VERIFY HOTWORD WAS SAID 
            continue
        ui('purple')
        prompt = "\n".join(history) + "\nAI:"
        response = generate_response(prompt)
        history.append(f"AI: {response}")
        print(f"{response}")
        voice_response = response
        audio = synthesize_text(voice_response, client)
        play_mp3(audio)
        ui('main')


if __name__ == "__main__":
    main()
