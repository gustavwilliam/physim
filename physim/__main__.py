import os

from pynput import keyboard

from models.objects import Object
from physim.models.canvas import Canvas

GRAVITY = [0, 0.03]
GROUND_HEIGHT = 3
TERMINAL_SIZE = os.get_terminal_size()
HEIGHT = TERMINAL_SIZE.lines - 1
WIDTH = TERMINAL_SIZE.columns

canvas = Canvas(width=WIDTH, height=HEIGHT, g=GRAVITY)
ground = Object(
    name="Ground",
    width=WIDTH,
    height=GROUND_HEIGHT,
    position=[0, HEIGHT - GROUND_HEIGHT],
    friction_coeff=7,
)
player = Object(
    name="Player",
    width=3,
    height=2,
    movable=True,
    gravity=True,
    position=[10, 1],
    user_input=True,
)
obstacle = Object(
    name="Obstacle",
    width=30,
    height=4,
    friction_coeff=20,
    position=[WIDTH - 50, HEIGHT - GROUND_HEIGHT - 5],
    texture="▚",
)

canvas.add_objects(obstacle, ground, player)
listener = keyboard.Listener(on_press=canvas.handle_key_press)

if __name__ == "__main__":
    listener.start()
    canvas.render_loop()
