       
"""
Stores the information of a move
"""

class Move():
    CONV_RANK_TO_ROWS = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    CONV_FILES_TO_COLS = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    CONV_ROWS_TO_RANK = {7: "1", 6:"2", 5:"3", 4:"4", 3:"5", 2:"6", 1:"7", 0:"8"}
    CONV_COLS_TO_FILES = {7: "h", 6:"g", 5:"f", 4:"e", 3:"d", 2:"c", 1:"b", 0:"a"}
    
    
    def __init__(self, fromSquare: tuple[int, int], toSquare: tuple[int, int], board: list[list[str]]):
        self.fromRow = fromSquare[0]
        self.fromCol = fromSquare[1]
        self.toRow = toSquare[0]
        self.toCol = toSquare[1]
        
        self.pieceMoved = board[self.fromRow][self.fromCol]
        self.pieceCaptured = board[self.toRow][self.toCol]

    
    def convertToChessNotation(self) -> str:
        return self.convertToRankFile(self.fromRow, self.fromCol) + self.convertToRankFile(self.toRow, self.toCol)
    
        
    def convertToRankFile(self, row, col) -> str:
        return self.CONV_COLS_TO_FILES[col] + self.CONV_ROWS_TO_RANK[row]
        
    def convertToRowCol(self, rank, file) -> list[int]:
        return [self.CONV_RANK_TO_ROWS[rank], self.CONV_FILES_TO_COLS[file]]
            
        
    def __str__(self) -> str:
        return self.convertToChessNotation()
    
    def __eq__(self, other) -> bool:
        if str(self) == str(other):
            return True
        return False
        
        
    
"""
Stores the information about the current state of a chess game.
Determines the valid moves for the current gamestate.

TODO: Use numpy for faster processing, especially when implementing AI engine
"""

