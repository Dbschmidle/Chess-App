
"""
The board class defines the physical board that is used for the game of chess. 
    - A board is full of alternating black and white squares.
    
"""
class Board:
    # initalizes the board full of squares 
    def __init__(self):
        self.board = []

        
        # initalize all the squares
        for i in range(8):
            currentRow = []
            for j in range(8):
                colorSelection = COLORS[0] if is_even(i + j) else COLORS[1]
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
            
            
    # returns the current board
    def getBoard(self):
        return self.board
    
    # Return the square with the given label
    def getSquare(self, label):
        index = toIndexes(label)
        
        return self.board[index[0]][index[1]]