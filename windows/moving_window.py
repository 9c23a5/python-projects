import threading
from time import sleep
from tkinter import *
from tkinter.tix import ButtonBox
from colour import Color

def moving(root):
    init_x = root.winfo_x()
    init_y = root.winfo_y()
    max_x = (root.winfo_screenwidth() - 200)

    print(f"{init_x=} {init_y=}")
    while True:
        # x to 1920
        for x in range(root.winfo_x(), max_x):
            print(f"{x=}")
            root.geometry(f"200x200+{x}+{init_y}")
            #sleep(0.0001)
        for x in range(max_x, 0, -1):
            print(f"{x=}")
            root.geometry(f"200x200+{x}+{init_y}")

def mycallback():
    print("Starting move...")
    root.button["state"] = "disabled"
    
    threading.Thread(target=moving, args=(root,), daemon=True).start()



root = Tk()
#root.overrideredirect(True)
root.geometry("200x200+200+200")
root["bg"] = "green"
root.resizable(0,0)

root.button = Button(text="Move!", command=mycallback)
root.button.pack()

root.mainloop()
