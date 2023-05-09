################################################################## JARVIS ORB ANIMATED ###############################################################
from tkinter import *
from tkvideo import tkvideo
from pathlib import Path
orbYellow = str(Path("JARVIS ORB YELLOWv2.gif"))
orbYellow = orbYellow.replace("\\", "/")

if __name__ == '__main__':

    root = Tk()


    orbElement = Label(root, borderwidth=0)
    orbElement.pack(anchor="center", pady=130)
    player = tkvideo(orbYellow, orbElement, loop = 1, size = (500,500))
    root.attributes('-fullscreen',True)
    root.configure(bg='black')
    root.title('yellow_orb')
    #root.overrideredirect(True)
    player.play()
    root.mainloop()
    