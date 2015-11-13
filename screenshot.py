#!/usr/bin/env python

#!/usr/bin/env python

from common import *
import sys
import time

import cv2
import win32con
import win32gui
import win32ui

HANDLE = None
SRC_DC = None
DC_OBJ = None
DST_DC = None
BMP = None

# Obtain bits from window. Upon experimenting, it is fastest to save the .bmp
# file and read it back via OpenCV.
def takeScreenshot():
  DST_DC.BitBlt((0, 0), (WINDOW_WIDTH, WINDOW_HEIGHT), DC_OBJ, (0, 0), win32con.SRCCOPY)
  BMP.SaveBitmapFile(DST_DC, SCREENSHOT_FILE)
  image = cv2.imread(SCREENSHOT_FILE)
  if image.shape != (WINDOW_HEIGHT, WINDOW_WIDTH, 3):
    print '[screenshot.py] ERROR: Set Project64 resolution to be 800x600'
    sys.exit(1)
  return image

# Get window handle to emulator screen and prepare bitmap buffer.
def initialize():
  global HANDLE, SRC_DC, DC_OBJ, DST_DC, BMP

  HANDLE = win32gui.FindWindow(None, WINDOW_NAME)
  if HANDLE == 0 or HANDLE == None:
    print '[screenshot.py] ERROR: Could not locate emulator window.'
    sys.exit(1)

  print '[screenshot.py] Obtaining window handle and preparing bitmap.'
  SRC_DC = win32gui.GetDC(HANDLE)
  DC_OBJ = win32ui.CreateDCFromHandle(SRC_DC)
  DST_DC = DC_OBJ.CreateCompatibleDC()
  BMP = win32ui.CreateBitmap()
  BMP.CreateCompatibleBitmap(DC_OBJ, WINDOW_WIDTH, WINDOW_HEIGHT)
  DST_DC.SelectObject(BMP)

# Release all handles.
def shutdown():
  if DC_OBJ != None:
    DC_OBJ.DeleteDC()
  if DST_DC != None:
    DST_DC.DeleteDC()
  if SRC_DC != None:
    win32gui.ReleaseDC(HANDLE, SRC_DC)
  if BMP != None:
    win32gui.DeleteObject(BMP.GetHandle())
  print '[screenshot.py] Shutdown successful.'


def test():
  takeScreenshot()

def foo(hwnd, unused):
  s = win32gui.GetWindowText(hwnd)
  if s != '':
    print s

if __name__ == '__main__':
  win32gui.EnumWindows(foo, None)
  initialize()
  test()
  shutdown()
