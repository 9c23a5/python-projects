import threading
from time import sleep
from tkinter import *
from tkinter.tix import ButtonBox
from colour import Color

gradientSteps = [
    # https://i.imgur.com/Gy9fUR8.png
    "#b3000c",   # Blood
    "#c70048",   # Crimson Glory
    "#d7008a",   # Mexican Pink
    "#ed30cd",   # Razzle Dazzle Rose
    "#f55ce7",   # Purple Pizzazz
    "#fa86f2",    # Light Fuchsia Pink
]

squares=3
fps = 144
durationGradient = 3

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


def generateGradient(mainColors, fps, duration):
    gradient = []

    numGradients = len(mainColors)-1
    framerate = 1/fps

    exclude = (numGradients - 1) * 2
    
    # S = ( ( D / F ) + E ) / G

    steps = round(( ( duration / framerate) + exclude ) / numGradients)


    print(f"{steps=}")

    for step in range(0, numGradients):
        currentColor = Color(mainColors[step])
        nextColor = Color(mainColors[step+1])
        print(f"Appending gradient between {currentColor} and {nextColor}")
        for color in currentColor.range_to(nextColor, steps):
            if color not in gradient:
                print(color, end="", flush=True)
                print("\r", end="", flush=True)
                gradient.append(color)

    return gradient
        


def colorChanger(colors, fps):
    framerate = 1/fps
    print(f"Thread launched with {fps=}/{framerate=}")
    while True:
        for color in colors:
            #print("Changing to", color)
            root["bg"] = color
            sleep(framerate)
        colors.reverse()


def mycallback():
    print("Starting color change...")
    root.button["state"] = "disabled"

    colorList = generateGradient(gradientSteps, fps, durationGradient)

    print("Starting thread...")
    print(f"{len(colorList)=}")

    threading.Thread(target=colorChanger, args=(colorList,fps), daemon=True).start()


root = Tk()
#root.overrideredirect(True)
root.geometry("200x200")
root["bg"] = gradientSteps[0]
root.resizable(0,0)

root.button = Button(text="Start!", command=mycallback)
root.button.pack()

root.mainloop()
while True:
    input("Press Enter to start!")
