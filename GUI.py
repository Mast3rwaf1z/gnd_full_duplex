import tkinter as tk

import full_duplex as fd

BBH:fd.dualBB_handler = None

def exec_fd():
    BBH = fd.dualBB_handler()
    txThread = fd.tx_thread(BBH)
    rxThread = fd.rx_thread(BBH)

def queue():
    if BBH is not None:
        BBH.tq.put(e.get())
        print(BBH.tq.size)

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

button = tk.Button(frame, 
                   text="QUIT", 
                   fg="red",
                   command=quit)
button.pack(side=tk.LEFT)
exec_button = tk.Button(frame,
                   text="exec full-duplex",
                   command=exec_fd)
exec_button.pack(side=tk.LEFT)

queue_button = tk.Button(frame, text="queue", command=queue)
queue_button.pack(side=tk.LEFT)

e = tk.Entry(root)
e.pack(side=tk.BOTTOM)

root.mainloop()
