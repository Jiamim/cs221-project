#!/usr/bin/env python

import os
import time

# Device: Pipe/0/ppl

PRESS_DELAY = 0.02
TILT_DELAY = 0.02

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
def C_UP(): up('C')
def C_DOWN(): down('C')
def C_LEFT(): left('C')
def C_RIGHT(): right('C')
##### End ######

def up(stick): tilt(stick, .5, 1)
def down(stick): tilt(stick, .5, 0)
def left(stick): tilt(stick, 0, .5)
def right(stick): tilt(stick, 1, .5)

def press(button):
  PIPE.write('PRESS %s\n' % button)
  PIPE.flush()
  time.sleep(PRESS_DELAY)
  PIPE.write('RELEASE %s\n' % button)
  PIPE.flush()
  time.sleep(PRESS_DELAY)

def tilt(stick, x, y):
  PIPE.write('SET %s %.1f %.1f\n' % (stick, x, y))
  PIPE.flush()
  time.sleep(TILT_DELAY)
  PIPE.write('SET %s .5 .5\n' % stick)
  PIPE.flush()
  time.sleep(TILT_DELAY)

def shutdown():
  PIPE.close()
  print '[controller.py] Closed named pipe writer.'


def test():
  initialize()
  A()
  shutdown()

if __name__ == '__main__':
  test()
