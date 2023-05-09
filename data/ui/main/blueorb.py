################################################################## JARVIS ORB ANIMATED ###############################################################
from tkinter import *
from tkvideo import tkvideo
from pathlib import Path
orbBlue = str(Path("JARVIS ORB BLUEv2.gif"))
orbBlue = orbBlue.replace("\\", "/")


if __name__ == '__main__':

    root = Tk()

    ## blue orb
    orbElement = Label(root, borderwidth=0)
    orbElement.pack(anchor="center", pady=130)
    player = tkvideo(orbBlue, orbElement, loop = 1, size = (500,500))
    root.attributes('-fullscreen',True)
    root.configure(bg='black')
    root.title('J.A.R.V.I.S')
    #root.overrideredirect(True)
    player.play()
    root.mainloop()
    