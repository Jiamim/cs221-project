#!/usr/bin/env python

import os
import time

import controller
import cv2

# Graphics Settings
# - Auto adjust Window Size
# - 1x Native (640 x 528)
# Hotkey Settings
# - Device: Pipe/0/ppl
# - Screenshot: D_DOWN

SCREENSHOT_DIR = os.path.expanduser('~/Library/Application Support/Dolphin/ScreenShots/NANE01')
FILENAME = os.path.join(SCREENSHOT_DIR, 'NANE01-1.png')
SCREENSHOT_WAIT = .25

SCREENSHOT_SIZE = (716, 1280, 3)

def initialize():
  pass

# Returns OpenCV image. None if a screenshot wasn't taken quickly enough.
def takeScreenshot():
  if os.path.exists(FILENAME): os.remove(FILENAME)
  controller.C_DOWN()
  time.sleep(SCREENSHOT_WAIT)
  img = cv2.imread(FILENAME)
  if img != None:
    assert img.shape == SCREENSHOT_SIZE
  return img

# Utility function to read a screenshot, without taking one or deleting anything
def readScreenshot(filename=FILENAME):
  img = cv2.imread(filename)
  assert img.shape == SCREENSHOT_SIZE
  return img

def shutdown():
  pass



def test():
  controller.initialize()
  takeScreenshot()
  controller.shutdown()

if __name__ == '__main__':
  initialize()
  test()
  shutdown()
