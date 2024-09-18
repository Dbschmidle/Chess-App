'''
Stores the information of a move, as well as a reference to the board gamestate.
'''
class Move():
    CONV_RANK_TO_ROWS = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    CONV_FILES_TO_COLS = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    CONV_ROWS_TO_RANK = {7: "1", 6:"2", 5:"3", 4:"4", 3:"5", 2:"6", 1:"7", 0:"8"}
    CONV_COLS_TO_FILES = {7: "h", 6:"g", 5:"f", 4:"e", 3:"d", 2:"c", 1:"b", 0:"a"}
    
    
    def __init__(self, fromSquare: tuple[int, int], toSquare: tuple[int, int], board: list[list[str]], enpassantMove = False, castling = False):
        self.fromRow = fromSquare[0]
        self.fromCol = fromSquare[1]
        self.toRow = toSquare[0]
        self.toCol = toSquare[1]
        
        self.pieceMoved = board[self.fromRow][self.fromCol]
        self.pieceCaptured = board[self.toRow][self.toCol]
        
        if (self.pieceMoved == 'bP' and self.toRow == 7) or (self.pieceMoved == 'wP' and self.toRow == 0):
            self.pawnPromotionMove = True
        else:
            self.pawnPromotionMove = False
        
        if enpassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'
            
        self.enpassantMove = enpassantMove
        
        self.castling = castling
        
        
        
    '''
    Converts the move to a psuedo-chess notation format
        - ex. (6, 4), (4, 4) -> e2e4
    '''
    def convertToChessNotation(self) -> str:
        return self.convertToRankFile(self.fromRow, self.fromCol) + self.convertToRankFile(self.toRow, self.toCol)
    
        
    def convertToRankFile(self, row, col) -> str:
        return self.CONV_COLS_TO_FILES[col] + self.CONV_ROWS_TO_RANK[row]
        
    def convertToRowCol(self, rank, file) -> list[int]:
        return [self.CONV_RANK_TO_ROWS[rank], self.CONV_FILES_TO_COLS[file]]
            
        
    def __str__(self) -> str:
        return self.convertToChessNotation()
    
    '''
    Used to compare moves
    '''
    def __eq__(self, other) -> bool:
        if str(self) == str(other):
            return True
        return False
        
        
