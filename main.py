#!/usr/bin/env python

## Runs the main program.

import brain
import controller
import emulator
import imgUtils
import screenshot

def initializeAll():
  imgUtils.initialize()
  controller.initialize()
  screenshot.initialize()
  emulator.initialize()

def shutdownAll():
  emulator.shutdown()
  screenshot.shutdown()
  controller.shutdown()
  imgUtils.shutdown()


def main():
  initializeAll()
  print '[main.py] Running main program...'
  ai = brain.BaselineBrain()
  emulator.run(ai)
  print '[main.py] Main program done.'


if __name__ == '__main__':
  main()