class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        
        self.whiteToMove = True
        self.moveLog = []
        
            
    def move(self, move: Move) -> None:
        self.board[move.fromRow][move.fromCol] = "--"
        self.board[move.toRow][move.toCol] = move.pieceMoved
        
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if self.whiteToMove:
            print("Whites turn.")
        else:
            print("Blacks turn.")
        
    '''
    Undoes the most recent move
    '''
    def undoMove(self) -> None:
        if len(self.moveLog) == 0:
            print("No move to undo")
            return
        move: Move = self.moveLog.pop()
        self.board[move.fromRow][move.fromCol] = move.pieceMoved
        self.board[move.toRow][move.toCol] = move.pieceCaptured
        
        self.whiteToMove = not self.whiteToMove
        
    '''
    Gets all the possible moves without considering checks.
    '''
    def getAllMoves(self) -> list[Move]:
        move_list: list[Move] = []
        
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                
                piece = self.board[row][col]
                if piece == "--":
                    continue
                
                if GameState.pieceIsWhite(piece):
                    if self.whiteToMove == True:

                        move_list.extend(self.getMoves(piece, row, col))
                    
                elif not GameState.pieceIsWhite(piece):
                    if self.whiteToMove == False:
                        
                        move_list.extend(self.getMoves(piece, row, col))
        

        return move_list
        
    def getMoves(self, piece, row: int, col: int) -> list[Move]:
        piece_type = GameState.getPieceType(piece)
        if piece_type == 'P':
            return self.getPawnMoves(row, col)
        elif piece_type == 'B':
            return self.getBishopMoves(row, col)
        elif piece_type == 'N':
            return self.getKnightMoves(row, col)
        elif piece_type == 'R':
            return self.getRookMoves(row, col)
        elif piece_type == 'Q':
            return self.getQueenMoves(row, col)
        elif piece_type == 'K':
            return self.getKingMoves(row, col)
        
        return []
        
    '''
    Gets the legal pawn moves given a pawn at a given row and col.
    A legal move for a pawn includes:
        - Moving forward 2 spaces if the pawn is on its starting square
        - Move forward 2 spaces if there is no piece in front of it
        - Capture an opposing piece diagonally
        - TODO: En-passant move
    '''
    def getPawnMoves(self, row: int, col: int) -> list[Move]:
        moves: list[Move] = []
        
        if self.whiteToMove == True:
            if not self.hasPiece(row-1, col):
                moves.append(Move((row, col), (row-1, col), self.board))
            
            
            if self.pawnOnStartingSquare(row, col) and not self.hasPiece(row-2, col):
                fromSquare = (row, col)
                toSquare = (row-2, col)
                moves.append(Move(fromSquare, toSquare, self.board))
            
            # capture diagonally to the left 
            if self.hasPiece(row-1, col-1):
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            # capture diagonally to the right
            if self.hasPiece(row-1, col+1):
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))
                
                
        if self.whiteToMove == False:
            if not self.hasPiece(row+1, col):
                moves.append(Move((row, col), (row+1, col), self.board))
            
            if self.pawnOnStartingSquare(row, col) and not self.hasPiece(row+2, col):
                fromSquare = (row, col)
                toSquare = (row+2, col)
                moves.append(Move(fromSquare, toSquare, self.board))
                
            # capture diagonally to the left 
            if self.hasPiece(row+1, col-1):
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            # capture diagonally to the right
            if self.hasPiece(row+1, col+1):
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col+1), self.board))
                
        
        return moves
    
    '''
    Gets the legal Bishop moves given a row and col position
    A legal move for a bishop includes:
        - Moving diagonally in each direction until blocked by a friendly piece
        - Capturing an enemy piece at the end of a diagonal if one exists
    '''
    def getBishopMoves(self, row: int, col: int) -> list[Move]:
        moves: list[Move] = []
        
        # directions of the diagonals, 
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        
        for direction in directions:
            for i in range(1, len(self.board)):
                    
                toRow = row + direction[0]*i
                toCol = col + direction[1]*i
                if not self.isInBoard(toRow, toCol):
                    # we've gone off the board in this direction!
                    break
                    
                if self.hasPiece(toRow, toCol):
                    if self.pieceIsWhite(self.board[toRow][toCol]):
                        if self.whiteToMove:
                            break
                        else: 
                            moves.append(Move((row, col), (toRow, toCol), self.board))
                            break
 
                    else:
                        if self.whiteToMove:
                            moves.append(Move((row, col), (toRow, toCol), self.board))
                            break
                        else:
                            break
                        
                # no piece blocking our bishop
                moves.append(Move((row, col), (toRow, toCol), self.board))
                            
        
        return moves    
    
    '''
    Gets the legal Knight moves given a row and col position
    A legal move for a knight includes:
        - Moving in an 'L' Shape in 8 different directions
    '''
    def getKnightMoves(self, row: int, col: int) -> list[Move]:
        moves: list[Move] = []
        
        directions = ((-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1))
        
        for direction in directions:
            toRow = row + direction[0]
            toCol = col + direction[1]
            
            if not self.isInBoard(toRow, toCol):
                continue
            
            if self.hasPiece(toRow, toCol):
                if self.board[toRow][toCol][0] == 'w':
                    if not self.whiteToMove:
                        moves.append(Move((row, col), (toRow, toCol), self.board))
                        
                else: 
                    # piece is black
                    if self.whiteToMove:
                        moves.append(Move((row, col), (toRow, toCol), self.board))
                continue
            
            # no piece
            moves.append(Move((row, col), (toRow, toCol), self.board))
                    
        return moves      
    
    
    '''
    Gets the legal Rook moves given a row and col position
    A legal move for a Rook includes:
        - Moving horizontally along the same row until blocked by a piece
        - Moving vertically along the same column until blocked by a piece 
        - TODO: castling
    '''
    def getRookMoves(self, row: int, col: int) -> list[Move]:
        moves: list[Move] = []
        
        
        directions = ((0, -1), (0, 1), (1, 0), (-1, 0))

        for direction in directions:
            for j in range(1, len(self.board)):
                toRow = row + direction[0]*j
                toCol = col + direction[1]*j
                
                if not self.isInBoard(toRow, toCol):
                    break
                
                if self.hasPiece(toRow, toCol):
                    pieceColor = self.board[toRow][toCol][0]
                    if self.whiteToMove:
                        if pieceColor != 'w':
                            moves.append(Move((row, col), (toRow, toCol), self.board))
                    else:
                        if pieceColor == 'w':
                            moves.append(Move((row, col), (toRow, toCol), self.board))
                    break
                
                # no piece
                moves.append(Move((row, col), (toRow, toCol), self.board))

        return moves      
    
    '''
    A combination of the rooks and bishop moves.
    '''
    def getQueenMoves(self, row: int, col: int) -> list[Move]:
        moves: list[Move] = []
        
        moves.extend(self.getBishopMoves(row, col))
        moves.extend(self.getRookMoves(row, col))
        
        return moves 
    
    '''
    Gets the legal King moves given a row and col position
    A legal move for a king includes:
        - Moving one space in any direction
        - TODO: Not moving into check
    '''
    def getKingMoves(self, row: int, col: int) -> list[Move]:
        moves: list[Move] = []
        
        directions = (-1, 0, 1)
        
        for r in directions:
            for c in directions:
                toRow = row + r
                toCol = col + c
                                
                if not self.isInBoard(toRow, toCol):
                    continue
                
                if self.hasPiece(toRow, toCol):
                    pieceColor = self.board[toRow][toCol][0]
                    if self.whiteToMove:
                        if pieceColor == 'b':
                            moves.append(Move((row, col), (toRow, toCol), self.board))
                    else:
                        if pieceColor == 'w':
                            moves.append(Move((row, col), (toRow, toCol), self.board))
                    continue
                
                # no piece 
                moves.append(Move((row, col), (toRow, toCol), self.board))

        return moves      
         
    '''
    Checks if a pawn is on it's starting square given a row and col indexes
    '''
    def pawnOnStartingSquare(self, row: int, col: int) -> bool:
        if self.whiteToMove == True:
            if row == 6:
                return True
            return False
        else:
            if row == 1:
                return True
            return False
        
    '''
    Checks if this square has a piece on it.
    '''
    def hasPiece(self, row, col) -> bool:
        if row < 0 or row >= 8:
            return False
        if col < 0 or col >= 8:
            return False
        if self.board[row][col] == "--":
            return False
        return True
       
    '''
    Checks if the given row and col cooresponds to a square on the board
    ''' 
    def isInBoard(self, row, col) -> bool:
        if row >= 8 or row < 0 or col >= 8 or col < 0:
            return False
        return True
        
        
    @staticmethod
    def pieceIsWhite(piece: str) -> bool:
        if piece[0] == 'w':
            return True
        return False
    
    @staticmethod
    def getPieceType(piece: str) -> str:
        return piece[1]