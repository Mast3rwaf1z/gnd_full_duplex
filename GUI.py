import tkinter as tk

import full_duplex as fd

BBH:fd.dualBB_handler = None
def exec_fd():
    try:
        BBH = fd.dualBB_handler()
        txThread = fd.tx_thread(BBH)
        rxThread = fd.rx_thread(BBH)
        textbox.config(text="successfully initialized full duplex", fg="green")
    except Exception as ex:
        textbox.config(text="failed to initialize full duplex, is two blueboxes plugged in and initialized correctly?", fg="red")
        print(e)

def queue():
    if BBH is not None:
        BBH.tq.put(e.get())
        print(BBH.tq.size)
        textbox.config(text="successfully queued item", fg="red")
    else:
        textbox.config(text="failed to queue item, is BBH initialized?", fg="red")

def get_queue():
    if BBH is not None:
        print(BBH.tq.items)
        textbox.config(text="successfully got queue", fg="green")
    else:
        textbox.config(text="failed to get queue, is BBH initialized?", fg="red")

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

queue_button = tk.Button(frame, text="queue", command=queue)
queue_button.pack(side=tk.LEFT)

get_queue_button = tk.Button(frame, text="Get Queue", command=get_queue)
get_queue_button.pack(side=tk.BOTTOM)

textbox = tk.Label(root, fg="green")
textbox.pack(side=tk.BOTTOM)

e = tk.Entry(root)
e.pack(side=tk.BOTTOM)

root.mainloop()
