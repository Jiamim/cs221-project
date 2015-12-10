#!/usr/bin/env python

## Runs the main program.

import board
import brain
import controller
import emulator
import screenshot

def initializeAll():
  controller.initialize()
  screenshot.initialize()
  emulator.initialize()

def shutdownAll():
  emulator.shutdown()
  screenshot.shutdown()
  controller.shutdown()


def main():
  initializeAll()
  print '[main.py] Running main program...'
  ai = brain.BaselineBrain()
  emulator.run(ai)
  print '[main.py] Main program done.'


if __name__ == '__main__':
  main()
