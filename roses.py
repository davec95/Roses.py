#!/usr/bin/env python3
"""
roses.py - Animated 8-particle rose attractor.

Steps 8 particles through the rose (Clifford-style) attractor
    x' = a*x + y + c
    c' = 2*b*x'^2 / (1 + x'^2)
    y' = a*x' - x + c'
and paints every point onto a numpy RGB framebuffer, blitted to
the screen as one bulk PhotoImage per tick (~2M points/sec).
Each particle draws in its own EGA palette color.

Controls:
    Space      next rose: replays the next buffered (a, b) pair,
               or picks a new random pair when the buffer is used up
    Backspace  previous rose: reuses the buffered (a, b) pair
    Enter      toggle fullscreen
    Escape     leave fullscreen
    q          quit

The last BUFFER_SIZE (a, b) pairs are remembered, so Backspace
revisits each rose exactly as it was first drawn.

Usage: ./roses.py   (or: python3 roses.py)
"""

from tkinter import *
import random
import numpy as np

WINDOW_W = 1280
WINDOW_H = 700
SCALE = 9.5

BUFFER_SIZE = 20

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

# Same colors as RGB triples for the numpy framebuffer
COLOR_RGB = np.array(
    [
        [int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)]
        for c in COLORS
    ],
    dtype=np.uint8
)

STEPS_PER_TICK = 20000

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
img_id = None
fb = None          # numpy RGB framebuffer, shape (h, w, 3)
fb_w = 0
fb_h = 0
particles = []
a = 0.0
b = 0.0
fullscreen = False

ab_buffer = []     # remembered (a, b) pairs, max BUFFER_SIZE entries
index = 0          # current position in ab_buffer


def blit():
    global photo, img_id

    ppm = (
        b"P6\n%d %d\n255\n" % (fb_w, fb_h)
        + fb.tobytes()
    )

    photo = PhotoImage(data=ppm)

    if img_id is None:
        img_id = canvas.create_image(
            0,
            0,
            image=photo,
            anchor=NW
        )
    else:
        canvas.itemconfig(img_id, image=photo)


def create_framebuffer(w, h):
    global fb, fb_w, fb_h, img_id

    canvas.delete("all")
    img_id = None

    fb_w = w
    fb_h = h
    fb = np.zeros((h, w, 3), dtype=np.uint8)

    canvas.config(width=w, height=h)

    blit()


def render():
    global particles

    root.title(
        f"Rose Attractor   #{index}   "
        f"a={a:.6f}   b={b:.6f}"
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
            [x, y, c]
        )


def next_rose(event=None):
    global index, a, b

    index += 1

    if index < len(ab_buffer):

        # a rose we have already seen: replay it exactly
        a, b = ab_buffer[index]

    else:

        a = random.uniform(-1.0, 1.0)
        b = 1.0 - a

        if index < BUFFER_SIZE:

            # room left in the buffer: remember this one
            ab_buffer.append(
                (a, b)
            )

        else:

            # buffer full: this rose is ephemeral,
            # park the index at the buffer edge
            index = BUFFER_SIZE

    render()


def back_rose(event=None):
    global index, a, b

    if index > 0:
        index -= 1

    # index is always < len(ab_buffer) here:
    # it can never go below 0, and the ephemeral
    # zone parks it at BUFFER_SIZE, one past the
    # last saved entry
    a, b = ab_buffer[index]

    render()


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

    render()


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

        render()


def quit_program(event=None):
    root.destroy()


def iterate():

    cx = fb_w // 2
    cy = fb_h // 2

    px_list = []
    py_list = []
    ci_list = []

    for _ in range(STEPS_PER_TICK):

        for j, p in enumerate(particles):

            x, y, c = p

            xp = a * x + y + c

            cp = (
                2 * b * xp * xp /
                (1 + xp * xp)
            )

            yp = a * xp - x + cp

            p[0] = xp
            p[1] = yp
            p[2] = cp

            px_list.append(int(SCALE * xp + cx))
            py_list.append(int(SCALE * yp + cy))
            ci_list.append(j)

    px = np.array(px_list, dtype=np.int64)
    py = np.array(py_list, dtype=np.int64)
    ci = np.array(ci_list, dtype=np.int64)

    inside = (
        (px >= 0) & (px < fb_w) &
        (py >= 0) & (py < fb_h)
    )

    # paint each particle's points in one fancy-index op
    for j in range(len(particles)):
        m = inside & (ci == j)
        if m.any():
            fb[py[m], px[m]] = COLOR_RGB[j]

    blit()

    # Force the canvas redraw now. With after(1) keeping the
    # event loop busy, Tk would otherwise never go idle and
    # the new PhotoImage would never reach the screen.
    root.update_idletasks()

    root.after(1, iterate)


root.bind("<space>", next_rose)
root.bind("<BackSpace>", back_rose)
root.bind("<Return>", toggle_fullscreen)
root.bind("<Escape>", escape_fullscreen)
root.bind("q", quit_program)

root.update()

create_framebuffer(
    WINDOW_W,
    WINDOW_H
)

# first rose: index 0, saved into the buffer
a = random.uniform(-1.0, 1.0)
b = 1.0 - a

ab_buffer.append(
    (a, b)
)

render()
iterate()

root.mainloop()
