#!/usr/bin/env python

## Learning for various square types

import os
import sys

# import cv2
import numpy as np

import board
import emulator

samples = np.empty((0, NUM_PIXELS))
responses = []

def main():
  global samples, responses

  print '[train.py] Be careful about running this!'
  sys.exit(0)

  # trainEndGameDetection()
  # return

  # Training
  for screenshot in getScreenshots():
    train(screenshot)

  # Remove previous training data and save new one
  # for filename in os.listdir(DATA_FOLDER):
  #   if filename.endswith('data'):
  #     os.remove(os.path.join(DATA_FOLDER, filename))
  # np.savetxt(os.path.join(DATA_FOLDER, 'samples.data'), samples)
  # np.savetxt(os.path.join(DATA_FOLDER, 'responses.data'), responses)
  print '** Training complete **'


def trainEndGameDetection():
  sample = np.empty((0, NUM_BOARD_PIXELS))
  img = cv2.imread(os.path.join(DATA_FOLDER, 'snapENDGAME.jpg'))
  img = emulator.cropBoardFromScreenshot(img)
  img = cv2.resize(img, BOARD_SIZE)
  img = img.reshape((1, NUM_BOARD_PIXELS))
  responses.append(1)
  sample = np.append(sample, img, 0)

  img = cv2.imread(os.path.join(DATA_FOLDER, 'snapENDGAME_False.jpg'))
  img = emulator.cropBoardFromScreenshot(img)
  img = cv2.resize(img, BOARD_SIZE)
  img = img.reshape((1, NUM_BOARD_PIXELS))
  responses.append(0)
  sample = np.append(sample, img, 0)
  np.savetxt(os.path.join(DATA_FOLDER, 'sampleEND.data'), sample)
  np.savetxt(os.path.join(DATA_FOLDER, 'responseEND.data'), responses)


def train(screenshot):
  global samples, responses

  boardImg = emulator.cropBoardFromScreenshot(screenshot)
  for square, rowIndex, colIndex in emulator.parseSquaresFromBoard(boardImg):
    cv2.imshow('%d, %d' % (colIndex, rowIndex), square)
    # Enter the key corresponding to the board enums
    key = cv2.waitKey(0)
    if key == 27: sys.exit()
    val = int(chr(key))
    printVal(val)
    cv2.destroyAllWindows()
    if val == board.CLEAR or val == board.EMPTY or val == board.DEAD: continue

    # Add to training data
    square = cv2.resize(square, SQUARE_SIZE)
    square = square.reshape((1, NUM_PIXELS))
    responses.append(val)
    samples = np.append(samples, square, 0)


# Helper to make sure training is accurate.
def printVal(val):
  print {1:'Fire', 2:'Grass', 3:'Water', 4:'Heart', 5:'Electric',
         6:'Pokeball', 7:'CLEAR', 8:'DEAD', 0:'EMPTY'}[val]


# Iterate through all screenshots in data directory.
def getScreenshots():
  for filename in os.listdir(DATA_FOLDER):
    if SCREENSHOT_PREFIX in filename:
      # Read in image.
      img = cv2.imread(os.path.join(DATA_FOLDER, filename))
      if img.shape != (600, 800, 3):
        print 'ERROR: Set Project64 resolution to be 800x600'
        sys.exit(1)
      yield img


if __name__ == '__main__':
  main()
