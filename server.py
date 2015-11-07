from random import randint
from flask import Flask, jsonify, request, url_for, send_from_directory, render_template

app = Flask(__name__)

sideLen = 8
numGames = 100

class game:
	def __init__(self):
		self.player1 = ''
		self.player2 = ''
		self.turn = 0
		self.boardState = 0
		self.board = [['' for _ in range(sideLen)] for _ in range(sideLen)]

	def getPiece(self, x, y):
		if (0 <= x <= 7) and (0 <= y <= 7):
			return self.board[7-y][x]
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
	'bR','bN','bB','bK','bQ','bB','bN','bR',
	'bP','bP','bP','bP','bP','bP','bP','bP',
	'  ','  ','  ','  ','  ','  ','  ','  ',
	'  ','  ','  ','  ','  ','  ','  ','  ',
	'  ','  ','  ','  ','  ','  ','  ','  ',
	'  ','  ','  ','  ','  ','  ','  ','  ',
	'wP','wP','wP','wP','wP','wP','wP','wP',
	'wR','wN','wB','wK','wQ','wB','wN','wR'
]

games = [ game() for i in range(numGames)]

@app.route('/')
def index():
	return app.send_static_file('index.html')

@app.route('/api')
def send_api():
	return app.send_static_file('api.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img', path)

@app.route('/games/<int:boardid>/init', methods=['GET'])
def initBoard(boardid):
	if boardid < 0  or boardid > 99:
		return "404 - Please enter a board number between 0 and 99"

	returnMessage = [{}]

	if games[boardid].boardState == 0:
		games[boardid].boardState += 1
		games[boardid].player1 = hex(randint(0, 43046721))
		returnMessage[0]['id'] = games[boardid].player1
		returnMessage[0]['color'] = 'W'

	elif games[boardid].boardState == 1:
		games[boardid].boardState += 1
		idx = 0
		for r in range(0,sideLen):
			for c in range(0,sideLen):
				games[boardid].board[r][c] = boardLayout[idx]
				idx += 1
		games[boardid].player2 = hex(randint(0, 43046721))
		returnMessage[0]['id'] = games[boardid].player2
		returnMessage[0]['color'] = 'B'
	else:
		print "Board used, refused"
		returnMessage[0]['err'] = "Board is being used"
		return jsonify(returnMessage[0]), 423

	#print "Init on board " + str(boardid) + " was made, giving user message: " + returnMessage

	return jsonify(returnMessage[0]), 201

@app.route('/games/<int:boardid>/move', methods=['POST'])
def makeMove(boardid):
	if boardid < 0  or boardid > 99:
		return "404 - Please enter a board number between 0 and 99"

	if not request.json:
		return jsonify({'err': 'Not json type'}), 400

	move = {
		'id' : request.json['id'],
		'moveFrom': request.json['moveFrom'],
		'moveTo': request.json['moveTo']
	}
	#.append(move) We should add this object to a list of previous moves
	#TODO: Sanity check, is move valid

	if checkMove(games[boardid], move):
		moveFrom = games[boardid].convert(move['moveFrom'])
		moveTo = games[boardid].convert(move['moveTo'])

		piece = games[boardid].getPiece(moveFrom[0], moveFrom[1])

		games[boardid].setPiece(moveTo[0], moveTo[1], piece)
		games[boardid].setPiece(moveFrom[0], moveFrom[1], "")
	else:
		return jsonify({'err': 'Bad move'}), 406

	return jsonify({'move': move}), 201 #Return JSON move followed by OK

def checkMove(game, move):
	#move    = x position,               y position
	moveFrom = game.convert(move['moveFrom'])
	moveTo   = game.convert(move['moveTo'])

	piece = game.getPiece(moveFrom[0], moveFrom[1])

	if not piece:
		return False

	color = piece[0]

	print moveFrom
	print moveTo
	print piece

	if color != 'w' and color != 'b':
		print "Color is wrong somehow"
		return False

	type = piece[1]
	if type == 'K':
		# checks for King
		print "check king"
		return checkOrthogonal(moveFrom, moveTo) or checkDiagonal(moveFrom, moveTo)

	if type == 'Q':
		# checks for Queen
		print "check queen"
		return checkOrthogonal(moveFrom, moveTo) or checkDiagonal(moveFrom, moveTo)

	if type == 'N':
		# checks for Knight
		print "check knight"
		xDiff = abs(moveTo[0] - moveFrom[0])
		yDiff = abs(moveTo[1] - moveFrom[1])
		print (xDiff, yDiff)

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
		print "check bishop"
		return checkDiagonal(moveFrom, moveTo)

	if type == 'R':
		# checks for Rook
		print "check rook"
		return checkOrthogonal(moveFrom, moveTo)

	if type == 'P':
		# Check white pawn
		print "check pawn"
		if color == 'w':
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

		elif color == 'b':
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

@app.route('/games/<int:boardid>/status', methods=['GET'])
def boardStatus(boardid):
	if boardid < 0  or boardid > 99:
		return "404 - Please enter a board number between 0 and 99"

	#Stringify the board and return it
	boardString = [{}]
	for r in range(0,sideLen):
		for c in range(0,sideLen):
			boardString[0][games[boardid].revert((7-c, 7-r))] = games[boardid].board[r][c]

	return jsonify(boardString[0]), 201

if __name__ == '__main__':
	app.run(debug=True)
