sideLen = 8
numGames = 100

class game:
	def __init__(self):
		self.player1 = ''
		self.player2 = ''
		self.turn = 0
		self.boardState = 0
		self.board = [['' for _ in range(sideLen)] for _ in range(sideLen)]
		self.currentPlayer = 0

	def getPiece(self, x, y):
		if (0 <= x <= 7) and (0 <= y <= 7):
			return self.board[7-y][x].strip()
		return ""

	def setPiece(self, x, y, piece):
		if (0 <= x <= 7) and (0 <= y <= 7):
			self.board[7-y][x-0] = piece

	def convert(self, move):
		return ord(move[0].lower()) - 97, int(move[1]) - 1 # value of 'a' is 97

	def revert(self, move):
		if (0 <= move[0] <= 7) and (0 <= move[1] <= 7):
			return chr(104 - move[0]) + str(move[1] + 1)



boardLayout = [
	'bR','bN','bB','bQ','bK','bB','bN','bR',
	'bP','bP','bP','bP','bP','bP','bP','bP',
	'  ','  ','  ','  ','  ','  ','  ','  ',
	'  ','  ','  ','  ','  ','  ','  ','  ',
	'  ','  ','  ','  ','  ','  ','  ','  ',
	'  ','  ','  ','  ','  ','  ','  ','  ',
	'wP','wP','wP','wP','wP','wP','wP','wP',
	'wR','wN','wB','wQ','wK','wB','wN','wR'
]

def validDirection(game, move):

	moveFrom = game.convert(move['moveFrom'])
	moveTo   = game.convert(move['moveTo'])

	piece = game.getPiece(moveFrom[0], moveFrom[1])

	if not piece:
		return False

	color = piece[0]

	#Don't allow player to move the opposite color
	if (color is 'w' and game.currentPlayer is not 0) or (color is 'b' and game.currentPlayer is not 1):
		return False


	if color != 'w' and color != 'b':
		return False

	type = piece[1]
	if type == 'K':
		# checks for King
		print "check king"
		xDiff = abs(moveTo[0] - moveFrom[0])
		yDiff = abs(moveTo[1] - moveFrom[1])
		if xDiff > 1 or yDiff > 1:
			return False
		else:
			return checkOrthogonal(moveFrom, moveTo) or checkDiagonal(moveFrom, moveTo)

	if type == 'Q':
		# checks for Queen
		return checkOrthogonal(moveFrom, moveTo) or checkDiagonal(moveFrom, moveTo)

	if type == 'N':
		# checks for Knight
		xDiff = abs(moveTo[0] - moveFrom[0])
		yDiff = abs(moveTo[1] - moveFrom[1])

		if xDiff == 0 and yDiff == 0:
			return False
		# if the xDiff was 3 away, y must be 2 to be a correct move
		if xDiff == 2 and yDiff == 1:
			return True
		# if the xDiff was 2 away, y must be 3 to be a correct move
		elif xDiff == 1 and yDiff == 2:
			return True

		return False

	if type == 'B':
		# checks for Bishop
		return checkDiagonal(moveFrom, moveTo)

	if type == 'R':
		# checks for Rook
		return checkOrthogonal(moveFrom, moveTo)

	if type == 'P':
		# Check white pawn
		if color == 'w':
			if moveTo[0] != moveFrom[0]: #make sure X pos is the same
				if abs(moveTo[0] - moveFrom[0]) == 1 and moveTo[1] == moveFrom[1]+1:
					checkPiece = game.getPiece(moveTo[0], moveTo[1])
					if checkPiece is not "" and checkPiece[0] is 'b':
						return True

				return False

			# if white pawn is in starting pos
			if moveFrom[1] == 1:
				# white pawn can move to pos y + 1 or y + 2 (move up the board)
				if moveTo[1] != moveFrom[1] + 1 and moveTo[1] != moveFrom[1] + 2:
					return False
			else:
				# white pawn is not in starting pos, so can only move to y + 1
				if moveTo[1] != moveFrom[1] + 1:
					return False

			return True

		elif color == 'b':
			if moveTo[0] != moveFrom[0]: #make sure X pos is the same
				if abs(moveTo[0] - moveFrom[0]) == 1 and moveTo[1] == moveFrom[1]-1:
					checkPiece = game.getPiece(moveTo[0], moveTo[1])
					if checkPiece is not "" and checkPiece[0] is 'w':
						return True

				return False

			# if black pawn is in starting pos
			if moveFrom[1] == 6:
				# black pawn can move to pos y - 1 or y - 2 (move down the board)
				if moveTo[1] != moveFrom[1] - 1 and moveTo[1] != moveFrom[1] - 2:
					return False
			else:
				# black pawn is not in starting pos, so can only move to y - 1
				if moveTo[1] != moveFrom[1] - 1:
					return False

			return True

		else:
			return False


	return True

def checkDiagonal(moveFrom, moveTo):
	xDiff = abs(moveTo[0] - moveFrom[0])
	yDiff = abs(moveTo[1] - moveFrom[1])

	if xDiff == 0 and yDiff == 0:
		return False

	if xDiff != yDiff:
		return False

	return True

def checkOrthogonal(moveFrom, moveTo):
	xDiff = abs(moveTo[0] - moveFrom[0])
	yDiff = abs(moveTo[1] - moveFrom[1])

	if xDiff == 0 and yDiff == 0:
		return False

	if xDiff != 0 and yDiff != 0:
		return False

	return True

def obstructed(game, move):
	# assume move is correct
	moveFrom = game.convert(move['moveFrom'])
	moveTo   = game.convert(move['moveTo'])

	piece = game.getPiece(moveFrom[0], moveFrom[1])

	if not piece:
		return False

        if piece[1] is 'N':
            return False

	color = piece[0]

	if piece[1] is 'P':
		if abs(moveFrom[0] - moveTo[0]) is 0:
			checkPiece = game.getPiece(moveTo[0], moveTo[1])
			if checkPiece is not "":
				return True


	xDirection =  0
	if moveTo[0] - moveFrom[0] < 0:
		xDirection = -1

	if moveTo[0] - moveFrom[0] > 0:
		xDirection = 1

	yDirection =  0
	if moveTo[1] - moveFrom[1] < 0:
		yDirection = -1

	if moveTo[1] - moveFrom[1] > 0:
		yDirection = 1

	steps = max(abs(moveFrom[0] - moveTo[0]), abs(moveFrom[1] - moveTo[1]))
	start = moveFrom

	for offset in range(1, steps+1):
		checkPiece = game.getPiece(start[0] + offset*xDirection, start[1] + offset*yDirection)
		if checkPiece is not "":

			if offset is steps:
				if checkPiece[0] is color:
					return True
				else:
					print "CAPTURE!"
					print checkPiece
					if checkPiece[1] is 'K':
						print "GAME OVER"
						game.boardState = 3
			else:
				return True

	return False
