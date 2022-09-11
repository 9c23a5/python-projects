from math import sqrt
from numpy import mean
from dis import dis
from math import dist
import random
import threading
from time import sleep
import cv2
from tkinter import *

image_file="heart.png"


def debug_show_image(cv_image):
    cv2.imshow('image',cv_image)
    c = cv2.waitKey()
    if c >= 0 : return -1
    return 0


def contour_coords(filename):
    coords = []

    image = cv2.imread(filename)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, im = cv2.threshold(img_gray, 126, 255, cv2.THRESH_BINARY_INV)
    #debug_show_image(im)
    contours, hierarchy  = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        for i in range(0, len(cnt)):
            x = cnt[i][0][0]
            y = cnt[i][0][1]
            print(f"Debug: {x=} {y=}")
            coords.append([x, y])
            
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

            distance = sqrt(pow((x2-x),2) + pow((y2-y),2))

            print(f"{x=} {y=} || {x2=} {y2=} || {coords.index(xy)=} {start=} || {distance=}", end="", flush=True)
            print("\r", end="", flush=True)

            root.geometry(f"200x200+{str(x-100)}+{str(y-100)}")

            if start != 0 and coords.index(xy) == len(coords)-1:
                start = 0
            
            sleep(0.001)

def find_min_dist(coords):
    min_distance = 9999
    for i in range(0, len(coords)):
        xy = coords[i]

        try:
            xy2 = coords[i+1]
        except IndexError:
            xy2 = coords[0]
        
        x = xy[0]; y = xy[1]
        x2 = xy2[0]; y2 = xy2[1]
        
        distance = sqrt(pow((x2-x),2) + pow((y2-y),2))


        if distance < min_distance:
            print("new!")
            print(f"{x=}, {x2=}, {y=}, {y2=}")
            print(distance)
            min_distance = distance
    return min_distance

def half_point(x1, y1, x2, y2):
    half_x = mean((x1+x2)/2)
    half_y = mean((y1+y2)/2)
    return int(half_x), int(half_y)

def smooth(coords, limit):
    while True:
        halfs_created = 0
        for i in range(0, len(coords)):
            xy1 = coords[i]
            try:
                xy2 = coords[i+1]
            except:
                break
            
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

            


coords = contour_coords(image_file)

limit = 1.4142135623730951

print(f"{limit=}")

smoothed = smooth(coords, limit)

root = Tk()
root.overrideredirect(True)
root.geometry("200x200+200+200")
root["bg"] = "green"
root.attributes('-topmost', True)
root.resizable(0,0)




threading.Thread(target=move_coords, args=(root, smoothed, 0), daemon=True).start()
root.mainloop()