'''
Jeremy Pham
A12962840
CSE 150
PA2
'''

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
		self.depth = depth_of_tree

		# the root of the game tree
		self.root = Gamenode(root_state, current_score, is_player=True)

	'''
	Runs the expectimax algorithm on the constructed game tree to determine
	the next best move. Returns a pair (value, direction)
	'''
	def expectimax(self, state):
		# a node of the constructed game tree will be passed in
		node = state

		# if it's a leaf node, just return the payoff which is a pair (value, direction)
		if node.is_terminal:
			return node.payoff()
		# this is a max node
		elif node.is_player:
			value = -float("Inf")
			best_move = 1
			for n in node.children:
				# whenever a better value is found, also update the current best move
				res = self.expectimax(n)[0]
				if res > value:
					value = res
					best_move = n.from_dir

				# edge case, prevents the AI from stalling if the second layer of the
				# game tree results in game over
				elif res == -float("Inf"):
					best_move = random.randint(0, len(MOVES) - 1)
			return (value, best_move)
		# a chance node
		elif not node.is_player:
			value = 0
			for n in node.children:
				# make sure to calculate the probability of each child
				value = value + self.expectimax(n)[0] * node.chance()
			return (value, -1)
		else:
			print("Should not reach here")
			return

	'''
	Function to the return the next optimal decision.
	Each time this function is called, the game tree should be constructed
	and the best decision should be made using expectimax.
	'''
	def compute_decision(self):
		# grow the tree starting from root node to depth
		self.growTree(self.root, depth=0)
		# after growing, run expectimax to find optimal move
		optimal_move = self.expectimax(self.root)[1]
		return optimal_move

	'''
	This function will take in a root node and expand the game tree 3 more
	levels recursively.
	'''
	def growTree(self, node, depth):

		moves = 4
		board_size = 4
		cpu_tile = 2
		# use this as a place holder in the list of children in order to
		# keep track of which moves did not alter the board
		#empty_matrix = [[-1,-1,-1,-1], [-1,-1,-1,-1], [-1,-1,-1,-1], [-1,-1,-1,-1]]

		# base case, creates returns the node because we are at the leaf level
		if depth == self.depth:

			node.is_terminal = True
			return node

		# 2 recursive cases, max node or chance node

		# make a MAX NODE
		if node.is_player:
			# only 4 possible moves
			for i in range(len(MOVES)):
				# create a copy of the node and run the simulator on it
				tmp = copy.deepcopy(node)
				sim = Simulator(tmp.score, tmp.state)
				sim.move(i)
				# do not add duplicate boards
				if node.state != sim.tileMatrix:
					# create a subtree recursively
					# this child node is the root with a simulated direction input
					child = self.growTree(Gamenode(sim.tileMatrix, sim.total_points, False, from_dir=i), depth + 1)
					# add the child to the list of children in the current root
					node.children.append(child)

		# make a CHANCE NODE
		else:
			# iterate through the entire board and look for 0's
			for i in range(len(node.state)):
				for j in range(len(node.state)):
					tm = node.state
					if tm[i][j] == 0:
						# make a copy of the root's tileMatrix and add a 2 to it
						tmp = copy.deepcopy(node)
						tmp.state[i][j] = cpu_tile
						# create a subtree recursively
						# this child node is a max node with a simulated added tile
						child = self.growTree(Gamenode(tmp.state, tmp.score, True, from_dir=-1), depth + 1)
						# add the child to the list of children in the current root
						node.children.append(child)

		return node


'''
This node class represents the nodes of the Gametree
'''
class Gamenode:
	def __init__(self, state, score, is_player=False, children=None, from_dir=0):
		self.state = state
		self.score = score

		# determines if this is a max node or a chance node
		self.is_player = is_player

		# determines if this is a terminal node
		self.is_terminal = False

		if children is None:
			self.children = []
		else:
			self.children = children

		# keep track of the move that led to this node
		# will be -1 if the last node was chance node
		self.from_dir = from_dir

	'''
	A string representation of the Gamenode
	'''
	def __str__(self):
		full_str = str(self.score) + "\t" + str(self.state)
		return full_str

	'''
	Assigns a node a "score" based on the current game state stored
	in the node. This is used as a heuristic to determine the next
	optimal move.
	'''
	def payoff(self):
		return (self.score, self.from_dir)

	'''
	Calculates the probability that the state stored inside of a chance
	node's child will be reached. In this context, it is the probability
	of a random tile appearing in some empty tile at a certain board state.
	'''
	def chance(self):
		if self.is_player:
			print("This is not a chance_player node")
			return 0
		return 1/(len(self.children))


'''
This class contains methods used to "simulate" game moves on a given board.
This is necessary in order to predict and determine optimal moves.
An instance of this class is initialized with a board state and score.
'''
class Simulator:

	def __init__(self, curr_points, curr_tileMatrix):
		self.total_points = curr_points

		self.board_size = 4

		self.tileMatrix = curr_tileMatrix


	def move(self, direction):
		for i in range(0, direction):
			self.rotateMatrixClockwise()
		if self.canMove():
			self.moveTiles()
			self.mergeTiles()
		for j in range(0, (4 - direction) % 4):
			self.rotateMatrixClockwise()

	def rotateMatrixClockwise(self):
		tm = self.tileMatrix
		for i in range(0, int(self.board_size/2)):
			for k in range(i, self.board_size- i - 1):
				temp1 = tm[i][k]
				temp2 = tm[self.board_size - 1 - k][i]
				temp3 = tm[self.board_size - 1 - i][self.board_size - 1 - k]
				temp4 = tm[k][self.board_size - 1 - i]
				tm[self.board_size - 1 - k][i] = temp1
				tm[self.board_size - 1 - i][self.board_size - 1 - k] = temp2
				tm[k][self.board_size - 1 - i] = temp3
				tm[i][k] = temp4

	def canMove(self):
		tm = self.tileMatrix
		for i in range(0, self.board_size):
			for j in range(1, self.board_size):
				if tm[i][j-1] == 0 and tm[i][j] > 0:
					return True
				elif (tm[i][j-1] == tm[i][j]) and tm[i][j-1] != 0:
					return True
		return False

	def moveTiles(self):
		tm = self.tileMatrix
		for i in range(0, self.board_size):
			for j in range(0, self.board_size - 1):
				while tm[i][j] == 0 and sum(tm[i][j:]) > 0:
					for k in range(j, self.board_size - 1):
						tm[i][k] = tm[i][k + 1]
					tm[i][self.board_size - 1] = 0

	def mergeTiles(self):
		tm = self.tileMatrix
		for i in range(0, self.board_size):
			for k in range(0, self.board_size - 1):
				if tm[i][k] == tm[i][k + 1] and tm[i][k] != 0:
					tm[i][k] = tm[i][k] * 2
					tm[i][k + 1] = 0
					self.total_points += tm[i][k]
					self.moveTiles()

	###### End of copied game engine methods ######

	def sim_player(self, direction):
		self.move(direction)
