from random import randint
from flask import Flask, jsonify, request, url_for, send_from_directory, render_template
from flask.ext.cors import CORS
from gamelogic import *

app = Flask(__name__)
CORS(app)

games = [ game() for i in range(numGames)]

def isPlayersTurn(game, playerID):
	if (playerID == game.player1) and (game.currentPlayer is 0):
		return True
	elif (playerID == game.player2) and (game.currentPlayer is 1):
		return True
	
	return False

#
# Return the api documentation on / 
#
@app.route('/')
def index():
	return app.send_static_file('api.html')

#
# /games/boardid/init/
# Init the board id. Returns a key that must be used for next requests.
# Once two people init game it will start
#
@app.route('/games/<int:boardid>/init', methods=['GET'])
def initBoard(boardid):
	if boardid < 0  or boardid > (numGames - 1):
		return jsonify({'err': 'Please enter a board number between 0 and ' + (numGames-1)}), 404

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

#
#
@app.route('/games/<int:boardid>/move', methods=['POST'])
def makeMove(boardid):
	if boardid < 0  or boardid > (numGames - 1):
		return jsonify({'err': 'Please enter a board number between 0 and ' + (numGames-1)}), 404

	if not request.json:
		return jsonify({'err': 'Not json type'}), 400

	move = {
		'id' : request.json['id'],
		'moveFrom': request.json['moveFrom'],
		'moveTo': request.json['moveTo']
	}
	#.append(move) We should add this object to a list of previous moves
	#TODO: Sanity check, is move valid

	#Make sure the player of the current turn is going
	if not isPlayersTurn(games[boardid], move['id']):
		print "Not right ID"
		return jsonify({'err': 'Not your turn'}), 403

	if not validDirection(games[boardid], move):
		return jsonify({'err': 'Move not available'}), 406

	if obstructed(games[boardid], move):
		return jsonify({'err': 'Move is obstructed'}), 409

	moveFrom = games[boardid].convert(move['moveFrom'])
	moveTo = games[boardid].convert(move['moveTo'])


	piece = games[boardid].getPiece(moveFrom[0], moveFrom[1])
	games[boardid].setPiece(moveTo[0], moveTo[1], piece)
	games[boardid].setPiece(moveFrom[0], moveFrom[1], "")
	games[boardid].currentPlayer = (games[boardid].currentPlayer + 1) % 2

	return jsonify({'move': move}), 201 #Return JSON move followed by OK


#
#
@app.route('/games/<int:boardid>/turn', methods=['POST'])
def allowedToPlay(boardid):
	if boardid < 0  or boardid > (numGames - 1):
		return jsonify({'err': 'Please enter a board number between 0 and ' + (numGames-1)}), 404

	if games[boardid].boardState == 0 or games[boardid].boardState == 1:
		return jsonify({'allow':False, 'err': 'Board not ready!'}), 200

	if not request.json:
		return jsonify({'err': 'Not json type'}), 400

				
	player = {
		'id' : request.json['id'],
	}

	if games[boardid].boardState == 3: 
		if player['id']	== games[boardid].player1:
			games[boardid].player1 = ''
		elif player['id'] == games[boardid].player2:
			games[boardid].player2 = ''
		
		if games[boardid].player1 == games[boardid].player2 == '':
			games[boardid].boardState = 0 

	if isPlayersTurn(games[boardid], player['id']):
		return jsonify({'allow':True}), 200

	return jsonify({'allow':False}), 200


#
#
@app.route('/games/<int:boardid>/status', methods=['GET'])
def boardStatus(boardid):
	if boardid < 0  or boardid > (numGames - 1):
		return jsonify({'err': 'Please enter a board number between 0 and ' + (numGames-1)}), 404

	coords = request.args.get("coords")
	if coords is not None:
		print coords

		#Stringify the board and return it
		boardString = [{}]
		for r in range(0,sideLen):
			for c in range(0,sideLen):
				boardString[0][games[boardid].revert((7-c, 7-r))] = games[boardid].board[r][c]
		return jsonify(boardString[0]), 201

	return jsonify(board=games[boardid].board), 201

if __name__ == '__main__':
	app.run(host='10.10.10.10')
