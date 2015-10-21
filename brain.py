#!/usr/bin/env python

## All of our AI techniques to develop a Pokemon Puzzle League agent.

import random

from constants import *

# Abstract class, defining what needs to be implemented to be an AI.
class PPLBrain:
  # Given a board, return the next action that the agent should take.
  def getNextAction(self, board): raise NotImplementedError('Override me')


class BaselineBrain(PPLBrain):
  # Return a random move.
  def getNextAction(self, board):
    return random.choice([KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT])
