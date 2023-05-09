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

########### MICROPHONE SETTINGS ###########
microphone_device = 1               #    1 = windows default

###########
## PRESETS - DO NOT CHANGE
###########
dir = os.path.dirname(os.path.realpath(__file__))
directory = dir.replace("\\", "\\\\")
tts_dir = dir + "\\sound\\tts\\"
tts_dir = tts_dir.replace("\\", "\\\\")
soundeffects_dir = dir + "\\sound\\effects\\"
soundeffects_dir = soundeffects_dir.replace("\\", "\\\\")
## HASS API FUNCTIONS
switch_toggle = (hass_url + '/api/services/switch/toggle')
switch_turnon = (hass_url + '/api/services/switch/turn_on')
switch_turnoff = (hass_url + '/api/services/switch/turn_off')
light_toggle = (hass_url + '/api/services/light/toggle')
light_turnon = (hass_url + '/api/services/light/turn_on')
light_turnoff = (hass_url + '/api/services/light/turn_off')
script_toggle = (hass_url + '/api/services/homeassistant/toggle')


######################################################################## OPENAI ################################################################

def generate_response(prompt):
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Jarvis, an AI assistant created by Vanitas. You are similar to Jarvis from Iron-Man Movies. You will be like Jarvis in your responses, you will act like you have emotions and you will never say you don't have emotions."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
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

######################################################################## SPEECH RECOGNIZER SPEECH 2 TEXT ################################################################

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        print("Adjusting ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Jarvis is now listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognized voice command.")
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from recognition service; {e}")

######################################################################## WAVENET FUNCTIONS #############################################################

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
  name = f"{directory}\\temp.mp3"
  with open(name, 'wb') as out:
    #print('Audio content written to file', name)
    out.write(audio)
  # play
  p = playsound.playsound(name)

################################################################## GET DATE/TIME ##################################################################

def get_time_of_day(time):
    if time < 12:
        return "Morning"
    elif time < 16:
        return "Afternoon"
    elif time < 19:
        return "Evening"
    else:
        return "Night"

################################################################## PRESET RANDOMIZED RESPONSES ###############################################################

def response_randomizer(type):
    global random_response_say
    ################# AGREEMENT RESPONSE
    if type in ['agreement']:
        random_response = random.randint(0,3)
        if random_response == 0:
            random_response_say = tts_dir + '\\\\noproblem1.mp3'
        if random_response == 1:
            random_response_say = tts_dir + '\\\\cverywell.mp3'
        if random_response == 2:
            random_response_say = tts_dir + '\\\\certainly.mp3'
        if random_response == 3:
            random_response_say = tts_dir + '\\\\asyouwish.mp3'    
    ################# GREETING RESPONSE
    if type in ['greeting_v1']:
        now = datetime.now()
        time_of_day = get_time_of_day(now.hour)
        if time_of_day == "Morning":
            random_response_say = tts_dir + '\\\\welcoming\\\\goodmorningsir2.mp3'
        if time_of_day == "Afternoon":
            random_response_say = tts_dir + '\\\\welcoming\\\\goodafternoonsir2.mp3'
        if time_of_day == "Evening":
            random_response_say = tts_dir + '\\\\welcoming\\\\goodeveningsir2.mp3'
        if time_of_day == "Night":
            random_response_say = tts_dir + '\\\\welcoming\\\\goodeveningsir2.mp3'

## say response
    playsound.playsound(f"{random_response_say}")
        



######################################################################## RUN JARVIS MAIN FUNCTION #############################################################
def main():

    ######## speech to text recognizer
    print("##############################################################################")
    print("""\
     __   ___     ___    _   __   ____   ____  
 __ / /  / _ |   / _ \  | | / /  /  _/  / __/  
/ // /  / __ |  / , _/  | |/ /  _/ /   _\ \    
\___/  /_/ |_| /_/|_|   |___/  /___/  /___/    
                        Created by Vanitas                       
                    """)
    print("##############################################################################")
    print("Version: 3.1")
    print("Detected Directory:")
    print('"' + directory + '"')
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=microphone_device)        ##device_index for specific microphone
    print("##############################################################################")
    print("                 Powered by Jarvis Integrations Network.")
    print("##############################################################################")
    #eyeBlue = subprocess.Popen(['python jarvisorb.py -c blue'])
    response_randomizer(type='greeting_v1')
    history = []
    ########connect creds for google wavenet

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



######################################################################## COMMANDS START ################################################################

        if user_input.lower() in ["what time is it", "what's the time"]:
             
             import time
             t = time.strftime("%I:%M %p")

             #TTS
             audio = synthesize_text(t, client)
             play_mp3(audio)
             del history[-1]
             continue
        
