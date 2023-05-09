# J.A.R.V.I.S: An AI Voice Assistant utilizing OpenAI Technology, and Home Assistant smart-device control. Yes, like Ironman.


###### Features ######

Voice recognition and Google Wavenet TTS responses
Text-to-speech and speech-to-text capabilities using gtts, pygame, and speech_recognition libraries
Home Assistant Device Control
User-friendly and interactive experience

# Installation

Clone the repository

# Install the required libraries:

pip install -r requirements.txt

# Setup Google Wavenet TTS API

Add your .json file to /credentials

# Use Jarvis UI / Optional
use_ui = 'true'     # leave empty if you don't want the jarvis ui

# Add your OpenAI API key to the script:

openai_key = "your_key_here"

# Add your Home Assistant Settings
hass_name = ''  # the name of your HASS instance (anything you want) <br>
hass_dns = ''   # (ex. https://yourhassdomain.duckdns.org:443) <br>
hass_local = ''    # the local ip address/port (ex. http://192.168.1.1:8123) <br>
host_server = ''   # only set if you're running hass on a VM - this is your VM's host IP <br>
hass_key = '' # your hass auth key <br>

# HASS Devices (change to your actual device ids on your hass instance)
main_lights = ''
alt_lights = '' 
fan = ''
fridge = ''
security_mode = ''

# HASS Scripts (custom scripts you may want Jarvis to control)
script_1 = ''
script_2 = ''
script_3 = ''
script_4 = ''
script_5 = ''

# Run JARVIS-MAIN
python JARVIS-MAIN.py

