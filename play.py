import gameState
import agents
import data

def run(board, score):
    move = gameState.Move()
    game = gameState.GameState2048()
    game.board = board
    game.score = score
    agent = agents.ExpectimaxAgent()
    validActions = move.getAllMoves()
    while True:
        humanAction = agent.getAction(game, 0, validActions)
        if humanAction is None:
            return None
        newgame = game.generateSuccessor(0, humanAction)
        if game.board != newgame.board:
            return humanAction
        else:
            validActions.remove(humanAction)

def simulate(num_games=1, save_to_csv=False, verbose=False):
    '''
    Returns list of (score, num_moves) tuples.
    If save_to_csv is set to True, it saves each board state and the recommended move using MoveWriter. 
    '''
    def go(mw=None):
        results = []
        for _ in range(num_games):
            game = gameState.GameState2048()
            num_moves = 0
            while True:
                num_moves += 1

                computerAction = agent.getAction(game, 1, None)
                if computerAction is None:
                    break
                game = game.generateSuccessor(1, computerAction)

                humanAction = agent.getAction(game, 0, validActions)
                if humanAction is None:
                    break
                if verbose:
                    print(game)
                    print('Agent move: {}\n'.format(move.moveString(humanAction)))
                if mw is not None:
                    mw.write_move(game.board, humanAction)

                game = game.generateSuccessor(0, humanAction)

            print(game)
            results.append((game.score, num_moves))
        return results

    move = gameState.Move()
    agent = agents.ExpectimaxAgent()
    validActions = move.getAllMoves()

    if save_to_csv:
        with data.MoveWriter() as mw:
            return go(mw)
    else:
        return go()

if __name__ == '__main__':
    print(simulate(5, True, False))