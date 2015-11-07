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
	//return 'snapback';
};

var cfg = {
	draggable: true,
	onDrop: onDrop,
	sparePieces: false
};

var tryMove = function(source, target, color) {
	// var moveRequest = $.post( baseURL + "/games/"+boardID+"/move", {'id': playerID, 'moveFrom': source, 'moveTo': target}, function(data) {
	// 	board.move(source + '-' + target);
	// })
	// .fail(function(e) {
	// 	console.log("Server returned a "+ e.status +" "+ e.statusText);
	// 	if(e.status == 404) {
	// 		console.log("Board or Page does not exist");
	// 	}
	// 	else if(e.status == 400) {
	// 		console.log("Incorrect Move");
	// 	}
	// })
	// .always(function() {
	// 	console.log(typeof(JSON.stringify({'id': playerID, 'moveFrom': source, 'moveTo': target})))
	// });
	$.ajax({
		url: baseURL + "/games/"+boardID+"/move",
		type:"POST",
		data: JSON.stringify({'id': playerID, 'moveFrom': source, 'moveTo': target}),
		contentType:"application/json; charset=utf-8",
		dataType:"json",
		success: function(data){
			board.update()
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

var initBoard = function() {
	var statusRequest = $.get( baseURL + "/games/"+boardID+"/init", function(data) {
		console.log("Successfull Initialized");
	})
	.fail(function(e) {
		console.log(e.status);
		if(e.status == 423) console.log("Board has been started and has been locked from new inits.")
	})
}
board.update = getBoard;
board.init = initBoard;