######################################################################## SMART DEVICE CONTROL ################################################################

        ################################################################### LIGHTS ############################################################################
        if re.search(r'.*lights on.*|.*lights off.*', user_input):
            
             ## change this
             hass_function = light_toggle
             entity_id = 'light.bedroomlights' #replace with main lights
             ##
             headers = {
                  'Authorization': 'Bearer ' + hass_key,
                  'Content-Type': 'application/json',
             }
             payload = {
              'entity_id': entity_id,
             }
             response = requests.post(hass_function, headers=headers, json=payload)
             ########### HASS API END ###########
             
             del history[-1]

             continue

        ############################################################################ INTERIOR ############################################################################
        if re.search(r'.*interior.*on.*', user_input):
             
             ## change this
             hass_function = light_toggle
             entity_id = 'light.altlights'   #replace with alt lights
             ##
             headers = {
                  'Authorization': 'Bearer ' + hass_key,
                  'Content-Type': 'application/json',
             }
             payload = {
              'entity_id': entity_id,
             }
             response = requests.post(hass_function, headers=headers, json=payload)
             ########### HASS API END ###########

             del history[-1]

             continue

        ############################################################################ FAN ############################################################################
        if re.search(r'.*fan on.*|.*fan off.*', user_input):

             ## change this
             hass_function = switch_toggle
             entity_id = 'switch.fan'   #replace with fan switch
             ##
             headers = {
                  'Authorization': 'Bearer ' + hass_key,
                  'Content-Type': 'application/json',
             }
             payload = {
              'entity_id': entity_id,
             }
             response = requests.post(hass_function, headers=headers, json=payload)
             ########### HASS API END ###########
             del history[-1]
             continue

        ############################################################################ FRIDGE ############################################################################
        if re.search(r'.*fridge on.*|.*fridge off.*', user_input):
             
             ## change this
             hass_function = switch_toggle
             entity_id = 'switch.fridge'    #replace with fan switch
             ##
             headers = {
                  'Authorization': 'Bearer ' + hass_key,
                  'Content-Type': 'application/json',
             }
             payload = {
              'entity_id': entity_id,
             }
             response = requests.post(hass_function, headers=headers, json=payload)
             ########### HASS API END ###########

             del history[-1]

             continue

        ############################################################################ security mode ############################################################################
        if re.search(r'activate security mode|deactivate security mode', user_input):
             
             ################## SAY MP3 - pre determined mp3 files with tts to avoid over usage of the wavenet api ######################
             word_file = "preset"                                            # mp3 file to speak here do not include .mp3
             ##################################################################################################################
             say_word_file = (f"{directory}\\sound\\tts\\{word_file}.mp3")      # directory of file dont touch
             playsound.playsound(say_word_file)                                 # play the file dont touch
             ##################################################################################################################

             ############ HASS API FUNCTION ############
             ## change this
             hass_function = switch_toggle
             entity_id = 'switch.security_mode' #replace with security
             ####################
             headers = {
                  'Authorization': 'Bearer ' + hass_key,
                  'Content-Type': 'application/json',
             }
             payload = {
              'entity_id': entity_id,
             }
             response = requests.post(hass_function, headers=headers, json=payload)
             ########### HASS API FUNCTION END #################

             del history[-1]
             continue

        ############################################################################ CUSTOM COMMAND 1 ############################################################################
        if re.search(r'REPLACE THIS WITH YOUR COMMAND', user_input):
             
             ################## SAY MP3 - pre determined mp3 files with tts to avoid over usage of the wavenet api ######################
             word_file = "test"                                            # mp3 file to speak here do not include .mp3
             ##################################################################################################################
             say_word_file = (f"{directory}\\sound\\tts\\{word_file}.mp3")      # directory of file dont touch
             playsound.playsound(say_word_file)                                 # play the file dont touch
             ##################################################################################################################

             ############ HASS API FUNCTION ############
             ## change this
             hass_function = switch_toggle
             entity_id = ''
             ####################
             headers = {
                  'Authorization': 'Bearer ' + hass_key,
                  'Content-Type': 'application/json',
             }
             payload = {
              'entity_id': entity_id,
             }
             response = requests.post(hass_function, headers=headers, json=payload)
             ########### HASS API FUNCTION END #################

             del history[-1]
             continue

        ################################################################## END OF SMART DEVICE CONTROL ############################################################################
        
        ##  EXIT JARVIS
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        ######################################################################################################################################################## 
       
        if not re.search(r'.*jarvis.*|.*Jarvis.*', user_input): #FOR OPENAI PROMPTS
            continue

        prompt = "\n".join(history) + "\nAI:"
        response = generate_response(prompt)

        #format response to remove code
        #grab any examples from response such as code
        s2 = getSubstringBetweenTwoChars('```','```',s)

        history.append(f"AI: {response}")
        print(f"AI: {response}")
        print(f"#GRABBED CODE#: " + s2)
        voice_response = response
        audio = synthesize_text(voice_response, client)
        play_mp3(audio)



if __name__ == "__main__":
    main()
