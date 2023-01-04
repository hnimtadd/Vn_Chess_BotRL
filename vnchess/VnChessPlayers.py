import numpy as np
from VnChessUtils import *
from .VnChessGame import VnChessGame

class RandomVnChessPlayer():
    def __init__(self, game):
        self.game = game
    
    def play(self, prev_board, board, player):
        '''
        Random agent should return random move in list of valid moves
        '''
        moves = get_all_actions(prev_board,board,player)
        move = moves[np.random.randint(len(moves))]
        return move
    
class HumanVnChessPlayer():
    def __init__(self, game):
        self.game = game
    def play(self, prev_board, board, player):
        moves = get_all_actions(prev_board,board,player)
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
    
    def play(self, prev_board, board, player):
        # moves = get_all_actions(prev_board, board,player)
        valids = self.game.getValidMoves(board, board.getPlayerToMove())
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a] == 0:
                continue
            nextBoard, _ = self.game.getNextState(board, board.getPlayerToMove(),a)
            score = self.game.getScore(nextBoard, board.getPlayerToMove())
            candidates += [(-score, a)]
        candidates.sort()
        return candidates[0][1]
                

        