//Global variable Listing
var turn = 'w';
var position;
var boardID = 1;
var color = 'w';
var playerID = "1";
var baseURL = ""

var onDrop = function(source, target, piece, newPos, oldPos, orientation) {
	// console.log("Source: " + source);
	// console.log("Target: " + target);
	// console.log("Piece: " + piece);
	// console.log("Orientation: " + orientation);
	// console.log("--------------------");
	position = board.position();
	tryMove(source, target, piece[0]);
	return 'snapback';
};

var cfg = {
	draggable: true,
	position: 'start',
	onDrop: onDrop,
	sparePieces: false
};

var tryMove = function(source, target, color) {
	var moveRequest = $.post( baseURL + "/games/"+boardID+"/move", {id: playerID, moveFrom: source, moveTo: target}, function(data) {
		board.move(source + '-' + target);
	})
	.fail(function(e) {
		console.log("Server returned a "+ e.status +" "+ e.statusText);
		if(e.status == 404) {
			console.log("Board or Page does not exist");
		}
		else if(e.status == 400) {
			console.log("Incorrect Move");
		}
	})
	.always(function() {
		
	});
	
	
}


var board = ChessBoard('board1', cfg);

var getBoard = function() {
	var statusRequest = $.get( baseURL + "/games/"+boardID+"/status", function(data) {
		board.clear();
		position = data;
		console.log(data);
	})
	.done(function() {
		board.position(position);
	})
	.fail(function() {
		
	})
	.always(function() {
		
	});

}

var initBoard = function() {
	var statusRequest = $.get( baseURL + "/games/"+boardID+"/init", function(data) {
		console.log("Successfull Initialized");
	})	
}
