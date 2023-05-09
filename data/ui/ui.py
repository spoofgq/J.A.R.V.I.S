################################################################## JARVIS ORB ANIMATED ###############################################################
from pathlib import Path
from subprocess import Popen
import os
from time import sleep

Popen(["python", "main/redorb.py"])
Popen(["python", "main/yelloworb.py"])
Popen(["python", "main/greenorb.py"])
Popen(["python", "main/purpleorb.py"])
Popen(["python", "main/talking.py"])
sleep(2)
Popen(["python", "main/blueorb.py"])
while True:
    pass
