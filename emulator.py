#!/usr/bin/env python

import os
import sys
import time

# import cv2
import numpy as np
# from sklearn import linear_model

import board
import controller
import screenshot as screen
# import train

WSHELL = None

# Choose which model to use
# MODEL_KNEAREST, MODEL_LOGREG = False, True
# if MODEL_KNEAREST:
#   MODEL = cv2.ml.KNearest_create()
#   MODEL_ENDGAME = cv2.ml.KNearest_create()
# elif MODEL_LOGREG:
#   MODEL = linear_model.LogisticRegression(C=1e5)
#   MODEL_ENDGAME = linear_model.LogisticRegression(C=1e5)

MOVE_WAIT = 0
CLEAR_WAIT = 2.4

def run(brain):
  print '[emulator.py] Running game...'
  cursor_pos = (0, 0)
  for _ in range(10):
    controller.MAIN_DOWN()
    controller.MAIN_LEFT()
  for i in xrange(100):
    screenshot = screen.takeScreenshot()
    # if gameHasEnded(screenshot):
    #   break
    # boardImg = cropBoardFromScreenshot(screenshot)

    # # Generate board model.
    # inputRows = [[-1] * board.WIDTH for _ in range(board.HEIGHT)]
    # for square, rowIndex, colIndex in parseSquaresFromBoard(boardImg):
    #   img = cv2.resize(square, SQUARE_SIZE).astype(np.float32)
    #   img = img.reshape((1, NUM_PIXELS))
    #   val, score = getSquareClassification(img)
    #   inputRows[rowIndex][colIndex] = val

    # # Get next action and perform.
    # b = board.Board(inputRows=inputRows)
    moves = brain.getNextMoves(None)
    cursor_pos = performMoves(moves, cursor_pos)

    # End loop.
  print '[emulator.py] Done running game.'

def performMoves(moves, cursor_pos):
  for move in moves:
    next_pos, clear = move
    row_delta, col_delta = (next_pos[0] - cursor_pos[0], next_pos[1] - cursor_pos[1])
    if row_delta > 0:
      for _ in range(row_delta): controller.MAIN_UP()
    elif row_delta < 0:
      for _ in range(-row_delta): controller.MAIN_DOWN()
    if col_delta > 0:
      for _ in range(col_delta): controller.MAIN_RIGHT()
    elif col_delta < 0:
      for _ in range(-col_delta): controller.MAIN_LEFT()
    cursor_pos = next_pos
    controller.A()
    time.sleep(MOVE_WAIT)
    if clear:
      time.sleep(clear * CLEAR_WAIT)
  return cursor_pos


# Send keys to Project64.
def performAction(action):
  WSHELL.AppActivate(WINDOW_NAME)
  if action == KEY_UP:
    keyboard.UP(True)
  elif action == KEY_DOWN:
    keyboard.DOWN(True)
  elif action == KEY_LEFT:
    keyboard.LEFT(True)
  elif action == KEY_RIGHT:
    keyboard.RIGHT(True)
  keyboard.A(True)

# Detect if the game has ended.
def gameHasEnded(screenshot):
  screenshot = cv2.resize(screenshot, BOARD_SIZE).astype(np.float32)
  screenshot = screenshot.reshape((1, NUM_BOARD_PIXELS))
  if MODEL_KNEAREST:
    val, _, _, score = MODEL_ENDGAME.findNearest(screenshot, k=1)
    return val == 1 and score < 10000
  elif MODEL_LOGREG:
    val = MODEL_ENDGAME.predict(screenshot)[0]
    if val == 0:
      return False
    [index] = np.where(MODEL_ENDGAME.classes_ == val)
    score = MODEL_ENDGAME.predict_proba(screenshot)[0][index][0]
    if score > 0.75:
      return True
  return False

# Iterate through all grid squares on board.
def parseSquaresFromBoard(img):
  board_bottom = getBoardBottom(img)
  rowIndex = 0
  for y in range(board_bottom, 0, -SQUARE_HEIGHT):
    colIndex = 0
    for xs in GRID_XS:
      yStart = max(y - SQUARE_HEIGHT, 0)
      square = img[yStart:y, xs[0]:xs[1]]
      yield square, rowIndex, colIndex
      colIndex += 1
    rowIndex += 1

