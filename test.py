from datetime import datetime
from datetime import timedelta

import time


from tkinter import *

root = Tk()
prompt = "\nHello"
label1 = Label(root, text=prompt, width=len(prompt))
label1.pack()

def close_after_2s():
    root.destroy()

root.after(2000, close_after_2s)
root.mainloop()
