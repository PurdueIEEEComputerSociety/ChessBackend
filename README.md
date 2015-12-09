# ChessBackend

##Install
You should have Python 2.7.X installed (All Mac OS X machines and some Linux machines comes with this pre-installed)
The flask framework can be installed through Python Package Manager using ```pip install flask; pip install flask-cors```

##Running 
Start the server with ```python server.py```
The server will now be bound to port 5000 on your localhost

##Default Pages
The default pages that exist are accessed at '/' and '/api'. The first is a test landing page to interface with the server and the second is the documentation for requests to be sent to the server

##Usage
Currently the only 2 interactive endpoints are /games/<ID>/move and /games/<ID>/status where <ID> is a value 0-99 which is the id of a game

The move endpoint requires a POST request from the client with a JSON object containing the piece name. We use the code color [W|B] with piece first letter [K|Q|N|B|R|P]. Here knight is N
The 2nd part of the JSON object is our move to location with the breakdown [row 0-8][col 0-8]

At the status endpoint your browser makes a GET request for the status of the specified board, The returned board is a CSV (on |) layout of that board

##Example 
To send a move request through your browser ```curl -i -H "Content-Type: application/json" -X POST -d '{"piece":"WK", "moveTo":"14"}' http://localhost:5000/games/1/move```

To see the move you just made go to [http://localhost:5000/games/1/status](http://localhost:5000/games/1/status).
