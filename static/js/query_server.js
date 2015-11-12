/* Communicator between simulator and AI server.
 * Before each move, query_selector will send HTTP
 * request ~/move on server, send the grid layout
 * after the last move, and wait to get the next move
 * command from the server.
 * TODO: add end-game handling
 * TODO: add high score handling
 */
function query_server(keyboardInput) {
	this.keyboardInput = keyboardInput;

	// Function that will be called repeatedly to play the game
	function repeatedCall() {
		$.get("/move", function(data, status){
			// Data: {"move": int}
			// 0: up, 1: right, 2: down, 3: left
			keyboardInput.emit("move", data["move"]);
        	repeatedCall();
    	})
	}

	query_server.prototype.repeatedCall = repeatedCall;
}
