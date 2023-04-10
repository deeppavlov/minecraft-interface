import time
import threading
import logging
import pyautogui as ctr
import pygetwindow as gw
import copy
import cv2 as cv

from pyautogui import keyDown, keyUp, click
from functools import partial
from utils.interception import *

SCREEN_WIDTH, SCREEN_HEIGHT = ctr.size()
GAME_WINDOW = None

RUNNING = True
TIMEOUT = 2500 # ms

inter = interception()
inter.set_filter(interception.is_mouse, interception_filter_mouse_state.INTERCEPTION_FILTER_MOUSE_ALL.value)
device = inter.wait()
BASELINE_STROKE = inter.receive(device)


# TODO: get device without moving


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


def init_stroke():
    return copy.deepcopy(BASELINE_STROKE)


def move(dir: str, dur=1) -> None:
    keyDown(DIRS[dir])
    time.sleep(dur)
    keyUp(DIRS[dir])


def move_mouse_native(x, y):
    stroke = init_stroke()
    for i in range(25):
        stroke.x += 1 if x > 0 else -1 if x < 0 else 0
        stroke.y += 1 if y > 0 else -1 if y < 0 else 0
        inter.send(device, stroke)
        time.sleep(2/100)
        print(f'{i+1}/100')


def move_mouse(dir, dist=100, dur=1):
    x_offset = ((dir in MOUSE_DIRS['H']) * dist * MOUSE_DIRS['H'][dir]) if dir in MOUSE_DIRS['H'] else 0
    y_offset = ((dir in MOUSE_DIRS['V']) * dist * MOUSE_DIRS['V'][dir]) if dir in MOUSE_DIRS['V'] else 0
    threading.Thread(target=move_mouse_native(x_offset, y_offset)).start()
    


COMMANDS = {
    'move forward': partial(move, dir='forward'),
    'move left': partial(move, dir='left'),
    'move back': partial(move, dir='back'),
    'move right': partial(move, dir='right'),
    'face up': partial(move_mouse, dir='up'),
    'face left': partial(move_mouse, dir='left'),
    'face down': partial(move_mouse, dir='down'),
    'face right': partial(move_mouse, dir='right'),
}


mouse_x, mouse_y = ctr.position()


def main(): # F3 + P in game to disable unfocus autopause
    while True:
        cmd = input('Enter a command: ')
        if cmd in COMMANDS:
            GAME_WINDOW.minimize()
            GAME_WINDOW.maximize()
            click(GAME_WINDOW.center)
            threading.Thread(target=COMMANDS[cmd]).start()
        else:
            print(f"No such command.\n{COMMANDS.keys()}")



if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    windows = gw.getAllTitles()
    logging.info(f'Windows: {windows}')

    try:
        game_window = list(filter(lambda x: x.find('Minecraft') != -1, windows))[0]
        logging.info(f"Game window: {game_window}")

        GAME_WINDOW = gw.getWindowsWithTitle(game_window)[0]
    except:
        raise Exception("Minecraft is not running. Exiting program.")

    main()