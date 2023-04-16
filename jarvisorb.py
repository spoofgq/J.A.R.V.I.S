################################################################## JARVIS ORB ANIMATED ###############################################################
import tkinter
import time
from tkinter import *
from tkvideo import tkvideo
import argparse
orbBlue = "gui\\JARVIS ORB BLUEv2.gif"
orbGreens = "gui\\JARVIS ORB GREENv2.gif"
orbYellow = "gui\\JARVIS ORB YELLOWv2.gif"
orbPurple = "gui\\JARVIS ORB PURPLEv2.gif"
orbRed = "gui\\JARVIS ORB REDv2.gif"
parser = argparse.ArgumentParser(description='orb type')
parser.add_argument('-c', '--color', help='blue, green, yellow, purple, red', default="blue")
parser.add_argument('-d', '--destroy', help='yes', required=False)
args = parser.parse_args()


if args.color == "blue":
    orb = orbBlue
if args.color == "green":
    orb = orbGreens
if args.color == "yellow":
    orb = orbYellow
if args.color == "purple":
    orb = orbPurple
if args.color == "red":
    orb = orbRed

if __name__ == '__main__':
    root = Tk()
    my_label = Label(root, borderwidth=0)
    my_label.pack()
    my_label.pack(anchor="center", pady=130)
    player = tkvideo(orb, my_label, loop = 1, size = (500,500))
    root.attributes('-fullscreen',True)
    root.configure(bg='black')
    player.play()
    root.mainloop()