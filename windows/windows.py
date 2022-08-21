from tkinter import *
from tkinter.tix import ButtonBox

# size = 60
# windows = {}

# for y in range(0, 1000, 10):
#     windows[str(y)] = Tk()
#     windows[str(y)].geometry(f"{size}x{size}+0+{y}")
#     windows[str(y)].wm_attributes('-fullscreen', 'True')

# for i in windows:
#     windows[i].mainloop()

# Sample window, 100x100 with only red background

def createWindow(x:str, y:str):
    window = Tk()
    window.overrideredirect(True)
    window.geometry(f"100x100+{x}+{y}")
    window.resizable(0,0)
    window.configure(bg="red")
    return window

# w1 = createWindow("950", "300")
# w1.mainloop()

def mycallback():
    if root["bg"] == "red":
        root["bg"] = "blue"
    else:
        root["bg"] = "red"

root = Tk()
root.geometry("200x200")
root["bg"] = "blue"
root.resizable(0,0)
root.button = Button(text="Button!", command=mycallback)
root.button.pack()
root.mainloop()
