#!/usr/bin/env python

import os
import time

# Device: Pipe/0/ppl

PRESS_DELAY = 0.025
TILT_DELAY = 0.05
HOLD_DELAY = 0.8

NAMED_PIPE = os.path.expanduser('~/Library/Application Support/Dolphin/Pipes/ppl')
PIPE = None

def initialize():
  global PIPE
  print '[controller.py] Initializing named pipe writer...'
  if not os.path.exists(NAMED_PIPE):
    os.mkfifo(NAMED_PIPE)
  PIPE = open(NAMED_PIPE, 'w')

##### Call these #####
def A(): press('A')
def B(): press('B')
def X(): press('X')
def Y(): press('Y')
def Z(): press('Z')
def START(): press('START')
def L(): press('L')
def R(): press('R')
def D_UP(): press('D_UP')
def D_DOWN(): press('D_DOWN')
def D_RIGHT(): press('D_RIGHT')
def D_LEFT(): press('D_LEFT')
def MAIN_UP(): up('MAIN')
def MAIN_DOWN(): down('MAIN')
def MAIN_LEFT(): left('MAIN')
def MAIN_RIGHT(): right('MAIN')
def UP(): MAIN_UP()
def DOWN(): MAIN_DOWN()
def LEFT(): MAIN_LEFT()
def RIGHT(): MAIN_RIGHT()
def C_UP(): up('C')
def C_DOWN(): down('C')
def C_LEFT(): left('C')
def C_RIGHT(): right('C')

def MASH_UP(): up('MAIN', .35)
def MASH_DOWN(): down('MAIN', .35)
def MASH_RIGHT(): right('MAIN', .25)
def MASH_LEFT(): left('MAIN', .25)
##### End ######

def up(stick, delay=TILT_DELAY): tilt(stick, .5, 1, delay)
def down(stick, delay=TILT_DELAY): tilt(stick, .5, 0, delay)
def left(stick, delay=TILT_DELAY): tilt(stick, 0, .5, delay)
def right(stick, delay=TILT_DELAY): tilt(stick, 1, .5, delay)

def press(button):
  PIPE.write('PRESS %s\n' % button)
  PIPE.flush()
  time.sleep(PRESS_DELAY)
  PIPE.write('RELEASE %s\n' % button)
  PIPE.flush()
  time.sleep(PRESS_DELAY)

def tilt(stick, x, y, delay=TILT_DELAY):
  PIPE.write('SET %s %.1f %.1f\n' % (stick, x, y))
  PIPE.flush()
  time.sleep(delay)
  PIPE.write('SET %s .5 .5\n' % stick)
  PIPE.flush()
  if delay == TILT_DELAY:
    time.sleep(delay)

def holdR():
  PIPE.write('PRESS R\n')
  PIPE.flush()
  time.sleep(HOLD_DELAY)
  PIPE.write('RELEASE R\n')
  PIPE.flush()
  time.sleep(HOLD_DELAY)

def shutdown():
  PIPE.close()
  print '[controller.py] Closed named pipe writer.'


def test():
  initialize()
  START()
  shutdown()

if __name__ == '__main__':
  test()
