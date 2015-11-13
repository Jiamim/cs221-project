#!/usr/bin/env python

import ctypes
import time

GRANULARITY = 10
MOVE_DELAY_SECS = 0.25

# Right click
def A(log=False):
  if log: __log('A')
  ctypes.windll.user32.mouse_event(0x08, 0, 0, 0, 0)
  time.sleep(0.10)    # Delay in between to register click
  ctypes.windll.user32.mouse_event(0x10, 0, 0, 0, 0)
  __delay()

# Move mouse right.
def RIGHT(log=False):
  if log: __log('RIGHT')
  ctypes.windll.user32.mouse_event(0x01, GRANULARITY, 0, 0, 0)
  __delay()

# Move mouse left.
def LEFT(log=False):
  if log: __log('LEFT')
  ctypes.windll.user32.mouse_event(0x01, -GRANULARITY, 0, 0, 0)
  __delay()

# Move mouse up.
def UP(log=False):
  if log: __log('UP')
  ctypes.windll.user32.mouse_event(0x01, 0, -GRANULARITY, 0, 0)
  __delay()

# Move mouse down.
def DOWN(log=False):
  if log: __log('DOWN')
  ctypes.windll.user32.mouse_event(0x01, 0, GRANULARITY, 0, 0)
  __delay()

# Prevent mouse input from overloading P64.
def __delay():
  time.sleep(MOVE_DELAY_SECS)

# Log move.
def __log(str):
  print '[keyboard.py] %s' % str


if __name__ =="__main__":
  pass
