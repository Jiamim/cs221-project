#!/usr/bin/env python

import os
import sys

import board
import cv2
import numpy as np
import train
from sklearn import linear_model

SQUARE_HEIGHT = 47.5

BOARD_TOP = 95
BOARD_BOTTOM = 665
BOARD_LEFT = 93
BOARD_RIGHT = 526

BOARD_HEIGHT = BOARD_BOTTOM - BOARD_TOP
BOARD_WIDTH = BOARD_RIGHT - BOARD_LEFT

MAX_ROWS = 12
NUM_COLS = 6

SQUARE_WIDTH = float(BOARD_WIDTH) / NUM_COLS
SQUARE_HEIGHT = float(BOARD_HEIGHT) / MAX_ROWS

SQUARE_RESHAPE_WIDTH = int(SQUARE_WIDTH)
SQUARE_RESHAPE_HEIGHT = int(SQUARE_HEIGHT)

NUM_PIXELS = SQUARE_RESHAPE_HEIGHT * SQUARE_RESHAPE_WIDTH * 3

COLOR = (0, 255, 0)

# Choose which model to use
MODEL_KNEAREST, MODEL_LOGREG = False, True
if MODEL_KNEAREST:
  MODEL = cv2.ml.KNearest_create()
  MODEL_ENDGAME = cv2.ml.KNearest_create()
elif MODEL_LOGREG:
  MODEL = linear_model.LogisticRegression(C=1e5)
  MODEL_ENDGAME = linear_model.LogisticRegression(C=1e5)

def initialize():
  print '[imgUtils.py] Training models...'
  samples = np.loadtxt(train.SAMPLES_FILE, np.float32)
  responses = np.loadtxt(train.RESPONSES_FILE, np.int32)
  responses = responses.reshape((responses.size, 1))

  # sample_end = np.loadtxt(os.path.join(DATA_FOLDER, 'sampleEND.data'),
  #                         np.float32)
  # response_end = np.loadtxt(os.path.join(DATA_FOLDER, 'responseEND.data'),
  #                           np.int32)
  # response_end = response_end.reshape((response_end.size, 1))

  if MODEL_KNEAREST:
    MODEL.train(samples, cv2.ml.ROW_SAMPLE, responses)
    # MODEL_ENDGAME.train(sample_end, cv2.ml.ROW_SAMPLE, response_end)
  elif MODEL_LOGREG:
    MODEL.fit(samples, responses.ravel())
    # MODEL_ENDGAME.fit(sample_end, response_end.ravel())
  print '[imgUtils.py] Initialization complete (%d samples).' % samples.shape[0]

def shutdown():
  pass


# Detect if the game has ended.
def gameHasEnded(screenshot):
  # screenshot = cv2.resize(screenshot, BOARD_SIZE).astype(np.float32)
  # screenshot = screenshot.reshape((1, NUM_BOARD_PIXELS))
  # if MODEL_KNEAREST:
  #   val, _, _, score = MODEL_ENDGAME.findNearest(screenshot, k=1)
  #   return val == 1 and score < 10000
  # elif MODEL_LOGREG:
  #   val = MODEL_ENDGAME.predict(screenshot)[0]
  #   if val == 0:
  #     return False
  #   [index] = np.where(MODEL_ENDGAME.classes_ == val)
  #   score = MODEL_ENDGAME.predict_proba(screenshot)[0][index][0]
  #   if score > 0.75:
  #     return True
  return False

# Iterate through all grid squares on board.
def parseSquaresFromBoard(img):
  board_bottom = getBoardBottom(img)
  rowIndex = 0
  for yi in range(MAX_ROWS):
    yBottom = int(board_bottom - (SQUARE_HEIGHT * yi))
    yTop = int(max(yBottom - SQUARE_HEIGHT, 0))
    colIndex = 0
    for xi in range(NUM_COLS):
      x = int(SQUARE_WIDTH * xi)
      square = img[yTop:yBottom, x:int(x + SQUARE_WIDTH)]
      square = resizeSquare(square)
      yield square, rowIndex, colIndex
      colIndex += 1
    rowIndex += 1

# Use model to classify each grid square.
def getSquareClassification(square):
  sq = resizeSquare(square).astype(np.float32)
  sq = squareFeatureVector(sq)
  if MODEL_KNEAREST:
    val, _, _, score = MODEL.findNearest(sq, k=1)
    # Best score is lowest distance
    score = -score[0][0]
  elif MODEL_LOGREG:
    val = MODEL.predict(sq)[0]
    [index] = np.where(MODEL.classes_ == val)
    score = MODEL.predict_proba(sq)[0][index][0]
    if score < 0.90 or not withinLuminance(square, val):
      val = board.EMPTY
  return val, score

# Extract board from screenshot.
def cropBoard2Player(img):
  return img[BOARD_TOP:BOARD_BOTTOM, BOARD_LEFT:BOARD_RIGHT]

def resizeSquare(square):
  return cv2.resize(square, (SQUARE_RESHAPE_WIDTH, SQUARE_RESHAPE_HEIGHT))

def squareFeatureVector(square):
  return square.reshape((1, NUM_PIXELS))

# Find where the grid starts by trying all y-positions.
def getBoardBottom(img):
  best_score = None
  best_bottom = -1
  for bottom in range(BOARD_HEIGHT, BOARD_HEIGHT - int(SQUARE_HEIGHT), -1):
    yStart = int(bottom - SQUARE_HEIGHT)
    square = img[yStart:bottom, 0:int(SQUARE_WIDTH)]
    val, score = getSquareClassification(square)
    if score > best_score or best_score == None:
      best_score = score
      best_bottom = bottom
  return best_bottom


def calculateLuminance(square):
  (rows, cols, _) = square.shape
  total = 0.0
  for i in range(rows):
    for j in range(cols):
      [B, G, R] = square[i, j]
      total += (0.299*R + 0.587*G + 0.114*B)
  return total / (rows * cols)

LUMINANCE_MAP = {
  3: 86.5, # Water
  4: 77.5, # Heart
  1: 59.1, # Fire
  5: 99.8, # Electric
  6: 108.4, # Pokeball
  2: 62.5 # Grass
}
def withinLuminance(square, prediction):
  luminance = calculateLuminance(square)
  return abs(luminance - LUMINANCE_MAP[prediction]) < 5


def showImage(img):
  cv2.imshow('IMG', img)
  key = cv2.waitKey(0)
  cv2.destroyAllWindows()
  if key == 27:   # Exit immediately upon escape
    sys.exit(0)


def test():
  initialize()
  filename = os.path.join(train.DATA_FOLDER, 'train1.png')
  grid = cropBoard2Player(cv2.imread(filename))
  responses = [int(i) for i in np.loadtxt(train.RESPONSES_FILE)]
  count = 0
  for square, row, col in parseSquaresFromBoard(grid):
    print calculateLuminance(square)
    val, score = getSquareClassification(square)
    print val, score
    showImage(square)
    count += 1
  shutdown()


if __name__ == '__main__':
  test()
