from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .VnChessLogic import Board
from .VnChessUtils import *
import numpy as np
from .Digit import int2base 
# Index action space to 5 * 5 = 25 size array.

class VnChessGame(Game):
    square_content = {
        -1: "X",
         0: "-",
         1: "O"
    }




    @staticmethod
    def getSquarePiece(piece):
        return VnChessGame.square_content[piece]

    def __init__(self, cfg = None):
        self.cfg = cfg
        self.n = cfg['size']
        self.getInitBoard()
    
    def getInitBoard(self):
        # print(self.cfg)
        cfg = {
            'size': 5,
            'prev_pieces': None,
            'player': 1,
            'pieces': np.array(get_init_board()),
        }
        b = Board(cfg)
        # print(b.tostring())
        # exit()
        return b
    
    def getBoardSize(self):
        #Returns shape (a, b) tuple
        return (self.n, self.n)
    
    def getActionSize(self):
        # Return number of maximum actions can get from board
        return self.n**4

    def getNextState(self, board, player, action):
        # if player takes action, on board, return next (board, player)
        # Action must be a valid move
        # Action is array (flatten)
        b = board.getCopy()
        move = int2base(action, self.n, 4)
        start = (move[0], move[1])
        end = (move[2], move[3])
        move = (start, end)
        b.execute_move(move, player)
        return (b, -player)

    def getValidMoves(self, board, player):
        # Return fixed size vector
        valids = [0] * self.getActionSize()
        assert(isinstance(board, Board))
        b = board.getCopy()
        legal_moves = b.get_legal_moves(player)
        
        if len(legal_moves) == 0:
            valids[-1]=1
            return np.array(valids)
        for move in legal_moves:
            start, end = move
            x1, y1 = start
            x2, y2 = end
            valids[x1+y1*self.n+x2*self.n**2+y2*self.n**3]=1
        return np.array(valids)

    def getGameEnded(self, board, player):
        '''
        Return result of game played.
        0 indicated not end
        1 if player 1 won,
        -1 if player 1 lost
        player = 1
        '''
        return board.done*player
        # board_results = np.sum(board)
        # return -1 if board_results == -1 else 1 if board_results == 1 else 0
    def AreaGameEnd(self, board, player):
        res = np.sum(board.pieces)
        return res == 16 or res == -16
    def getCanonicalForm(self, board, player):
        '''
        Return state of player view
        '''
        assert(isinstance(board, Board))
        cfg = {
            'size': board.n,
            'prev_pieces': np.copy(np.array(board.prev_pieces))*player if board.prev_pieces is not None else None,
            'pieces': np.copy(np.array(board.pieces))*player,
        }
        new_board = Board(cfg)
        new_board.time = board.time
        new_board.done = board.done
        return new_board
    
    def getSymmetries(self, board, pi):
        return [(board,pi)]
    
    def stringRepresentation(self, board):
        return board.tostring()

    def stringRepresentationReadable(self, board):
        # board_s = "".join(self.square_content[square] for row in board for square in row)
        return self.stringRepresentation(board)
    
    
    def getScore(self, board, player):
        '''
        init of q value
        '''
        assert(isinstance(board, Board))
        if board.done: return 1000*board.done*player + 1000/(board.time + 1)
        # opp_move = get_avail_moves(board.pieces, -player)
        return board.countDiff(player)
        #  + 1/(len(opp_move) + EPS)


    
    @staticmethod
    def display(board):
        board = np.array(board.pieces)
        n = board.shape[0]
        print("   ", end = "")
        for y in range(n):
            print(y, end = " ")
        print("")
        print("---"*5)
        for y in range(n):
            print(y, "|", end="")
            for x in range(n):
                piece = board[y][x] #get the piece to print
                print(VnChessGame.square_content[piece], end=" ")
            print("|")
        print("---"*5)
EPS = 1e-8