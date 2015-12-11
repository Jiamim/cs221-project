#!/usr/bin/env python

## Learning for various square types

import os
import sys

import cv2
import numpy as np

import board
import imgUtils
import screenshot

DATA_FOLDER = 'data'

TRAIN1_DATA = \
  [3, 4, 4, 3, 1, 5,
   1, 3, 1, 6, 6, 4,
   2, 2, 5, 3, 1, 5,
   3, 4, 4, 2, 4, 3,
   1, 1, 6, 5, 1, 4,
   3, 5, 4, 6, 6, 2,
   1, 1, 4, 4, 2, 3,
   2, 2, 3, 4, 2, 1,
   4, 1, 3, 3, 5, 3,
   4, 2, 5, 0, 6, 4,
   8, 8, 8, 8, 8, 8,
   0, 0, 0, 0, 0, 0]

def main():
  print '[train.py] Be careful about running this!'

  # trainEndGameDetection()
  # return

  # Training
  train(screenshot.readScreenshot(os.path.join(DATA_FOLDER, 'train1.png')))
  print '** Training complete **'

# Helper to make sure training is accurate.
def printVal(val):
  print {1:'Fire', 2:'Grass', 3:'Water', 4:'Heart', 5:'Electric',
         6:'Pokeball', 7:'CLEAR', 8:'DEAD', 0:'EMPTY'}[val]


SAMPLES_FILE = os.path.join(DATA_FOLDER, 'samplesColors.data')
RESPONSES_FILE = os.path.join(DATA_FOLDER, 'responsesColors.data')

def train(screenshot):
  # for filename in os.listdir(DATA_FOLDER):
  #   if filename.endswith('data'):
  #     os.remove(os.path.join(DATA_FOLDER, filename))

  if (os.path.exists(SAMPLES_FILE)):
    samples = np.loadtxt(SAMPLES_FILE)
    responses = [int(i) for i in np.loadtxt(RESPONSES_FILE)]
  else:
    samples = np.empty((0, imgUtils.FEATURE_VECTOR_SIZE))
    responses = []

  grid = imgUtils.cropBoard2Player(screenshot)

  index = 0
  for square, rowIndex, colIndex in imgUtils.parseSquaresFromBoard(grid):
    # cv2.imshow('%d, %d' % (colIndex, rowIndex), square)
    # # Enter the key corresponding to the board enums
    # key = cv2.waitKey(0)
    # if key == 27: break
    # val = int(chr(key))
    # printVal(val)
    # cv2.destroyAllWindows()
    val = TRAIN1_DATA[index]
    index += 1
    if val == board.CLEAR or val == board.EMPTY or val == board.DEAD: continue

    # Add to training data
    feature_vec = imgUtils.squareFeatureVector(square)
    responses.append(val)
    samples = np.append(samples, feature_vec, 0)

  np.savetxt(SAMPLES_FILE, samples)
  np.savetxt(RESPONSES_FILE, responses)



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



if __name__ == '__main__':
  main()
