from random import randint
from flask import Flask, jsonify, request

app = Flask(__name__)

sideLen = 8
numGames = 100

class game:
	def __init__(self):
		self.player1 = ''
		self.player2 = ''
		self.turn = 0
		self.boardState = 0
		self.board = [[' ' for _ in range(sideLen)] for _ in range(sideLen)]

boardLayout = [
	'BR','Bk','BB','BQ','BK','BB','Bk','BR',
	'BP','BP','BP','BP','BP','BP','BP','BP',
	'  ','  ','  ','  ','  ','  ','  ','  ',
	'  ','  ','  ','  ','  ','  ','  ','  ',
	'  ','  ','  ','  ','  ','  ','  ','  ',
	'  ','  ','  ','  ','  ','  ','  ','  ',
	'WP','WP','WP','WP','WP','WP','WP','WP',
	'WR','Wk','WB','WK','WQ','WB','Wk','WR'
]

games = [ game() for i in range(numGames)]

@app.route('/')
def index():
	return "Please refer to our API"

@app.route('/games/<int:boardid>/init', methods=['GET'])
def initBoard(boardid):
	if boardid < 0  or boardid > 99:
		return "404 - Please enter a board number between 0 and 99"

	returnMessage = ""

	if games[boardid].boardState == 0:
		games[boardid].boardState += 1
		games[boardid].player1 = hex(randint(0, 43046721))
		returnMessage += games[boardid].player1

	elif games[boardid].boardState == 1:
		games[boardid].boardState += 1
		idx = 0
		for r in range(0,sideLen):
			for c in range(0,sideLen):
				games[boardid].board[r][c] = boardLayout[idx]
				idx += 1
		games[boardid].player2 = hex(randint(0, 43046721))
		returnMessage += games[boardid].player2

	else:
		print "Board used, refused"
		return jsonify({'err': 'Board in use'}), 423

	print "Init on board " + str(boardid) + " was made, giving user message: " + returnMessage

	return jsonify({'id':returnMessage}), 201

@app.route('/games/<int:boardid>/move', methods=['POST'])
def makeMove(boardid):
	if boardid < 0  or boardid > 99:
		return "404 - Please enter a board number between 0 and 99"

	if not request.json:
		abort(400)

	move = {
		'id' : request.json['id'],
		'moveFrom': request.json['moveFrom'],
		'moveTo': request.json['moveTo']
	}
	#.append(move) We should add this object to a list of previous moves
	#TODO: Sanity check, is move valid
	board = games[boardid]

	if checkMove(board, move):
		moveFromRow = int(7-move['moveFrom'][0])
		moveFromCol = int(move['moveFrom'][1])

		moveToRow = int(7-move['moveTo'][0])
		moveToCol = int(move['moveTo'][1])

		board[moveToRow][moveToCol] = board[moveFromRow][moveFromCol]
		board[moveFromRow][moveFromCol] = ''
	else:
		abort(400)

	return jsonify({'move': move}), 201 #Return JSON move followed by OK

def getPiece(board, position):
	return board[7 - position[1]][position[0]]

def checkMove(board, move):
	#move    = x position,               y position
	moveFrom = int(move['moveFrom'][0]), int(move['moveFrom'][1])
	moveTo   = int(move['moveTo'][0]),   int(move['moveTo'][1])

	# Check the moveFrom index
	if (moveFrom[0] < 0 or moveFrom[0] > 7) or (moveFrom[1] < 0 or moveFrom[1] > 7):
		print "Out of bounds"
		return False

	# Check the moveTo index
	if (moveTo[0] < 0 or moveTo[0] > 7) or (moveTo[1] < 0 or moveTo[1] > 7):
		print "Out of bounds"
		return False

	piece = getPiece(board, moveFrom)

	color = piece[0]
	if color != 'W' or color != 'B':
		print "Color is wrong somehow"
		return False

	type = piece[1]
	if type == 'K':
		# checks for King
		return checkOrthogonal(moveFrom, moveTo) or checkDiagonal(moveFrom, moveTo)

	if type == 'Q':
		# checks for Queen
		return checkOrthogonal(moveFrom, moveTo) or checkDiagonal(moveFrom, moveTo)

	if type == 'k':
		# checks for Knight
		xDiff = abs(moveTo[0], moveFrom[0])
		yDiff = abs(moveTo[1], moveFrom[1])

		if xDiff == 0 and yDiff == 0:
			return False
		# if the xDiff was 3 away, y must be 2 to be a correct move
		if xDiff == 3 and yDiff != 2:
			return False
		# if the xDiff was 2 away, y must be 3 to be a correct move
		elif xDiff == 2 and yDiff != 3:
			return False

		return True

	if type == 'B':
		# checks for Bishop
		return checkDiagonal(moveFrom, moveTo)

	if type == 'R':
		# checks for Rook
		return checkOrthogonal(moveFrom, moveTo)

	if type == 'P':
		# Check white pawn
		if color == 'W':
			if moveTo[0] != moveFrom[0]: #make sure X pos is the same
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

		elif color == 'B':
			if moveTo[0] != moveFrom[0]: #make sure X pos is the same
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
	xDiff = abs(moveTo[0], moveFrom[0])
	yDiff = abs(moveTo[1], moveFrom[1])

	if xDiff == 0 and yDiff == 0:
		return False

	if xDiff == yDiff:
		return False

	return True

def checkOrthogonal(moveFrom, moveTo):
	xDiff = abs(moveTo[0], moveFrom[0])
	yDiff = abs(moveTo[1], moveFrom[1])

	if xDiff == 0 and yDiff == 0:
		return False

	if xDiff != 0 and yDiff != 0:
		return False

	return True

@app.route('/games/<int:boardid>/status', methods=['GET'])
def boardStatus(boardid):
	if boardid < 0  or boardid > 99:
		return "404 - Please enter a board number between 0 and 99"

	#Stringify the board and return it
	boardString = ''
	for r in range(0,sideLen):
		boardString += '|'
		for c in range(0,sideLen):
			boardString += '%s |' % (games[boardid].board[r][c])
		boardString += '<br/>'

	return boardString

if __name__ == '__main__':
	app.run(debug=True)
