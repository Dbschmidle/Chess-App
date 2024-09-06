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
        
"""
Stores the information of a move
"""
class Move():
    CONV_RANK_TO_ROWS = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    CONV_FILES_TO_COLS = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    CONV_ROWS_TO_RANK = {7: "1", 6:"2", 5:"3", 4:"4", 3:"5", 2:"6", 1:"7", 0:"8"}
    CONV_COLS_TO_FILES = {7: "h", 6:"g", 5:"f", 4:"e", 3:"d", 2:"c", 1:"b", 0:"a"}
    
    
    def __init__(self, fromSquare, toSquare, gameState):
        self.pieceMoved = gameState[self.fromRow][self.fromCol]
        self.pieceCaptured = gameState[self.toRow][self.toCol]
        
        self.fromRow = fromSquare[0]
        self.fromCol = fromSquare[1]
        self.toRow = toSquare[0]
        self.toCol = toSquare[1]
    
    def convertToChessNotation(self) -> str:
        fromRank = Move.CONV_ROWS_TO_RANK[self.fromRow]
        toRank = Move.CONV_ROWS_TO_RANK[self.toRow]
        fromFile = Move.CONV_COLS_TO_FILES[self.fromCol]
        toFile = Move.CONV_COLS_TO_FILES[self.toCol]
        return str(fromRank)+str(fromFile)+"->"+str(toRank)+str(toFile)
    
    def convertToRowCol(self) -> [int, int]:
        return
        
        
    def __str__(self):
        return self.convertToChessNotation()
        
    
    
        