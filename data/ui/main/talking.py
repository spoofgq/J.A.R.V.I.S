################################################################## JARVIS ORB ANIMATED ###############################################################
from tkinter import *
from tkvideo import tkvideo
from pathlib import Path
orbBlueTalking = str(Path("JARVIS ORB TALKING.gif"))
orbBlueTalking = orbBlueTalking.replace("\\", "/")


if __name__ == '__main__':

    root = Tk()

    ## blue orb talking
    orbElement = Label(root, borderwidth=0)
    orbElement.pack(anchor="center", pady=130)
    player = tkvideo(orbBlueTalking, orbElement, loop = 1, size = (500,500))
    root.attributes('-fullscreen',True)
    root.configure(bg='black')
    root.title('talking_orb')
    #root.overrideredirect(True)
    player.play()
    root.mainloop()
    