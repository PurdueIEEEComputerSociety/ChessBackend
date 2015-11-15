//Global variable Listing
var turn = 'w';
var position;
var boardID = 1;
var color = 'w';
var playerID = "0";
var playerID2 = "0";
var baseURL = "";
var currentID = "0";
var mode = "S"; //S is for local game (with server checking) M is for multiplayer (1 side)
var intervalKeeper;
 
var onDrop = function(source, target, piece, newPos, oldPos, orientation) {
	// console.log("Source: " + source);
	// console.log("Target: " + target);
	// console.log("Piece: " + piece);
	// console.log("Orientation: " + orientation);
	// console.log("--------------------");
	position = board.position();
	tryMove(source, target, piece[0]);
	//return 'snapback';
};

var cfg = {
	draggable: true,
	onDrop: onDrop,
	sparePieces: false
};

var tryMove = function(source, target, color) {

	$.ajax({
		url: baseURL + "/games/"+boardID+"/move",
		type:"POST",
		data: JSON.stringify({'id': currentID, 'moveFrom': source, 'moveTo': target}),
		contentType:"application/json; charset=utf-8",
		dataType:"json",
		success: function(data){
			board.update();
			turnChange();
		},
		error: function(e) {
			board.position(position);
			board.update();
			console.log("Server returned a "+ e.status +" "+ e.statusText);
			if(e.status == 404) {
				console.log("Board or Page does not exist");
			}
			else if(e.status == 400) {
				console.log("Incorrect Move");
			}
		}
	});
}


var board = ChessBoard('board1', cfg);

var getBoard = function() {
	var statusRequest = $.get( baseURL + "/games/"+boardID+"/status", function(data) {
		board.clear();
		$.each(data, function(key, value){
			if (value == "  " || value == "" || value === null){
				delete data[key];
			}
			// console.log("Key: " + key + " Value: " + value)
		});
		position = data;
		console.log(data);
		board.position(position);
	})
	.done(function() {

	})
	.fail(function() {

	})
	.always(function() {

	});

}

var turnChange = function() { 
	$("#turn").html(($("#turn").html() == "W")? "B":"W");
	if(mode == "S") currentID = (currentID == playerID)? playerID2 : playerID;
	intervalKeeper = setInterval(""); //FINISH THIS INTERVAL CODE WHEN TURN CHECKING IS IMPLEMENTED
}

var switchMode = function() {
	mode = (mode == "S")? "M" : "S";
	//insert code to clear game session here
	board.clear();
	//Temp board change
	boardID = (boardID == 1)? 0 : 1;
	$("#initB").show();
	$("#turn").html("W");
	$("#playerTurn").html("");
}

var initBoard = function() {
	var statusRequest = $.get( baseURL + "/games/"+boardID+"/init", function(data) {
		console.log("Successfully Initialized. ID is " + data.id);
		color = data.color;
		if(mode == "S") {
			playerID = playerID2;
			playerID2 = data.id;
			currentID = playerID;			
		}
		else {
			$("#initB").hide();
			playerID = data.id;
			currentID = data.id;
			$("#playerTurn").html("Your pawn color is " + ((color == "B")?"black":"white"));
			//clear any interval checking
			clearInterval(intervalKeeper);
		}

	})
	.fail(function(e) {
		console.log(e.status);
		if(e.status == 423) console.log("Board has been started and has been locked from new inits.")
	})
}
board.update = getBoard;
board.init = initBoard;