class CastleRights():
    def __init__(self, wks: bool, bks: bool, wqs: bool, bqs: bool):
        self.wKingSide: bool = wks
        self.wQueenSide: bool = wqs
        self.bKingSide: bool = bks
        self.bQueenSide: bool = bqs
    
    '''
    Returns a deep copy of the Castling rights instance.
    '''
    def deep_copy(self):
        deepcopy = CastleRights(self.wKingSide, self.bKingSide, self.wQueenSide, self.bQueenSide)
        return deepcopy
    
    
    def __str__(self):
        return str(self.wKingSide)+", "+str(self.wQueenSide)+", "+str(self.bKingSide)+", "+str(self.bQueenSide)+"\n"
        
    
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
        
        # track both of the kings locations 
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        
        # flags for checkmate and stalemate
        self.checkMate = False
        self.staleMate = False
        
        self.inCheck = False
        
        self.enpassantLocation = ()
        
        # castling rights, start the game with all rights
        # logs the castling rights in case a move is undone
        self.castleRightsLog = [CastleRights(True,True,True,True)]
        self.currentCastlingRights = self.castleRightsLog[0]
        
        
        
        
    '''
    Makes a move and flips the turn
    '''        
    def move(self, move: Move) -> None:
        self.board[move.fromRow][move.fromCol] = "--"
        self.board[move.toRow][move.toCol] = move.pieceMoved
        
        self.moveLog.append(move)
        
        
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.toRow, move.toCol)
            
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.toRow, move.toCol)
            
        if move.pawnPromotionMove:
            # auto promote to a queen for now
            pawncolor = move.pieceMoved[0]
            self.board[move.toRow][move.toCol] = pawncolor + "Q"
            print(self.board[move.toRow][move.toCol])
            
        if move.enpassantMove:
            # have to remove the pawn
            move.pieceCaptured = self.board[move.fromRow][move.toCol]
            self.board[move.fromRow][move.toCol] = '--'
             
            
        # updating the viable enpassant square location
        if move.pieceMoved[1] == 'P' and abs(move.fromRow - move.toRow) == 2:
            self.enpassantLocation = ((move.fromRow + move.toRow) // 2, move.toCol)
            
        else:
            self.enpassantLocation = ()
            
        # castle move
        if move.castling:
            # need to move rook 
            # determine which way the player castled
            if move.toCol - move.fromCol == 2:
                # king side
                self.board[move.fromRow][move.fromCol+1] = self.board[move.fromRow][move.fromCol+3]
                self.board[move.fromRow][move.fromCol+3] = '--'
            
            if move.toCol - move.fromCol == -2:
                # queen side
                self.board[move.fromRow][move.fromCol-1] = self.board[move.fromRow][move.fromCol-4]
                self.board[move.fromRow][move.fromCol-4] = '--'
                

        # update the castling rights 
        self.castleRightsLog.append(self.currentCastlingRights.deep_copy())
        self.updateCastlingRights(move)
        
        
        # change turn
        self.whiteToMove = not self.whiteToMove
        
        
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
         
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.fromRow, move.fromCol)
            
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.fromRow, move.fromCol)
            
        if move.enpassantMove:
            # put the captured piece back
            self.board[move.toRow][move.toCol] = '--'
            self.board[move.fromRow][move.toCol] = move.pieceCaptured

            self.enpassantLocation = (move.toRow, move.toCol)
            
        # two move pawn advance    
        if move.pieceMoved[1] == 'P' and abs(move.fromRow - move.toRow) == 2:
            self.enpassantLocation = ()
            
        self.castleRightsLog.pop()    
        self.currentCastlingRights = self.castleRightsLog[len(self.castleRightsLog)-1].deep_copy()
    
        if move.castling:
            if move.toCol - move.fromCol == 2:
                # kingside
                # move the rook back
                self.board[move.fromRow][move.fromCol+3] = self.board[move.fromRow][move.fromCol+1]
                self.board[move.fromRow][move.fromCol+1] = '--'
                
            
            if move.toCol - move.fromCol == -2:
                # queenside
                # move the rook back
                self.board[move.fromRow][move.fromCol-4] = self.board[move.fromRow][move.fromCol-1]
                self.board[move.fromRow][move.fromCol-1] = '--'
                
        self.whiteToMove = not self.whiteToMove

    
    '''
    Updates the castling rights for white or black given a move.
    '''
    def updateCastlingRights(self, move: Move) -> None:
    
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wKingSide = False
            self.currentCastlingRights.wQueenSide = False            
            
        elif move.pieceMoved == 'wR':
            if move.fromRow == 7 and move.fromCol == 7:
                self.currentCastlingRights.wKingSide = False
            else:
                self.currentCastlingRights.wQueenSide = False
    
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bKingSide = False
            self.currentCastlingRights.bQueenSide = False 
            
        elif move.pieceMoved == 'bR':
            if move.fromRow == 0 and move.fromCol == 7:
                self.currentCastlingRights.bKingSide = False
            else:
                self.currentCastlingRights.bQueenSide = False
    
    
    
    '''
    Determines if the current player is in check
    '''
    def isInCheck(self) -> bool:
        if self.whiteToMove:
            return self.squareAttacked(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareAttacked(self.blackKingLocation[0], self.blackKingLocation[1])
            
    '''
    Checks all of the opponents moves to see if the square is attacked
    '''    
    def squareAttacked(self, row, col) -> bool:
        self.whiteToMove = not self.whiteToMove
        
        opponentMoves = self.getAllMoves()
        
        for move in opponentMoves:
            if move.toRow == row and move.toCol == col:
                self.whiteToMove = not self.whiteToMove
                return True
            
        self.whiteToMove = not self.whiteToMove
        return False
    
    
    '''
    Gets all of the valid moves including checks, pins
    '''
    def getValidMoves(self) -> list[Move]:
        tmpEnpassantOriginalLocation = self.enpassantLocation
        tmpCastleRights = self.currentCastlingRights.deep_copy()
        
        moves = []
        
        castleMoves = self.getCastleMoves(0,0)

        moves.extend(castleMoves)
        
        moves.extend(self.getAllMoves())
        for i in range(len(moves) - 1, -1, -1):
            self.move(moves[i])
            self.whiteToMove = not self.whiteToMove
            
            if self.isInCheck():
                moves.remove(moves[i])
                
            self.undoMove()
            self.whiteToMove = not self.whiteToMove
        
        
        
        if len(moves) == 0 and self.isInCheck():
            self.checkMate = True
            
        if len(moves) == 0:
            self.staleMate = True
            
        self.enpassantLocation = tmpEnpassantOriginalLocation
        self.currentCastlingRights = tmpCastleRights
            
        return moves
    
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
        - En-passant move
        - Pawn Promotion, currently defaults to a queen
    '''
    def getPawnMoves(self, row: int, col: int) -> list[Move]:
        moves: list[Move] = []
        
        if self.whiteToMove == True:
            if not self.hasPiece(row-1, col) and self.isInBoard(row-1, col):
                moves.append(Move((row, col), (row-1, col), self.board))
            
            
            if self.pawnOnStartingSquare(row, col) and not self.hasPiece(row-2, col):
                fromSquare = (row, col)
                toSquare = (row-2, col)
                moves.append(Move(fromSquare, toSquare, self.board))
            
            # capture diagonally to the left 
            if self.hasPiece(row-1, col-1) and self.isInBoard(row-1, col-1):
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))
                
            elif (row-1, col-1) == self.enpassantLocation:
                moves.append(Move((row, col), (row-1, col-1), self.board, enpassantMove=True))
                    
                    
            # capture diagonally to the right
            if self.hasPiece(row-1, col+1) and self.isInBoard(row-1, col+1):
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))
            elif (row-1, col+1) == self.enpassantLocation:
                moves.append(Move((row, col), (row-1, col+1), self.board, enpassantMove=True))
                
                
        if self.whiteToMove == False:
            if not self.hasPiece(row+1, col) and self.isInBoard(row+1, col):
                moves.append(Move((row, col), (row+1, col), self.board))
            
            if self.pawnOnStartingSquare(row, col) and not self.hasPiece(row+2, col):
                fromSquare = (row, col)
                toSquare = (row+2, col)
                moves.append(Move(fromSquare, toSquare, self.board))
                
            # capture diagonally to the left 
            if self.hasPiece(row+1, col-1) and self.isInBoard(row+1, col-1):
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            elif (row+1, col-1) == self.enpassantLocation:
                moves.append(Move((row, col), (row+1, col-1), self.board, enpassantMove=True))
                    
            # capture diagonally to the right
            if self.hasPiece(row+1, col+1) and self.isInBoard(row+1, col+1):
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col+1), self.board))
            elif (row+1, col+1) == self.enpassantLocation:
                moves.append(Move((row, col), (row+1, col+1), self.board, enpassantMove=True))
        
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
    Gets the legal castling moves given a row and col position.
    A legal move for castling is:
        - The king cannot castle out of check
        - The king cannot castle through a square that is under attack
        - The king cannot castle once moved
        - The king cannot castle towards the side that a rook has moved.
        - The king cannot castle through other pieces
        - The king cannot castle into check (logic handled in getValidMoves)
    '''    
    def getCastleMoves(self, row, col) -> list[Move]:
        moves = []
        if self.isInCheck():
            return moves
        
        if not self.kingOnStartingSquare():
            return moves
        
        if self.whiteToMove:
            
            if self.currentCastlingRights.wKingSide:
                moves.extend(self.getKingSideCastleMoves())
            
            if self.currentCastlingRights.wQueenSide:
                moves.extend(self.getQueenSideCastleMoves())
            
        
        if not self.whiteToMove:
            if self.currentCastlingRights.bKingSide:
                moves.extend(self.getKingSideCastleMoves())
            
            if self.currentCastlingRights.bQueenSide:
                moves.extend(self.getQueenSideCastleMoves())

        return moves
    
    '''
    Gets the king side castle moves. 
    Checks for pieces in the way
    Checks for squares being targeting 
    '''
    def getKingSideCastleMoves(self) -> list[Move]:
        kingPos = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
        
        moves = []
        
        # check for a piece inbetween the king the king-side rook
        if self.hasPiece(kingPos[0], kingPos[1]+1) or self.hasPiece(kingPos[0], kingPos[1]+2):
            return moves 
        
        # check for if the squares inbetween the king and king-side rook are being targeted
        if self.squareAttacked(kingPos[0], kingPos[1]+1) or self.squareAttacked(kingPos[0], kingPos[1]+2):
            return moves 
            
        
        moves.append(Move((kingPos[0], kingPos[1]), (kingPos[0], kingPos[1]+2), self.board, castling=True)    )
        
        return moves
        
    
    
    '''
    Gets the queen side castle moves. 
    Checks for pieces in the way
    Checks for squares being targeting 
    '''  
    def getQueenSideCastleMoves(self) -> list[Move]:
        kingPos = self.whiteKingLocation if self.whiteToMove else self.blackKingLocation
        
        moves = []
        
        # check for a piece inbetween the king the king-side rook
        if self.hasPiece(kingPos[0], kingPos[1]-1) or self.hasPiece(kingPos[0], kingPos[1]-2) or self.hasPiece(kingPos[0], kingPos[1]-3):
            return moves 
        
        # check for if the squares inbetween the king and king-side rook are being targeted
        if self.squareAttacked(kingPos[0], kingPos[1]-1) or self.squareAttacked(kingPos[0], kingPos[1]-2) or self.hasPiece(kingPos[0], kingPos[1]-3):
            return moves 
            
        
        moves.append(Move((kingPos[0], kingPos[1]), (kingPos[0], kingPos[1]-2), self.board, castling=True))
        
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
    Checks if the king is on his starting square.
    '''
    def kingOnStartingSquare(self) -> bool:
        if self.whiteToMove:
            if self.whiteKingLocation == (7, 4):
                return True
            return False
        
        elif not self.whiteToMove:
            if self.blackKingLocation == (0, 4):
                return True
            return False
        
        return False
        
                 

    '''
    Checks if this square has a piece on it.
    '''
    def hasPiece(self, row: int, col: int) -> bool:
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
    def isInBoard(self, row: int, col: int) -> bool:
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