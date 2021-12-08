import tkinter as tk
from tkinter import filedialog as filed

import full_duplex as fd

BBH:fd.dualBB_handler = None
def exec_fd():
    try:
        global BBH
        BBH = fd.dualBB_handler(txserial="00000008", rxserial="ffffffff", power=8)
        fd.txThread = fd.tx_thread(BBH)
        fd.rxThread = fd.rx_thread(BBH)
        textbox.config(text="successfully initialized BBH", fg="green")
    except Exception as ex:
        textbox.config(text="ERROR: failed to initialize BBH, is two blueboxes plugged in and initialized correctly?", fg="red")
        print(e)

def queue_text():
    global BBH
    if BBH is not None:
        BBH.tq.put(e.get())
        textbox.config(text="successfully queued item", fg="green")
    else:
        textbox.config(text="ERROR: failed to queue item, is BBH initialized?", fg="red")

def queue_file():
    if BBH is not None:
        filename = filed.askopenfilename(title="open a file", initialdir="~")
        with open(filename, "r") as file:
            ba = bytearray(file.read(), "utf-8")
            Index = 0
            while Index<len(ba):
                data = ba[Index:Index+80]
                Index += 80
                BBH.tq.put(bytearray.decode(data, "utf-8"))
        textbox.config(text="successfully queued file!", fg="green")
    else:
        filename = filed.askopenfilename(title="open a file", initialdir=".")
        with open(filename, "r") as file:
            ba = bytearray(file.read(), "utf-8")
            Index = 0
            while Index<len(ba):
                data = ba[Index:Index+80]
                Index += 80
                print(bytearray.decode(data, "utf-8"))
        textbox.config(text="ERROR: failed to queue file, is BBH initialized?", fg="red")

def get_queue():
    if BBH is not None:
        print(BBH.tq.items)
        textbox.config(text="successfully got queue", fg="green")
    else:
        textbox.config(text="ERROR: failed to get queue, is BBH initialized?", fg="red")

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

button = tk.Button(frame, 
                   text="QUIT", 
                   fg="red",
                   command=quit)
button.pack(side=tk.LEFT)
exec_button = tk.Button(frame,
                   text="init full-duplex",
                   command=exec_fd)
exec_button.pack(side=tk.LEFT)

queue_button = tk.Button(frame, text="queue", command=queue_text)
queue_button.pack(side=tk.LEFT)

queue_file_button = tk.Button(frame,text="queue file", command=queue_file)
queue_file_button.pack(side=tk.LEFT)

get_queue_button = tk.Button(frame, text="Get Queue", command=get_queue)
get_queue_button.pack(side=tk.LEFT)


textbox = tk.Label(root, fg="green")
textbox.pack(side=tk.BOTTOM)

e = tk.Entry(root)
e.pack(side=tk.BOTTOM)

root.mainloop()
