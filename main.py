import time
import pyautogui as ctr
import cv2 as cv
import threading
import logging

from pyautogui import keyDown, keyUp, moveRel
from functools import partial

SCREEN_WIDTH, SCREEN_HEIGHT = ctr.size()

DIRS = {
    'forward': 'w',
    'left': 'a',
    'back': 's',
    'right': 'd'
}


ANGLES = {
    'H': {
        'right': 1,
        'left': -1
    },
    'V': {
        'up': -1,
        'down': 1
    },
}


def move(dir: str, dur=1) -> None:
    keyDown(DIRS[dir])
    logging.info('key pressed')
    time.sleep(dur)
    keyUp(DIRS[dir])
    logging.info('key released')


def move_mouse(dir, dist=100, dur=1):
    x_offset = (dir in ANGLES['H']) * dist * ANGLES['H'][dir] if dir in ANGLES['H'] else 0
    y_offset = ((dir in ANGLES['V']) * dist * ANGLES['V'][dir]) if dir in ANGLES['V'] else 0
    moveRel(
        x_offset,
        y_offset,
        dur
    )


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


def main():
    while True:
        cmd = input('Enter a command: ')
        if cmd in COMMANDS:
            threading.Thread(target=COMMANDS[cmd]).start()
        else:
            print(f"No such command.\n{COMMANDS.keys()}")



if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    main()