import logging

from tqdm import tqdm
from vnchess.Digit import int2base
log = logging.getLogger(__name__)


class Arena():
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, player1, player2, game, display=None):
        """
        Input:
            player 1,2: two functions that takes board as input, return action
            game: Game object
            display: a function that takes board as input and prints it (e.g.
                     display in othello/OthelloGame). Is necessary for verbose
                     mode.

        see othello/OthelloPlayers.py for an example. See pit.py for pitting
        human players/other baselines with each other.
        """
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.display = display

    def playGame(self, verbose=False, threshold=300):
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """
        players = [self.player2, None, self.player1]
        curPlayer = 1
        board = self.game.getInitBoard()
        it = 0
        while self.game.AreaGameEnd(board, curPlayer) == 0 and it < threshold:
            it += 1
            can_board = self.game.getCanonicalForm(board, curPlayer)
            action = players[curPlayer + 1](can_board)
            valids = self.game.getValidMoves(can_board, 1)

            if valids[action] == 0:
                from vnchess.Digit import int2base
                from vnchess.VnChessUtils import get_all_actions
                print('Action', int2base(action, self.game.n, 4), 'is not valid!')
                print('valid actions: ', get_all_actions(can_board.prev_pieces, can_board.pieces, 1))
                exit()
                assert valids[action] > 0
            board, curPlayer = self.game.getNextState(board, curPlayer, action)
            if verbose:
                assert self.display
                from vnchess.Digit import int2base
                print("Taked action", int2base(action, self.game.n, 4))
                print("Turn ", str(it), "Player ", str(curPlayer))
                self.display(board)
        if verbose:
            assert self.display
            print("Game over: Turn ", str(it), "Result ", str(self.game.getGameEnded(board, 1)))
            self.display(board)
        if it > 300:
            return 0
        return curPlayer * self.game.getGameEnded(board, curPlayer)

    def playGames(self, num, verbose=False, threshold = 300):
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.

        Returns:
            oneWon: games won by player1
            twoWon: games won by player2
            draws:  games won by nobody
        """

        num = int(num / 2)
        oneWon = 0
        twoWon = 0
        draws = 0
        for _ in tqdm(range(num), desc="Arena.playGames (1)"):
            gameResult = self.playGame(verbose=verbose, threshold = threshold)
            if gameResult == 1:
                oneWon += 1
            elif gameResult == -1:
                twoWon += 1
            else:
                draws += 1

        self.player1, self.player2 = self.player2, self.player1

        for _ in tqdm(range(num), desc="Arena.playGames (2)"):
            gameResult = self.playGame(verbose=verbose, threshold = threshold)
            if gameResult == -1:
                oneWon += 1
            elif gameResult == 1:
                twoWon += 1
            else:
                draws += 1

        return oneWon, twoWon, draws
