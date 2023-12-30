from constants import *
from piece import *
from game import *


"""
The board class defines the physical board that is used for the game of chess. 
    - A board is full of alternating black and white squares.
    - Squares potentailly have pieces on them.
"""
class Board:
    # initalizes the board full of squares 
    def __init__(self, board=None):
        if board != None:
            self.board = board
            return
        
        self.board = []

        
        # initalize all the squares
        for i in range(8):
            currentRow = []
            for j in range(8):
                colorSelection = COLORS[0] if (i+j)%2 == 0 else COLORS[1]
                currentRow.append(Square(label=LETTERS[j]+str(8-i), color=colorSelection))     
            self.board.append(currentRow)
            
        # add the pieces to the default squares   
        for i in range(8):
            # add all the pawns
            self.board[1][i].addPiece(Pawn(PIECE_NAMES[0], COLORS[1], self.board[1][i].getLabel()))
            self.board[6][i].addPiece(Pawn(PIECE_NAMES[0], COLORS[0], self.board[6][i].getLabel()))    
           
        # add the black back rows
        self.board[0][0].addPiece(Rook(PIECE_NAMES[3], COLORS[1], self.board[0][0].getLabel()))
        self.board[0][7].addPiece(Rook(PIECE_NAMES[3], COLORS[1], self.board[0][7].getLabel()))
        self.board[0][1].addPiece(Knight(PIECE_NAMES[1], COLORS[1], self.board[0][1].getLabel()))
        self.board[0][6].addPiece(Knight(PIECE_NAMES[1], COLORS[1], self.board[0][6].getLabel()))
        self.board[0][2].addPiece(Bishop(PIECE_NAMES[2], COLORS[1], self.board[0][2].getLabel()))
        self.board[0][5].addPiece(Bishop(PIECE_NAMES[2], COLORS[1], self.board[0][5].getLabel()))
        self.board[0][3].addPiece(Queen(PIECE_NAMES[4], COLORS[1], self.board[0][3].getLabel()))
        self.board[0][4].addPiece(King(PIECE_NAMES[5], COLORS[1], self.board[0][4].getLabel()))
            
        # add the white back rows
        self.board[7][0].addPiece(Rook(PIECE_NAMES[3], COLORS[0], self.board[7][0].getLabel()))
        self.board[7][7].addPiece(Rook(PIECE_NAMES[3], COLORS[0], self.board[7][7].getLabel()))
        self.board[7][1].addPiece(Knight(PIECE_NAMES[1], COLORS[0], self.board[7][1].getLabel()))
        self.board[7][6].addPiece(Knight(PIECE_NAMES[1], COLORS[0], self.board[7][6].getLabel()))
        self.board[7][2].addPiece(Bishop(PIECE_NAMES[2], COLORS[0], self.board[7][2].getLabel()))
        self.board[7][5].addPiece(Bishop(PIECE_NAMES[2], COLORS[0], self.board[7][5].getLabel()))
        self.board[7][3].addPiece(Queen(PIECE_NAMES[4], COLORS[0], self.board[7][3].getLabel()))
        self.board[7][4].addPiece(King(PIECE_NAMES[5], COLORS[0], self.board[7][4].getLabel()))
            
        
    """
    Creates an empty board with just squares.
    """
    def createEmptyBoard():
        # initalize all the squares
        board = []
        for i in range(8):
            currentRow = []
            for j in range(8):
                colorSelection = COLORS[0] if (i+j)%2 == 0 else COLORS[1]
                currentRow.append(Square(label=LETTERS[j]+str(8-i), color=colorSelection))     
            board.append(currentRow)
            
        return board
    
            
    # returns the current board
    def getBoard(self):
        return self.board
    
    # Return the square with the given label
    def getSquare(self, label):
        index = self.toIndexes(label)
        
        return self.board[index[0]][index[1]]
    
    
    def toIndexes(self, label) -> (int, int):
        if (len(label) != 2):
            print("Board coordiantes out of range...")
            return -1
        label = label.lower()
        col = -1
        # get the col
        for i, letter in enumerate(LETTERS):
            if label[0] == letter:
                col = i
                
        row = 8 - int(label[1]) 
        
        return (row, col)
    
    
    
    """
    Finds a square given a piece abbreviation and a color.
    Ex. 'K'
    """
    def findSquare(self, pieceAbb, color):
        if pieceAbb not in PIECE_ABB:
            print("DEBUG: piece abbreviation not correct")
            return None
        
        for row in self.board:
            for square in row:
                if(square.hasPiece()):
                    if(square.piece.color == color):
                        if(str(square.piece) == pieceAbb):
                            return square
                        
        print("DEBUG: could not find piece")
        
    
    
    """
    Returns a deep copy of the current game board
    """
    def copy(self):
        new_board = []
        
        for row in self.board:
            new_row = []
            for square in row:
                new_row.append(square.copy())
            new_board.append(new_row)
            
        board_copy = Board(new_board)    
            
        return board_copy
            
    
    
class Square:
    def __init__(self, label, color, piece=None):
        self.label = label 
        self.color = color
        self.piece = piece
        
    def __str__(self):
        if self.piece == None:
            return " "
        return str(self.piece)
    
    def getLabel(self):
        return self.label
    
    
    # adds a piece to the square
    def addPiece(self, piece):
        self.piece = piece
        
        
    # remove a piece from the square
    def removePiece(self):
        pieceCopy = self.piece    
        self.piece = None
        return pieceCopy    
    
    def hasPiece(self):
        if(self.piece == None):
            return False
        return True
    
    def copy(self):
        piece_copy = self.piece.copy() if self.hasPiece() else None
        return Square(self.label, self.color, piece_copy)