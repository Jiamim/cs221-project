#!/usr/bin/env python

import random
import board
import randomBrain
import geneticBrain
import exhaustiveBrain

# Abstract class, defining what needs to be implemented to be an AI.
class PPLBrain:

  # Given a board, return a list of moves that the agent should take.
  # Each element of the list should be a tuple: ((rowIndex, colIndex), clear)
  # Indices are 0-indexed counting from the bottom-left corner.
  # Set the clear boolean flag to True if the move results in a clear.
  # So, moving to the bottom-left corner to clear blocks would be ((0, 0), True)
  def getNextMoves(self, board): raise NotImplementedError('Override me')


class BaselineBrain(PPLBrain):
  # Return a 25 random move sequence.
  def getNextMoves(self, board):
    max_row_index = 11
    max_col_index = 5
    moves = []
    for _ in range(25):
      clear = 0
      row_index = random.randint(0, max_row_index - 4)
      col_index = random.randint(0, max_col_index)
      move = ((row_index, col_index), clear)
      moves.append(move)
    return moves

class TestSequencesBrain(PPLBrain):
  # Return a manually set test move sequence
  def getNextMoves(self, board):
    moves = []
    moves.append(((0,1), 0))
    moves.append(((0,2), 1))
    moves.append(((9,4), 1))
    moves.append(((4,0), 0))
    moves.append(((5,1), 4))
    return moves

class RandomBrainBrain(PPLBrain):
  # Return a sequence of moves as determined by the random brain
  def getNextMoves(self, board):
    rBrain = randomBrain.RandomBrain()
    return rBrain.findBestActions(board)[1]

class GeneticBrainBrain(PPLBrain):
  # Return a sequence of moves as determined by the random brain
  def getNextMoves(self, board):
    gBrain = geneticBrain.GeneticBrain()
    return gBrain.findBestActions(board)[1]

class ExhaustiveBrainBrain(PPLBrain):
  # Return a sequence of moves as determined by the random brain
  def getNextMoves(self, board):
    eBrain = exhaustiveBrain.ExhaustiveBrain()
    return eBrain.findBestActions(board)[1]

