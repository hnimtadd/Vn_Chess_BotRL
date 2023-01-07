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
        self.cfg = cfg
        self.n = cfg['size']
        # Create the empty board array.
        self.prev_pieces = cfg['prev_pieces']
        self.pieces = cfg['pieces'] #list(list(int))
        self.done=0
        self.time=0
    def __str__(self):
        return str(self.getPlayerToMove()) +  ''.join(str(r) for v in self.getImage() for r in v) 

    #Add [][] indexer syntax to the Board.
    def __getitem__(self, index):
        return np.array(self.getImage())[index]
    
    # @property
    def _getWinLose(self):
        if self.time > 100: return -1
        
        res = np.sum(self.pieces)
        return 1 if res == 16 else -1 if res == -16 else 0

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
    

    def get_legal_moves(self, player):
        '''
        Returns all the legal moves for the given chess player.
        (1 for O, -1 for X)
        '''
        return get_all_actions(self.prev_pieces, self.pieces, player)
        # return self._getValidMoves(player)

    # def _getValidMoves(self, player):
    #     all_actions = get_all_actions(self.prev_pieces, self.pieces, player)
    #     return all_actions
        # last_move = self.get_last_move()
        # if last_move is not None:
        #     last_start, _ = last_move
        #     traps_move = get_traps(self.pieces, player, last_start)
        #     if len(traps_move) != 0:
        #         return traps_move

        # all_actions = []
        # if len(all_actions)!= 0:

        # for i in range(self.n):
        #     for j in range(self.n):
        #         if self[i][j] == player:
        #             actions = get_actions_of_chessman(self.pieces,(i,j))
        #             all_actions += [((i,j), blind_move((i,j),action)) for action in actions]
    
        # return all_actions #type(start, end)
    
    def has_legal_moves(self, player):
        for i in range(self.n):
            for j in range(self.n):
                if self[i][j] == player:
                    newmoves = self.get_moves_for_square((i,j))
                    if len(newmoves) > 0:
                        return True
        return False
    
    def get_moves_for_square(self, pos):
        '''
        Returns all legal moves start at index square
        '''
        (x,y) = pos
        type = self[x][y]

        #skip empty source squares.
        if type == 0:
            return None
        
        #search all possible directions:
        return get_actions_of_chessman(self.pieces,pos)
    
    def execute_move(self, move, player):
        '''
        Perform given move on the board
        '''
        # print('execute num', self.time)
            # print("End")
            # return
        try:
            assert(self._isLegalMove(move, player))
            # print('accepted move: ', move)
            prev_board = np.copy(np.array(self.pieces))
            start, end = move
            i, j = start
            if self[i][j] != player:
                raise Exception("Start position is not valid")
            
            # i, j = start
            self.pieces[i][j] = 0

            i, j = end
            self.pieces[i][j] = player
            
            # Cap nhat ganh, vay
            for action in get_avail_half_actions(end):
                pos1, pos2 = blind_move(end, action), blind_move(end, action.get_opposite())

                type1, type2 = get_at(self.pieces, pos1), get_at(self.pieces, pos2)

                if type1 == type2 == -player:
                    i1, j1 = pos1
                    i2, j2 = pos2
                    self.pieces[i1][j1] = player
                    self.pieces[i2][j2] = player
            surround_teams = get_surrounded_chesses(self.pieces, player)
            self.pieces = surround(self.pieces, surround_teams, player)
            # self.player *= -1
            self.prev_pieces = prev_board
            self.done = self._getWinLose()
            self.time = self.time + 1
        except:
            # print_board(self.prev_pieces)
            print("illegal")
            if self.prev_pieces is not None:
                print_board(self.prev_pieces)
            print_board(self.pieces)
            print(player)
            print(move)
            print(get_all_actions(self.prev_pieces, self.pieces, player))
            exit()
    
    def getCopy(self):
        cfg = {
            "size" : self.cfg['size'],
            "prev_pieces": np.copy(np.array(self.cfg['prev_pieces'])).tolist(),
            "pieces": np.copy(np.array(self.cfg['pieces'])).tolist(),
        }
        new_board = Board(cfg)
        new_board.time = self.time
        new_board.done = self.done
        return new_board
    
    def getPlayerToMove(self):
        return -(self.time%2*2-1)

    def _isLegalMove(self, move, player):
        return is_valid_move(self.prev_pieces, self.pieces, player, move)

    def tostring(self):
        xchar = {
            '1':'w',
            '-1':'b',
            '0':'p'
        }
        if self.prev_pieces is not None:
            strr = ' '.join(''.join([xchar[str(char)] for char in row]) for row in self.prev_pieces)\
                 + ' '.join(''.join([xchar[str(char)] for char in row]) for row in self.pieces)\
                 + ' \\{}'.format(xchar[str(self.getPlayerToMove())])
            return strr
        strr = ' '.join(''.join([xchar[str(char)] for char in row]) for row in self.pieces) + ' \\{}'.format(xchar[str(self.getPlayerToMove())])
        return strr
    
    def astype(self, t):
        arr =  np.array(self.getImage()).astype(t)
        return arr

    def getImage(self):
        return self.pieces

if __name__ == "__main__":
    cfg = {
        'size': 5,
        'pieces': np.array([[ 1,  1,  1,  1,  1],
                            [ 1,  0,  0,  0,  1],
                            [ 1,  0,  0,  0, -1],
                            [-1,  0,  0,  0, -1],
                            [-1, -1, -1, -1, -1]]),
        'prev_pieces': None,
        'player': 1,
        'moves':[]

    }
    b = Board(cfg)
    print(((1,2),(1,1)) in b.get_legal_moves(1))