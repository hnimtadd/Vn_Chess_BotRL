'''
Board class:
Board data:
    1=X, -1=O, 0=empty, or something:)))
    first dim is column, 2nd is row:
        pieces[1][3] is the square in column 2,
        at the opposite end of the board in row 4.
Squares are stored and manipulated as (x,y) tuples.
x is the column index, y is the row index.
'''

from .VnChessUtils import *
import numpy as np

class Board():
    def __init__(self, cfg):
        '''
        Set up initial board configuration.
        params: n: size of board
        '''
        self.n = cfg.size
        # Create the empty board array.
        self.prev_pieces = cfg.prev_pieces
        self.player = cfg.player
        self.pieces = cfg.pieces
        self.moves = cfg.moves
    
    #Add [][] indexer syntax to the Board.
    def __getitem__(self, index):
        return self.pieces[index]
    
    def countDiff(self, type):
        '''
        Couts the # piees of the given type chessman
        (1 for X, -1 for O, 0 for empty spaces) or something ;))
        '''
        count = 0
        for i in range(self.n):
            for j in range(self.n):
                if self[i][j] == type:
                    count += 1
                elif self[i][j] == -type:
                    count -= 1
        return count
    
    def get_last_move(self):
        return None if len(self.moves) == 0 else self.moves[-1]

    def get_legal_moves(self, player):
        '''
        Returns all the legal moves for the given chess player.
        (1 for X, -1 for O)
        '''
        return self._getValidMoves(player)

    def _getValidMoves(self, player):
        last_move = self.get_last_move()
        if last_move is not None:
            last_start, _ = last_move
            traps_move = get_traps(self.pieces, player, last_start)
            if len(traps_move) != 0:
                return traps_move

        all_actions = []
        for i in range(self.n):
            for j in range(self.n):
                if self[i][j] == player:
                    actions = get_actions_of_chessman(self.pieces,(i,j))
                    all_actions += [((i,j), blind_move((i,j),action)) for action in actions]
        
        return all_actions
    
    def has_legal_moves(self, player):
        for i in range(self.n):
            for j in range(self.n):
                if self[i][j] == player:
                    newmoves = self.get_moves_for_square((i,j))
                    if len(newmoves) > 0:
                        return True
        return False
    
    def get_moves_for_square(self, square):
        '''
        Returns all legal moves start at index square
        '''
        (x,y) = square
        type = self[x][y]

        #skip empty source squares.
        if type == 0:
            return None
        
        #search all possible directions:
        return get_actions_of_chessman(self.pieces,square)
    
    def execute_move(self, move, player):
        '''
        Perform given move on the board
        '''
        prev_board = self.pieces
        start, end = move
        i, j = start
        if self[i][j] != player:
            raise Exception("Start position is not valid")
        
        # i, j = start
        self[i][j] = 0

        i, j = end
        self[i][j] = player
        
        # Cap nhat ganh, vay
        for action in get_avail_half_actions(end):
            pos1, pos2 = blind_move(end, action), blind_move(end, action.get_opposite())

            type1, type2 = get_at(self.pieces, pos1), get_at(self.pieces, pos2)

            if type1 == type2 == -player:
                i1, j1 = pos1
                i2, j2 = pos2
                self[i1][j1] = player
                self[i2][j2] = player
        surround_teams = get_surrounded_chesses(self.pieces, player)
        self.pieces = surround(self.pieces, surround_teams, player)
        self.prev_pieces = prev_board
    
    # @staticmethod
    # def _increment_move(move, direction, n):
    #     '''
    #     Geneator expression for incrementing moves
    #     '''
    #     move = list(map(sum, zip(move, direction)))

    #     while all(map(lambda x: 0 <= x < n, move)):
    #         yield move
    #         move=list(map(sum,zip(move,direction)))

    def getCopy(self):
        cfg = {
            "size" : self.n,
            "player": self.player,
            "prev_pieces": self.prev_pieces,
            "pieces": self.pieces,
            "move": self.moves
        }
        new_board = Board(cfg)
        return new_board
    
    def getPlayerToMove(self):
        return (self.player)

    def _isLegalMove(self, move):
        return is_valid_move(-self.pieces, self.pieces, self.player, move)
