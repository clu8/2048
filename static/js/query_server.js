/* Communicator between simulator and AI server.
 * Before each move, query_selector will send HTTP
 * request ~/move on server, send the grid layout
 * after the last move, and wait to get the next move
 * command from the server.
 * TODO: add end-game handling
 * TODO: add high score handling
 * TODO: handle human manual input
 */
function query_server(gameManager) {
	this.gameManager = gameManager;

	// Function that will be called repeatedly to play the game
	function repeatedCall(layout) {
		layout_serialize = JSON.stringify(parseLayout(layout));
		//console.log(layout_serialize);
		$.get("/move?layout=" + layout_serialize, function(data, status){
			// data: {"move": move_int}
			// move_int:
			// 		0: up, 1: right, 2: down, 3: left
			console.log(data);
			// console.assert(data["move"], "Algorithm output format error. Data should contain field \"move\", an integer between >=0 and <=3.");
			layout = gameManager.move(data["move"]);
        	repeatedCall(layout);
    	})
	}

	/* Raw layout format:
	    grid:        this.grid.serialize(),
			- cells: [Tile[4], Tile[4], Tile[4], Tile[4]]
			    - Tile:
					position:
			    	    x: int range(0:4)
			    	    y: int range(0:4)
			    	value: int
    	score:       this.score,
    	over:        this.over,
    	won:         this.won,
    	keepPlaying: this.keepPlaying
		===================================================================
    	Parsed to the following format:
    	grid: 		[int[4], int[4], int[4], int[4]], (0 if no grid present)
    	score: 		int
	 */
	function parseLayout(layout) {
		data = {};
		data.score = layout.score;
		data.grid = [[], [], [], []];
		console.log(layout);
		/* layout.grid.cells.forEach(function(tileRow) {
			row = [];
			tileRow.forEach(function(tile) {
				if (tile)
					row.push(tile.value);
				else
					row.push(0);
			});
			data.grid.push(row);
		});*/
		for (i = 0; i < layout.grid.size; i++) {
			for (j = 0; j < layout.grid.size; j++) {
				if (layout.grid.cells[i][j])
					data.grid[j].push(layout.grid.cells[i][j].value);
				else
					data.grid[j].push(0);
			}
		}
		return data;
	}

	query_server.prototype.repeatedCall = repeatedCall;
}
