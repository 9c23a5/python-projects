from cmath import sqrt
from dis import dis
from math import dist
import threading
from time import sleep
from tkinter import *
from tkinter.tix import ButtonBox
from colour import Color
import cv2

image_file="heart.png"

def debug_show_image(cv_image):
    cv2.imshow('image',cv_image)
    c = cv2.waitKey()
    if c >= 0 : return -1
    return 0

def contour_coords(filename):
    coordsX = []
    coordsY = []

    image = cv2.imread(filename)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, im = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY_INV)
    #debug_show_image(im)
    contours, hierarchy  = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        for i in range(0, len(cnt)):
            x = cnt[i][0][0]
            y = cnt[i][0][1]
            print(f"Debug: {x=} {y=}")
            coordsX.append(str(x))
            coordsY.append(str(y))
            
    return coordsX, coordsY

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
            sleep(0.0001)
        for x in range(max_x, 0, -1):
            print(f"{x=}")
            root.geometry(f"200x200+{x}+{init_y}")
            sleep(0.0001)


def move_coords(root, coordsX, coordsY):
    while True:
        for i in range(0, len(coordsX)):
            x = coordsX[i]
            y = coordsY[i]
            try:
                x2 = int(coordsX[i+1])
                y2 = int(coordsY[i+1])
            except IndexError:
                x2 = int(coordsX[0])
                y2 = int(coordsY[0])
            distance = abs(sqrt((x2-int(x))^2 + (y2-int(y))^2))
            print(f"{x=} {y=}\n{x2=} {y2=}\n{distance=}")
            root.geometry(f"200x200+{x}+{y}")
            sleep(0.01)


def mycallback():
    print("Starting move...")
    root.button["state"] = "disabled"
    
    #threading.Thread(target=moving, args=(root,), daemon=True).start()
    threading.Thread(target=move_coords, args=(root,coordsX, coordsY), daemon=True).start()


print("Getting coordinates from file...")
coordsX, coordsY = contour_coords(image_file)

root = Tk()
#root.overrideredirect(True)
root.geometry("200x200+200+200")
root["bg"] = "green"
root.resizable(0,0)

root.button = Button(text="Move!", command=mycallback)
root.button.pack()

root.mainloop()
