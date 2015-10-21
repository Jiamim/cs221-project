#!/usr/bin/env python

DATA_FOLDER = 'data'
SCREENSHOT_DIR = 'tmp'
SCREENSHOT_PREFIX = 'Pokemon Puzzle League (U)  snap'
WINDOW_NAME = 'PUZZLE LEAGUE n64 - Project64 Version 1.6'

# Time to wait after F3 has been pressed before looking for the screenshot.
SCREENSHOT_DELAY_SECS = 0.5
MOVE_DELAY_SECS = 0.5

BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT = 62, 84, 330 - 62, 558 - 84
SQUARE_HEIGHT, SQUARE_WIDTH = 40, 33
GRID_XS = [(0, 33), (43, 78), (88, 123), (133, 168), (178, 213), (223, 258)]

# Interface
KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT = range(4)

SQUARE_SIZE = (15, 15)
NUM_PIXELS = SQUARE_SIZE[0] * SQUARE_SIZE[1] * 3

BOARD_SIZE = (40, 40)
NUM_BOARD_PIXELS = BOARD_SIZE[0] * BOARD_SIZE[1] * 3
