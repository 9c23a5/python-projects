from tkinter import *


prefs = {
  # "variable_name" : [Default, FriendlyName, TypeOf]
    "asdas" : ["Yes", 'Do you need asdas?', 'str'],
    "prpfrpfr" : [2, 'How many prfprfr', 'int'],
    "n_meows?" : [999, 'Number of meows', 'int'],
    "victor_kills" : [420, 'Owned with Victor on League?', 'int'],
    "asdasds" : ["sadsa", "dkfjkdshfd?", 'str']
}

sz_main = 400
outer_pad = 35
inner_pad = 10
bg = '#2b2b2b'
bg_widget = '#353535'
fg = 'white'

main = Tk()

main.overrideredirect(True)
main.attributes('-topmost', True)

w_main = int(main.winfo_screenwidth()/2 - sz_main/2)
h_main = int(main.winfo_screenheight()/2 - sz_main/2)

main.geometry(f"{sz_main}x{sz_main}+{w_main}+{h_main}")
main["bg"] = bg
main.resizable(0,0)

all_entries = []
y_counter = outer_pad

for i in prefs:

    my_label = Label(main, text=prefs[i][1], bg=bg, fg=fg)
    my_label.place(x=0, y=0)
    main.update()
    my_label.place(x=sz_main/2-inner_pad-my_label.winfo_width(), y=y_counter)

    my_entry = Entry(main, bg=bg_widget, fg=fg)
    my_entry.place(x=sz_main/2+inner_pad, y=y_counter, width=my_label.winfo_width())
    my_entry.insert(0, prefs[i][0])
    all_entries.append(my_entry)

    y_counter += my_label.winfo_height() + inner_pad

main.mainloop()
