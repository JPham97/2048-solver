from __future__ import absolute_import, division, print_function
import copy
import random
MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}

class Gametree:
	"""main class for the AI"""
	# Hint: Two operations are important. Grow a game tree, and then compute minimax score.
	# Hint: To grow a tree, you need to simulate the game one step.
	# Hint: Think about the difference between your move and the computer's move.
	def __init__(self, root_state, depth_of_tree, current_score):
		pass
	# expectimax for computing best move
	def expectimax(self, state):
		pass
	# function to return best decision to game
	def compute_decision(self):
		#change this return value when you have implemented the function
		return 0

class Simulator:
	pass
