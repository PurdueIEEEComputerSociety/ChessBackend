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
		'id' : 0,
		'piece': request.json['piece'],
		'moveTo': request.json['moveTo']
	}
	#.append(move) We should add this object to a list of previous moves
	#TODO: Sanity check, is move valid
	row = int(move['moveTo'][0])
	col = int(move['moveTo'][1])
	if (row < 0 or row > 7) or (col < 0 or col > 7):
		abort(400)

	games[boardid][row][col] = move['piece']
	return jsonify({'move': move}), 201 #Return JSON move followed by OK 

def checkBoard():
	#Check pawn
	#	- Turn == 1 then check 1 or 2 spaces, other turns check 1 space ahead. Check if left or right is occupied (and allow movement)
	
	#Check  
	print "hi"

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
