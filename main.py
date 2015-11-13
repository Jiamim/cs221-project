#!/usr/bin/env python

## Runs the main program.

## CONFIGURATION NEEDED
# Set Project64 emulation resolution to 800x600
# Set screenshot save directory to be cs221-project/tmp/
# Do not change any ROM names

import board
import brain
import emulator
import screenshot

def initializeAll():
  screenshot.initialize()
  emulator.initialize()

def shutdownAll():
  emulator.shutdown()
  screenshot.shutdown()


def main():
  initializeAll()
  print '[main.py] Running main program...'
  ai = brain.BaselineBrain()
  emulator.run(ai)
  print '[main.py] Main program done.'


if __name__ == '__main__':
  main()
