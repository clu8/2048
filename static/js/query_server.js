function query_server(keyboardInput) {
	this.keyboardInput = keyboardInput;

	function repeatedCall() {
		$.get("/move", function(data, status){
			console.log(data);
			keyboardInput.emit("move", data["move"]);
        	repeatedCall();
    	})
	}

	query_server.prototype.repeatedCall = repeatedCall;
}
