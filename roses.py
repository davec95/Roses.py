from tkinter import *
import random

WIDTH = 640
HEIGHT = 350

SCALE = 9.5
CX = 320
CY = 223

# Approximate EGA colors 8..15
COLORS = [
    "#555555",  # 8
    "#5555ff",  # 9
    "#55ff55",  # 10
    "#55ffff",  # 11
    "#ff5555",  # 12
    "#ff55ff",  # 13
    "#ffff55",  # 14
    "#ffffff",  # 15
]

root = Tk()
root.title("8-Particle Rose Attractor")

canvas = Canvas(root, width=WIDTH, height=HEIGHT,
                bg="black", highlightthickness=0)
canvas.pack()

a = random.uniform(-1.0, 1.0)
b = 1.0 - a

print("a =", a)
print("b =", b)

particles = []

for i in range(8):
    t = 2 * i - 0.51

    x = t
    y = t
    c = 2 * b * x * x / (1 + x * x)

    particles.append([x, y, c, COLORS[i]])


def iterate():
    global particles

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
                canvas.create_line(px, py, px + 1, py,
                                   fill=color)

    root.after(1, iterate)

iterate()
root.mainloop()
