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
