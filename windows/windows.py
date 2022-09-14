from math import sqrt
import threading
from time import sleep
from tkinter import *
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
# Settings
#
#######################################

num_windows = 55
window_size = 15
image_file="heart.png"
fps = 144
durationGradient = 1
min_smooth_distance = 1.4142135623730951


#######################################
#
# Threading functions
#
#######################################

def createWindow(x:int, y:int):
    window = Tk()
    window.overrideredirect(True)
    window.geometry(f"{window_size}x{window_size}+{str(x)}+{str(y)}")
    window.resizable(0,0)
    window.configure(bg=gradientSteps[0])
    return window

def launch_mainloop(root, win_id):
    root.mainloop()
    globals[win_id] = root

def killAllThreads(*args, **kwargs):
    exit(0)



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
    w, h, c = image.shape
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #debug_show_image(img_gray)
    ret, im = cv2.threshold(img_gray, 1, 255, cv2.THRESH_BINARY)
    #debug_show_image(im)
    contours, hierarchy  = cv2.findContours(im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        for i in range(0, len(cnt)):
            x = cnt[i][0][0]
            y = cnt[i][0][1]
            #print(f"Debug: {x=} {y=}")
            coords.append([x, y])
            #coords.append({'x' : x, 'y' : y}) #list of dicts
    
    size = [w, h]
    return coords, size


def move_coords(window_list, coords, start_list):
    print(f"move_coords launched with {len(coords)} points!")
    while True:
        for cord_number in range(0, len(coords)):
            for window_id in range(0, len(window_list)):
                starting_point = start_list[window_id]
                cord_pos = cord_number+starting_point

                while cord_pos > len(coords)-1:
                    cord_pos -= len(coords)-1

                xy = coords[cord_pos]
                x = xy[0]-window_size
                y = xy[1]-window_size

                #print(f"Moving {window_id=} to {x=}, {y=}")
                
                window_list[window_id].geometry(f"{window_size}x{window_size}+{str(x)}+{str(y)}")
        sleep(0.001)
                
        


def half_point(x1, y1, x2, y2):
    half_x = round((x1+x2)/2)
    half_y = round((y1+y2)/2)
    return half_x, half_y


def smooth(coords, limit):
    total_points = 0
    while True:
        halfs_created = 0
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
                total_points =+ 1
                new_x, new_y = half_point(x1, y1, x2, y2)
                #print(f"{i=} ||{x1=}, {y1=} || {new_x=}, {new_y=} || {x2=}, {y2=}")
                coords.insert(i+1, [new_x, new_y])
            

        if halfs_created == 0:
            print(f"[smooth] Points created while smoothing: {total_points}")
            print("[smooth] No more smoothing needed...")
            return coords


def center(coords, w_screen, h_screen, w_img, h_img):
    diff = [int((w_screen/2)-(w_img/2)+(window_size/2)), int((h_screen/2)-(h_img/2)+(window_size/2))]
    for i in range(0, len(coords)):
        coords[i][0] += diff[0]
        coords[i][1] += diff[1]
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


    print(f"[generateGradient] Colors per gradient: {steps}")

    for step in range(0, numGradients):
        currentColor = Color(mainColors[step])
        nextColor = Color(mainColors[step+1])
        print(f"[generateGradient] Appending gradient between {currentColor} and {nextColor}")
        for color in currentColor.range_to(nextColor, steps):
            if color not in gradient:
                print(color, end="", flush=True)
                print("\r", end="", flush=True)
                gradient.append(color)
    return gradient
        

def colorChanger(window_list, colors, fps):
    frametime = 1/fps
    print(f"colorChanger launched with {fps=}/{frametime=}\n")
    while True:
        for color in colors:
            print("Current color:", color, end='', flush=True)
            print('\r', end='', flush=True)
            for window in window_list:
                window["bg"] = color
            sleep(frametime)
        colors.reverse()


def mycallback():
    global num_windows
    main_root.withdraw() 

    colorList = generateGradient(gradientSteps, fps, durationGradient)

    coords, image_size = generate_coords(image_file)
    coords = smooth(coords, min_smooth_distance)
    coords = center(coords, screen_size[0], screen_size[1], image_size[0], image_size[1])
    

    print("Launching!")
    print(f"[DEBUG] {len(colorList)=}")
    print(f"[DEBUG] {len(coords)=}")
    print(f"[DEBUG] {screen_size=} {image_size=}")

    coords_step = round(len(coords)/num_windows)
    starting_index = []
    for i in range(0, len(coords), coords_step):
        #print(f"[DEBUG] {i=}, {coords[i]=}")
        starting_index.append(i)

    print(f"[DEBUG] {len(starting_index)=} for {num_windows=}")
    
    if len(starting_index) == num_windows-1:
        #print("[DEBUG] Added one more starting_index")
        #starting_index.append(len(coords)-1)
        print("[DEBUG] Removing excess window...")
        #num_windows = num_windows - 1
        num_windows = num_windows - 1
        child_windows.remove(child_windows[num_windows])

    for window_id in range(0, len(child_windows)):
        print(f"Starting process on {window_id=}", end='', flush=True)
        print('\r', end='', flush=True)
        child_windows[window_id].deiconify()
    print(f"{'='*15} {num_windows} windows created! {'='*15}")
    print("\nPress Q to quit\n")
    
    threading.Thread(target=move_coords, args=(child_windows, coords, starting_index), daemon=True).start()
    threading.Thread(target=colorChanger, args=(child_windows, colorList, fps), daemon=True).start()



main_root = Tk()

screen_size = [main_root.winfo_screenwidth(), main_root.winfo_screenheight()]

main_root.overrideredirect(True)
main_root.attributes('-topmost', True)

wide_mid = int((screen_size[0]/2)-100)
height_mid = int((screen_size[1]/2)-100)

main_root.geometry(f"200x200+{wide_mid}+{height_mid}")
main_root["bg"] = gradientSteps[0]
main_root.resizable(0,0)

main_root.button = Button(text="Start!", command=mycallback)
main_root.button.pack()

child_windows = []

def create_child(root):
    child = Toplevel(root)
    child.geometry("0x0+0+0")
    child.overrideredirect(True)
    child.attributes('-topmost', True)
    child.resizable(0,0)
    child.withdraw()
    child.bind('<KeyPress-Q>', killAllThreads)
    child.bind('<KeyPress-q>', killAllThreads)
    return child
    

for i in range(0, num_windows):
    print(f"Creating child ID {i}", end='', flush=True)
    print('\r', end='', flush=True)
    child_windows.append(create_child(main_root))

print(f"{'='*15} Ready! {'='*15}")

main_root.mainloop()
