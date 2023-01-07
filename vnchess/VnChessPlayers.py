import numpy as np
from .VnChessUtils import *
from .VnChessGame import VnChessGame

class RandomVnChessPlayer():
    def __init__(self, game):
        self.game = game
    
    def play(self,board):
        '''
        Random agent should return random move in list of valid moves
        '''

        moves = get_all_actions(board.prev_pieces,board.pieces,1)
        assert(isinstance(self.game, VnChessGame))
        start, end = moves[np.random.randint(len(moves))]
        x1, y1 = start
        x2, y2 = end
        return x1 + y1*self.game.n + x2*self.game.n**2 + y2*self.game.n**3
    
class HumanVnChessPlayer():
    def __init__(self, game):
        self.game = game
    def play(self, board):
        moves = get_all_actions(prev_board,board,1)
        res_move = None
        while True:
            move = input("Input move: ")
            move = ''.join(x for x in move if x.isdigit())
            start = (int(move[0]), int(move[1]))
            end = (int(move[2]), int(move[3]))
            move = (start, end)
            if move in moves:
                res_move = move
                break
            else:
                print("invalid move", move)
        return res_move


class GreedyVnChessPlayer():
    def __init__(self, game):
        assert(isinstance(game, VnChessGame))
        self.game = game
    
    def play(self, board):
        # moves = get_all_actions(prev_board, board,player)
        valids = self.game.getValidMoves(board, 1)
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a] == 0:
                continue
            nextBoard, _ = self.game.getNextState(board, 1,a)
            score = self.game.getScore(nextBoard, 1)
            candidates += [(-score, a)]
        candidates.sort()
        return candidates[0][1]
                

        