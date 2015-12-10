#!/usr/bin/env python

import os
import time

import controller

# Graphics Settings
# - Auto adjust Window Size
# - 1x Native (640 x 528)
# Hotkey Settings
# - Device: Pipe/0/ppl
# - Screenshot: D_DOWN

SCREENSHOT_DIR = os.path.expanduser('~/Library/Application Support/Dolphin/ScreenShots/NANE01')
FILENAME = os.path.join(SCREENSHOT_DIR, 'NANE01-1.png')
SCREENSHOT_WAIT = .2

def initialize():
  pass

# Returns OpenCV image
def takeScreenshot():
  controller.D_DOWN()
  time.sleep(SCREENSHOT_WAIT)
  assert os.path.exists(FILENAME)
  os.remove(FILENAME)

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
