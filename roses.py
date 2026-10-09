from tkinter import *

root = Tk()
canvas = Canvas(root, width=640, height=350, bg="black")
canvas.pack()

canvas.create_rectangle(320, 175, 321, 176, fill="white", outline="")
root.mainloop()