# Use model to classify each grid square.
def getSquareClassification(square):
  if MODEL_KNEAREST:
    val, _, _, score = MODEL.findNearest(square, k=1)
    # Best score is lowest distance
    score = -score[0][0]
  elif MODEL_LOGREG:
    val = MODEL.predict(square)[0]
    [index] = np.where(MODEL.classes_ == val)
    score = MODEL.predict_proba(square)[0][index][0]
  return val, score

# Find where the grid starts by trying all y-positions.
def getBoardBottom(img):
  best_score = None
  best_bottom = -1
  for board_bottom in range(BOARD_HEIGHT, BOARD_HEIGHT - SQUARE_HEIGHT, -1):
    yStart = board_bottom - SQUARE_HEIGHT
    square = img[yStart:board_bottom, GRID_XS[0][0]:GRID_XS[0][1]]
    sq = cv2.resize(square, SQUARE_SIZE).astype(np.float32)
    sq = sq.reshape((1, NUM_PIXELS))
    val, score = getSquareClassification(sq)
    if score > best_score or best_score == None:
      best_score = score
      best_bottom = board_bottom
  return best_bottom

# Extract board from screenshot.
def cropBoardFromScreenshot(img):
  return img[BOARD_Y:(BOARD_Y + BOARD_HEIGHT), BOARD_X:(BOARD_X + BOARD_WIDTH)]


# Start script.
def initialize():
  pass
  # global WSHELL, MODEL
  # print '[emulator.py] Dispatching shell...'
  # WSHELL = win32com.client.Dispatch('WScript.Shell')
  # print '[emulator.py] Training models...'
  # samples = np.loadtxt(os.path.join(DATA_FOLDER, 'samples.data'), np.float32)
  # responses = np.loadtxt(os.path.join(DATA_FOLDER, 'responses.data'), np.int32)
  # responses = responses.reshape((responses.size, 1))

  # sample_end = np.loadtxt(os.path.join(DATA_FOLDER, 'sampleEND.data'),
  #                         np.float32)
  # response_end = np.loadtxt(os.path.join(DATA_FOLDER, 'responseEND.data'),
  #                           np.int32)
  # response_end = response_end.reshape((response_end.size, 1))

  # if MODEL_KNEAREST:
  #   MODEL.train(samples, cv2.ml.ROW_SAMPLE, responses)
  #   MODEL_ENDGAME.train(sample_end, cv2.ml.ROW_SAMPLE, response_end)
  # elif MODEL_LOGREG:
  #   MODEL.fit(samples, responses.ravel())
  #   MODEL_ENDGAME.fit(sample_end, response_end.ravel())
  # print '[emulator.py] Initialization complete (%d samples).' % samples.shape[0]

def shutdown():
  pass


def test():
  WSHELL.AppActivate(WINDOW_NAME)
  time.sleep(0.4)
  t0 = time.time()
  tttt.RIGHT()
  tttt.RIGHT()
  tttt.RIGHT()
  tttt.DOWN()
  tttt.DOWN()
  tttt.DOWN()
  tttt.DOWN()
  print time.time() - t0
  sys.exit(0)

  screenshot = screen.takeScreenshot()
  screenshot = cv2.imread(os.path.join(DATA_FOLDER, 'snapENDGAME.jpg'))
  boardImg = cropBoardFromScreenshot(screenshot)
  gameHasEnded(boardImg)

  for square, rowIndex, colIndex in parseSquaresFromBoard(boardImg):
    img = cv2.resize(square, SQUARE_SIZE).astype(np.float32)
    img = img.reshape((1, NUM_PIXELS))
    val, score = getSquareClassiification(img)
    print val
    train.printVal((val))
    print score
    print '*********'
    debug_showImage(square)

if __name__ == '__main__':
  pass
  # screen.initialize()
  # initialize()
  # test()
  # shutdown()
  # screen.shutdown()
