from tkinter import *
import random

WIDTH = 1280
HEIGHT = 700

SCALE = 9.5

# Doubled from original (320,223)
CX = 640
CY = 446

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

canvas = Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg="black",
    highlightthickness=0
)
canvas.pack()

particles = []
a = 0
b = 0


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

            px = int(SCALE * xp + CX)
            py = int(SCALE * yp + CY)

            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                canvas.create_line(
                    px, py,
                    px + 1, py,
                    fill=color
                )

    root.after(1, iterate)


root.bind("<space>", restart)

restart()
iterate()

root.mainloop()
