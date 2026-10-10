from tkinter import *
import random

WINDOW_W = 1280
WINDOW_H = 700

WIDTH = WINDOW_W
HEIGHT = WINDOW_H

fullscreen = False

SCALE = 9.5

COLORS = [
    "#555555",  # EGA 8
    "#5555ff",  # EGA 9
    "#55ff55",  # EGA 10
    "#55ffff",  # EGA 11
    "#ff5555",  # EGA 12
    "#ff55ff",  # EGA 13
    "#ffff55",  # EGA 14
    "#ffffff",  # EGA 15
]

root = Tk()
root.title("8-Particle Rose Attractor")

SCREEN_W = root.winfo_screenwidth()
SCREEN_H = root.winfo_screenheight()

canvas = Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="black",
    highlightthickness=0
)
canvas.pack()

cx = canvas.winfo_width() // 2
cy = canvas.winfo_height() // 2

particles = []
a = 0
b = 0

def quit_program(event=None):
    root.destroy()

def resize_canvas(w, h):
    canvas.config(width=w, height=h)

def toggle_fullscreen(event=None):
    global fullscreen

    fullscreen = not fullscreen

    if fullscreen:
        root.attributes("-fullscreen", True)
        resize_canvas(SCREEN_W, SCREEN_H)
    else:
        root.attributes("-fullscreen", False)
        resize_canvas(WINDOW_W, WINDOW_H)

def escape_fullscreen(event=None):
    global fullscreen

    fullscreen = False
    root.attributes("-fullscreen", False)
    resize_canvas(WINDOW_W, WINDOW_H)
    
def restart(event=None):
    global particles, a, b

    canvas.delete("all")

    a = random.uniform(-1.0, 1.0)
    b = 1.0 - a

    print(f"a = {a:.6f}    b = {b:.6f}")

    particles = []

    for i in range(8):
        t = 2 * i - 0.51

        x = t
        y = t

        c = 2 * b * x * x / (1 + x * x)

        particles.append([x, y, c, COLORS[i]])

def iterate():
    for _ in range(500):

        for p in particles:
            x, y, c, color = p

            xp = a * x + y + c
            cp = 2 * b * xp * xp / (1 + xp * xp)
            yp = a * xp - x + cp

            p[0] = xp
            p[1] = yp
            p[2] = cp

            px = int(SCALE * xp + cx)
            py = int(SCALE * yp + cy)

            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                canvas.create_line(
                    px, py,
                    px + 1, py,
                    fill=color
                )

    root.after(1, iterate)


root.bind("<space>", restart)
root.bind("q", quit_program)
root.bind("<Return>", toggle_fullscreen)

restart()
iterate()

root.mainloop()
