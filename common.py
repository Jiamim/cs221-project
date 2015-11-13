#!/usr/bin/env python

import os
import sys

import cv2

DATA_FOLDER = 'data'
SCREENSHOT_DIR = 'tmp'
SCREENSHOT_FILE = os.path.join(SCREENSHOT_DIR, 'tmp.bmp')
WINDOW_NAME = 'PUZZLE LEAGUE N64 - Project64 Version 1.6'
WINDOW_NAME2 = 'Project64 Version 1.6'

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

SCREENSHOT_DELAY_SECS = 0.5

# Interface
KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT = range(4)

BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT = 62, 84, 330 - 62, 558 - 84
SQUARE_HEIGHT, SQUARE_WIDTH = 40, 33
GRID_XS = [(0, 33), (43, 78), (88, 123), (133, 168), (178, 213), (223, 258)]

SQUARE_SIZE = (15, 15)
NUM_PIXELS = SQUARE_SIZE[0] * SQUARE_SIZE[1] * 3

BOARD_SIZE = (40, 40)
NUM_BOARD_PIXELS = BOARD_SIZE[0] * BOARD_SIZE[1] * 3

# Utility function.
def debug_showImage(img, title='image'):
  cv2.imshow(title, img)
  key = cv2.waitKey(0)
  cv2.destroyAllWindows()
  if key == 27:
    sys.exit(0)
