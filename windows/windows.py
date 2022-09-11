from math import sqrt, floor
from numpy import mean
import threading
from time import sleep
from tkinter import *
#from tkinter.tix import ButtonBox
from colour import Color
import cv2


gradientSteps = [
    # https://i.imgur.com/Gy9fUR8.png
    "#b3000c",   # Blood
    "#c70048",   # Crimson Glory
    "#d7008a",   # Mexican Pink
    "#ed30cd",   # Razzle Dazzle Rose
    "#f55ce7",   # Purple Pizzazz
    "#fa86f2",    # Light Fuchsia Pink
]


#######################################
#
# Default settings
#
#######################################

num_windows = 5
window_size = 100
image_file="heart.png"
squares=3
fps = 144
durationGradient = 3
min_smooth_distance = 1.4142135623730951


#######################################
#
# Threading functions
#
#######################################

def createWindow(x:str, y:str):
    window = Tk()
    window.overrideredirect(True)
    window.geometry(f"100x100+{x}+{y}")
    window.resizable(0,0)
    window.configure(bg="red")
    return window


#######################################
#
# Movement functions
#
#######################################

def debug_show_image(cv_image):
    cv2.imshow('image',cv_image)
    c = cv2.waitKey()
    if c >= 0 : return -1
    return 0


def generate_coords(filename):
    coords = []

    image = cv2.imread(filename)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, im = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY_INV)
    #debug_show_image(im)
    contours, hierarchy  = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        for i in range(0, len(cnt)):
            x = cnt[i][0][0]
            y = cnt[i][0][1]
            #print(f"Debug: {x=} {y=}")
            coords.append([x, y])
            #coords.append({'x' : x, 'y' : y}) #list of dicts
            
    return coords


def move_coords(root, coords, start):
    while True:
        for xy in coords[start:]:
            x = xy[0]
            y = xy[1]

            try:
                index_2ndxy = coords.index(xy)+1
                xy2 = coords[index_2ndxy]
            except IndexError:
                index_2ndxy = 0
                xy2 = coords[index_2ndxy]

            x2 = xy2[0]
            y2 = xy2[1]

            distance = sqrt(pow((x2-x), 2) + pow((y2-y), 2))

            print(f"{x=} {y=} || {x2=} {y2=} || {coords.index(xy)=} {start=} || {distance=}", end="", flush=True)
            print("\r", end="", flush=True)

            root.geometry(f"{window_size}x{window_size}+{str(x-100)}+{str(y-100)}")


            if start != 0 and coords.index(xy) == len(coords)-1:
                start = 0
            
            sleep(0.001)


def half_point(x1, y1, x2, y2):
    half_x = mean((x1+x2)/2)
    half_y = mean((y1+y2)/2)
    return int(half_x), int(half_y)

def smooth(coords, limit):
    while True:
        halfs_created = 0
        lastOne = False
        for i in range(0, len(coords)):
            xy1 = coords[i]

            try:
                xy2 = coords[i+1]
            except IndexError:
                xy2 = coords[0]
            
            x1 = xy1[0]; y1 = xy1[1]; x2 = xy2[0]; y2 = xy2[1]

            distance = sqrt(pow((x2-x1),2) + pow((y2-y1),2))

            if distance > limit:
                halfs_created =+ 1
                print("Higher distance (%s) found", distance)
                new_x, new_y = half_point(x1, y1, x2, y2)
                print(f"{i=} ||{x1=}, {y1=} || {new_x=}, {new_y=} || {x2=}, {y2=}")
                coords.insert(i+1, [new_x, new_y])
            

        if halfs_created == 0:
            print("No more smoothing")
            return coords


#######################################
#
# Color functions
#
#######################################

def generateGradient(mainColors, fps, duration):
    gradient = []

    numGradients = len(mainColors)-1
    framerate = 1/fps

    exclude = (numGradients - 1) * 2

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
    root.button["state"] = "disabled"

    colorList = generateGradient(gradientSteps, fps, durationGradient)
    coords = generate_coords(image_file)
    coords = smooth(coords, min_smooth_distance)

    print("Starting thread...")
    print(f"[DEBUG] {len(colorList)=}")
    print(f"[DEBUG] {len(coords)=}")
    coords_step = floor(len(coords)/(num_windows))
    starting_index = []
    for i in range(coords_step, len(coords), coords_step):
        print(f"[DEBUG] {i=}, {coords[i]=}")
        starting_index.append(i)

    threading.Thread(target=colorChanger, args=(colorList,fps), daemon=True).start()
    threading.Thread(target=move_coords, args=(root, coords, starting_index[0])).start()
    



root = Tk()
root.overrideredirect(True)
root.attributes('-topmost', True)
root.geometry(f"{window_size}x{window_size}")
root["bg"] = gradientSteps[0]
root.resizable(0,0)

root.button = Button(text="Start!", command=mycallback)
root.button.pack()

root.mainloop()
