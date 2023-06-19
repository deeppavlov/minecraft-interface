import time
import threading
import logging
import pyautogui as ctr
import pygetwindow as gw
import copy

from pyautogui import keyDown, keyUp, click
from functools import partial
from utils.interception import *

RUNNING = True
TIMEOUT = 2500 # ms

inter = interception()
inter.set_filter(interception.is_mouse, interception_filter_mouse_state.INTERCEPTION_FILTER_MOUSE_ALL.value)

# TODO: get device without moving
SCREEN_WIDTH, SCREEN_HEIGHT = ctr.size()

DIRS = {
    'forward': 'w',
    'left': 'a',
    'back': 's',
    'right': 'd'
}


MOUSE_DIRS = {
    'H': {
        'right': 1,
        'left': -1
    },
    'V': {
        'up': -1,
        'down': 1
    },
}


class interception_data():
    def __init__(self, device, window, BASELINE_STROKE) -> None:
        self.device = device
        self.window = window
        self.BASELINE_STROKE = BASELINE_STROKE


def init_stroke(idata: interception_data):
    return copy.deepcopy(idata.BASELINE_STROKE)


def move(dir: str, dur=1) -> None:
    keyDown(DIRS[dir])
    time.sleep(dur)
    keyUp(DIRS[dir])


def move_mouse_native(x: int, y: int):
    stroke = init_stroke()
    for i in range(25):
        stroke.x += 1 if x > 0 else -1 if x < 0 else 0
        stroke.y += 1 if y > 0 else -1 if y < 0 else 0
        inter.send(device, stroke)
        time.sleep(2 / 100)
        print(f'{i + 1}/100')


def move_mouse(dir: str, dist=100, dur=1):
    x_offset = ((dir in MOUSE_DIRS['H']) * dist * MOUSE_DIRS['H'][dir]) if dir in MOUSE_DIRS['H'] else 0
    y_offset = ((dir in MOUSE_DIRS['V']) * dist * MOUSE_DIRS['V'][dir]) if dir in MOUSE_DIRS['V'] else 0
    threading.Thread(target=move_mouse_native(x_offset, y_offset)).start()


COMMANDS = {
    'move_forward': partial(move, dir='forward'),
    'move_left': partial(move, dir='left'),
    'move_back': partial(move, dir='back'),
    'move_right': partial(move, dir='right'),
    'face_up': partial(move_mouse, dir='up'),
    'face_left': partial(move_mouse, dir='left'),
    'face_down': partial(move_mouse, dir='down'),
    'face_right': partial(move_mouse, dir='right'),
}


mouse_x, mouse_y = ctr.position()


def focus(window):
    window.activate()
    # window.minimize()
    # window.maximize()
    # click(window.center)


def execute(idata: interception_data, cmd: str):
    for command in COMMANDS:
        if command in cmd:
            cmd = command
            break
    if cmd in COMMANDS:
        focus(idata.window)
        threading.Thread(target=COMMANDS[cmd]).start()
    else:
        print(f"No such command - {cmd}.\n{COMMANDS.keys()}")


def prepare_game():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    print('MOVE YOUR MOUSE SO THAT THE PROGRAM CAN INTERCEPT IT')
    device = None #inter.wait()
    print('MOUSE INTERCEPTED SUCCESSFULLY')

    BASELINE_STROKE = None #inter.receive(device)

    windows = gw.getAllTitles()
    logging.info(f'Windows: {windows}')

    try:
        game_window = list(filter(lambda x: x.find('Minecraft') != -1, windows))[0]
        logging.info(f"Game window: {game_window}")
        GAME_WINDOW = gw.getWindowsWithTitle(game_window)[0]
    except Exception:
        raise Exception("Minecraft is not running. Exiting program.")

    focus(GAME_WINDOW)

    return device, GAME_WINDOW, BASELINE_STROKE

    # disable unfocuse autopause in minecraft
    # keyDown('f3')
    # keyDown('p')
    # keyUp('f3')
    # keyUp('p')
    #----------------------------------------
