from tkinter import *
import random

WINDOW_W = 1280
WINDOW_H = 700
SCALE = 9.5

COLORS = [
    "#555555",  # EGA 8
    "#5555ff",  # EGA 9
    "#55ff55",  # EGA 10
    "#55ffff",  # EGA 11
    "#ff5555",  # EGA 12
    "#ff55ff",  # EGA 13
    "#ffff55",  # EGA 14
    "#ffffff"   # EGA 15
]

root = Tk()
root.geometry(f"{WINDOW_W}x{WINDOW_H}")

SCREEN_W = root.winfo_screenwidth()
SCREEN_H = root.winfo_screenheight()

canvas = Canvas(
    root,
    bg="black",
    highlightthickness=0
)
canvas.pack(fill="both", expand=True)

photo = None
particles = []
a = 0.0
b = 0.0
fullscreen = False


def create_framebuffer(w, h):
    global photo

    canvas.delete("all")

    photo = PhotoImage(width=w, height=h)

    canvas.config(width=w, height=h)

    canvas.create_image(
        0,
        0,
        image=photo,
        anchor=NW
    )

    photo.put("black", to=(0, 0, w, h))


def plot(px, py, color):

    w = photo.width()
    h = photo.height()

    if 0 <= px < w and 0 <= py < h:
        photo.put(color, (px, py))


def restart(event=None):
    global particles, a, b

    a = random.uniform(-1.0, 1.0)
    b = 1.0 - a

    root.title(
        f"Rose Attractor   a={a:.6f}   b={b:.6f}"
    )

    create_framebuffer(
        canvas.winfo_width() or WINDOW_W,
        canvas.winfo_height() or WINDOW_H
    )

    particles = []

    for i in range(8):

        t = 2 * i - 0.51

        x = t
        y = t

        c = (
            2 * b * x * x /
            (1 + x * x)
        )

        particles.append(
            [x, y, c, COLORS[i]]
        )


def toggle_fullscreen(event=None):
    global fullscreen

    fullscreen = not fullscreen

    if fullscreen:

        root.attributes("-fullscreen", True)

        create_framebuffer(
            SCREEN_W,
            SCREEN_H
        )

    else:

        root.attributes("-fullscreen", False)

        root.geometry(
            f"{WINDOW_W}x{WINDOW_H}"
        )

        create_framebuffer(
            WINDOW_W,
            WINDOW_H
        )

    restart(None)


def escape_fullscreen(event=None):
    global fullscreen

    if fullscreen:

        fullscreen = False

        root.attributes(
            "-fullscreen",
            False
        )

        root.geometry(
            f"{WINDOW_W}x{WINDOW_H}"
        )

        create_framebuffer(
            WINDOW_W,
            WINDOW_H
        )

        restart(None)


def quit_program(event=None):
    root.destroy()


def iterate():

    w = photo.width()
    h = photo.height()

    cx = w // 2
    cy = h // 2

    batch = []

    for _ in range(5000):

        for p in particles:

            x, y, c, color = p

            xp = a * x + y + c

            cp = (
                2 * b * xp * xp /
                (1 + xp * xp)
            )

            yp = a * xp - x + cp

            p[0] = xp
            p[1] = yp
            p[2] = cp

            px = int(SCALE * xp + cx)
            py = int(SCALE * yp + cy)

            if 0 <= px < w and 0 <= py < h:
                batch.append(
                    (px, py, color)
                )

    for px, py, color in batch:
        photo.put(color, (px, py))

    root.after(1, iterate)


root.bind("<space>", restart)
root.bind("<Return>", toggle_fullscreen)
root.bind("<Escape>", escape_fullscreen)
root.bind("q", quit_program)

root.update()

create_framebuffer(
    WINDOW_W,
    WINDOW_H
)

restart()
iterate()

root.mainloop()
