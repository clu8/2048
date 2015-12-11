import gameState
import agents
import eval
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
    agent = agents.LogisticAgent(False)
    validActions = move.getAllMoves()

    if save_to_csv:
        with data.MoveWriter() as mw:
            return go(mw)
    else:
        return go()

def compare_depth():
    '''
    Plays a game using 2 expectimax agents - one of depth 2 and one of depth 3. 
    Counts the number of moves where their move choices differ. 
    '''
    move = gameState.Move()
    agent2 = agents.ExpectimaxAgent(2)
    agent3 = agents.ExpectimaxAgent(3)
    validActions = move.getAllMoves()

    game = gameState.GameState2048()
    num_moves = 0
    num_disagreements = 0
    while True:
        num_moves += 1

        computerAction = agent3.getAction(game, 1, None)
        if computerAction is None:
            break
        game = game.generateSuccessor(1, computerAction)

        depth2Action = agent2.getAction(game, 0, validActions)
        depth3Action = agent3.getAction(game, 0, validActions)
        if depth3Action is None:
            break

        if depth2Action != depth3Action:
            num_disagreements += 1
            print(game)
            print('Depth 2 move: {}'.format(move.moveString(depth2Action)))
            print('Depth 3 move: {}'.format(move.moveString(depth3Action)))
            print('Agents disagreed on {} of {} moves.\n'.format(num_disagreements, num_moves))

        game = game.generateSuccessor(0, depth3Action)

if __name__ == '__main__':
    print(simulate(10, False, True))
    # compare_depth()