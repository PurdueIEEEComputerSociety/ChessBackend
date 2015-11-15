//Global variable Listing
var turn = 'w'; //Keep track of what color's turn it is.
var position; //Keep a local account of the board.
var boardID = 1; 
var color = 'w';
var playerID = "0"; //IDs for local games to switch back and forth.
var playerID2 = "0";
var baseURL = ""; //Base url for requests
var currentID = "0"; //Working ID
var mode = "S"; //S is for local game (with server checking) M is for multiplayer (1 side)
var intervalKeeper; //Keeps track of interval polling for turn checking.
var allowed = true;
var waiting = false;
function onDrop(source, target, piece, newPos, oldPos, orientation) {
	// console.log("Source: " + source);
	// console.log("Target: " + target);
	// console.log("Piece: " + piece);
	// console.log("Orientation: " + orientation);
	// console.log("--------------------");
	position = board.position();
	tryMove(source, target);
	//return 'snapback';
};

var cfg = {
	draggable: true,
	onDrop: onDrop,
	sparePieces: false
};


//---------------------------------------
//
// tryMove makes an attempt to move a chess piece from point A to B [source to target]. 
// The ajax call takes in the user's ID, source, and destination locations. The server takes care of the rest.
//
//---------------------------------------
function tryMove(source, target) {

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


//---------------------------------------
//
// getBoard or board.update attempts to get the current board configuration from the server. This is just the locations of all the pieces.
// To cleanse the data from any empty spaces, the code iterates through all listings and gets rid of any with empty or 2 spaced strings. 
//
//---------------------------------------

function getBoard() {
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
	.done(function() { //Get rid of these eventually [below]

	})
	.fail(function() {

	})
	.always(function() {

	});

}

//---------------------------------------
//
// turnChange or board.turnChange changes the local declaration of what turn it is. It will change html elements and clears any polling intervals
//
//---------------------------------------

function turnChange() { 
	$("#turn").html(($("#turn").html() == "W")? "B":"W");
	if(mode == "S") currentID = (currentID == playerID)? playerID2 : playerID;
	else {
		turnWait();
	}
}

//---------------------------------------
//
// switchMode or board.switchMode changes from singleplayer and multiplayer games. This is local code only, and shouldn't be a part of the AI (should always act like multiplayer)
//
//---------------------------------------

function switchMode() {
	mode = (mode == "S")? "M" : "S";
	//insert code to clear game session here
	board.clear();
	$("#turn").html("W");
	$("#playerTurn").html("");
	//Temp board change SHOULD GET FROM SERVER EVENTUALLY
	boardID = (boardID == 1)? 0 : 1;
	$("#initB").show();
	clearInterval(intervalKeeper);

}

//---------------------------------------
//
// initBoard or board.init requests a handshake from the server for a given boardID. Once 2 players request this and get their IDs, the game will begin.
//
//---------------------------------------

function initBoard() {
	var statusRequest = $.get( baseURL + "/games/"+boardID+"/init", function(data) {
		console.log("Successfully Initialized. ID is " + data.id);
		color = data.color;
		if(mode == "S") {
			playerID = playerID2;
			playerID2 = data.id;
			currentID = playerID;		
			clearInterval(intervalKeeper);	
		}
		else {
			$("#initB").hide();
			playerID = data.id;
			currentID = data.id;
			$("#playerTurn").html("Your pawn color is " + ((color == "B")?"black":"white"));
			//clear any interval checking
			clearInterval(intervalKeeper);
			turnWait();
		}

	})
	.fail(function(e) {
		console.log(e.status);
		if(e.status == 423) console.log("Board has been started and has been locked from new inits.")
	})
}

function turnWait() {
	allowed = false;
	intervalKeeper = setInterval(function() {
		if(!waiting) {
			if(allowed) {
				$("#turn").html("It is your turn.");
				board.update();
				allowed = false;
				clearInterval(intervalKeeper);
			}
			else checkTurn();
		}

	},30);
}

function checkTurn() {
	waiting = true;
	$.ajax({
		url: baseURL + "/games/"+boardID+"/turn",
		type:"POST",
		data: JSON.stringify({'id': currentID}),
		contentType:"application/json; charset=utf-8",
		dataType:"json",
		success: function(data){
			//console.log(data);
			if(data.allow) {
				allowed = true;
			}
			else {
				allowed = false;
			}
			waiting = false;
		},
		error: function(e) {
		}
	});
}

//Board Initialization
var board = ChessBoard('board1', cfg);
board.update = getBoard;
board.init = initBoard;
board.switchMode = switchMode;
board.turnChange = turnChange;

