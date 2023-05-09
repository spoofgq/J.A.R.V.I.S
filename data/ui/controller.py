################################################################## JARVIS ORB ANIMATED ###############################################################
import tkinter
import time
from tkinter import *
from tkvideo import tkvideo
from pathlib import Path
import argparse
import pygetwindow as gw 


def ui(orb):
    jarvisBlue=gw.getWindowsWithTitle('J.A.R.V.I.S')[0]
    jarvisRed=gw.getWindowsWithTitle('red_orb')[0]
    jarvisGreen=gw.getWindowsWithTitle('green_orb')[0]
    jarvisYellow=gw.getWindowsWithTitle('yellow_orb')[0]
    jarvisPurple=gw.getWindowsWithTitle('purple_orb')[0]
    jarvisTalking=gw.getWindowsWithTitle('talking_orb')[0]
    orb.restore()

def ui_exit(orb):
    jarvisBlue=gw.getWindowsWithTitle('J.A.R.V.I.S')[0]
    jarvisRed=gw.getWindowsWithTitle('red_orb')[0]
    jarvisGreen=gw.getWindowsWithTitle('green_orb')[0]
    jarvisYellow=gw.getWindowsWithTitle('yellow_orb')[0]
    jarvisPurple=gw.getWindowsWithTitle('purple_orb')[0]
    jarvisTalking=gw.getWindowsWithTitle('talking_orb')[0]
    orb.minimize()