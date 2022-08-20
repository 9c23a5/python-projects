from tkinter import *

# size = 60
# windows = {}

# for y in range(0, 1000, 10):
#     windows[str(y)] = Tk()
#     windows[str(y)].geometry(f"{size}x{size}+0+{y}")
#     windows[str(y)].wm_attributes('-fullscreen', 'True')

# for i in windows:
#     windows[i].mainloop()

# Sample window, 100x100 with only red background

w1 = Tk()
w1.overrideredirect(True)
w1.geometry("100x100+600+100")
# w.wm_attributes("-toolwindow", True)
w1.resizable(0,0)
w1.configure(bg="red")

w1.mainloop()
