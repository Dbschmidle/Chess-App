
         
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
        self.whiteToMove = False if self.whiteToMove else True
        
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
        
        
        
        