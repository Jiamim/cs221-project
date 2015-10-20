#!/usr/bin/env python

import sys
import time

import cv2
import win32con
import win32gui
import win32ui

WINDOW_NAME = 'PUZZLE LEAGUE n64 - Project64 Version 1.6'

HANDLE = None
SRC_DC = None
DC_OBJ = None
DST_DC = None
WIDTH = None
HEIGHT = None

def test():
  takeScreenshot()

def takeScreenshot():
  bmp = win32ui.CreateBitmap()
  bmp.CreateCompatibleBitmap(DC_OBJ, WIDTH, HEIGHT)
  DST_DC.SelectObject(bmp)
  DST_DC.BitBlt((0, 0), (WIDTH, HEIGHT), DC_OBJ, (0, 0), win32con.SRCCOPY)
  bmp.SaveBitmapFile(DST_DC, 'tmp/test.bmp')
  win32gui.DeleteObject(bmp.GetHandle())

def initialize():
  global HANDLE, SRC_DC, DC_OBJ, DST_DC, WIDTH, HEIGHT
  HANDLE = win32gui.FindWindow(None, WINDOW_NAME)
  if HANDLE == 0 or HANDLE == None:
    print 'ERROR: Could not locate emulator window.'
    sys.exit()
  SRC_DC = win32gui.GetDC(HANDLE)
  DC_OBJ = win32ui.CreateDCFromHandle(SRC_DC)
  DST_DC = DC_OBJ.CreateCompatibleDC()
  left, top, right, bottom = win32gui.GetClientRect(HANDLE)
  WIDTH = right - left
  HEIGHT = bottom - top

def shutdown():
  if DC_OBJ != None:
    DC_OBJ.DeleteDC()
  if DST_DC != None:
    DST_DC.DeleteDC()
  if SRC_DC != None:
    win32gui.ReleaseDC(HANDLE, SRC_DC)


if __name__ == '__main__':
  initialize()
  test()
  shutdown()
