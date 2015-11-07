from flask import Flask, jsonify, request

app = Flask(__name__)

sideLen = 8
numGames = 100
games = [[[' ' for _ in range(sideLen)] for _ in range(sideLen)] for _ in range(numGames)] # init 100, 8 x 8 boards

@app.route('/')
def index():
	return "Please refer to our API"

@app.route('/games/<int:boardid>/move', methods=['POST'])
def makeMove(boardid):
	if not request.json:
		abort(400)

	move = {
		'id' : request.json['id']
		'moveFrom': request.json['moveFrom'],
		'moveTo': request.json['moveTo']
	}
	#.append(move) We should add this object to a list of previous moves
	#TODO: Sanity check, is move valid
	board = games[boardid]

	if checkMove(board, move):
		moveFromRow = int(move['moveFrom'][0])
		moveFromCol = int(move['moveFrom'][1])

		moveToRow = int(move['moveTo'][0])
		moveToCol = int(move['moveTo'][1])

		board[moveToRow][moveToCol] = board[moveFromRow][moveFromCol]
		board[moveFromRow][moveFromCol] = ''
	else:
		abort(400)

	return jsonify({'move': move}), 201 #Return JSON move followed by OK

def checkMove(board, move):
	moveFromRow = int(7 - move['moveFrom'][0])
	moveFromCol = int(move['moveFrom'][1])

	moveToRow = int(7 - move['moveTo'][0])
	moveToCol = int(move['moveTo'][1])

	piece = board[moveFromRow][moveFromCol]

	if (row < 0 or row > 7) or (col < 0 or col > 7):
		print "Out of bounds"
		return False

	color = piece[0]
	if color not 'W' or color not'B':
		print "Color is wrong somehow"
		return False

	type = piece[1]
	if type is 'K':
		# checks for king

	if type is 'Q':
		# checks for Queen

	if type is 'k'
		# checks for Knight

	if type is 'B'
		# checks for bishop

	if type is 'R'
		# checks for rook

	if type is 'P':
		# checks for pawn

	return True

def checkDiagonal(moveFrom, moveTo):




	return True

def checkOrthogonal(moveFrom, moveTo):




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
			boardString += '%s |' % (games[boardid][r][c])
		boardString += '<br/>'

	return boardString

if __name__ == '__main__':
	app.run(debug=True)
