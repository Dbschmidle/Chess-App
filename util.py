from constants import *
from board import Board
from piece import *

class FileManager:
    
    unknown_filename_counter = 0
    
    """
    Loads a file from this directory and returns the board.
    The first line of the file should be whose turn it is.
    File should be in format <color><name of piece><square name> newline
    Ex.
        - 'W'
        - 'WQb4'
        - 'BPh1'
        -  ...
    """
    def loadFile(filename):
        with open(filename, "r") as file:
            if filename == None:
                print(f"File '{filename}' not found...")
                return
            
            lines = file.readlines()
            
            board = Board.createEmptyBoard()
            
            ### assume white has turn for now
            lines.pop(0)
            ###
                
            for line in lines:
                line = line.upper().strip()
                if line[1] in PIECE_ABB:
                    # create the piece
                    piece_abb_index = PIECE_ABB.index(line[1])
                    piece_color = COLORS[0] if line[0] == 'W' else COLORS[1]
                    new_piece = PIECE_TYPES[piece_abb_index](PIECE_NAMES[piece_abb_index], piece_color, line[2:4].lower())
                    
                    # put piece on board
                    piece_board_indexes = Util.toIndexes(line[2:4])
                    if(not Util.withinBoard(piece_board_indexes[0], piece_board_indexes[1])):
                        print(f"{line[2:4]} is an invalid square")
                        return
                    
                    board[piece_board_indexes[0]][piece_board_indexes[1]].addPiece(new_piece)
                    
            return board
                    
    
    """
    Saves a gamestate into a file into this directory.
    The first line of the file will be whose turn it is.
    """
    def saveGame(game, filename="game"):
        with open(filename+".txt", "w") as newfile:
            newfile.write("W\n") if game.turn == COLORS[0] else newfile.write("B\n")
                
            for row in game.board.getBoard():
                for square in row:
                    if square.hasPiece():
                        pieceColor = square.piece.color
                        pieceName = str(square.piece)
                        newfile.write(pieceColor[0]+pieceName+square.label+"\n")
                            
            
class Util:

    # Converts board coordinates ex: "E4", "A8" to indexes on the board 
    # Returns a tuple of the indexes
    def toIndexes(label: str) -> (int, int):
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

    # Checks whether a given row and column index is wihtin the board space
    def withinBoard(row: int, col: int) -> bool:
        if(row >= 0 and row <= 7):
            if(col >= 0 and col <= 7):
                return True
        return False
        

    def getOpponentColor(myColor):
        oppColor = COLORS[1] if myColor == COLORS[0] else COLORS[0]
        return oppColor


    def debugPrintMoves(listOfMoves):
        for move in listOfMoves:
            print(move.debugPrint())



def main():
    board = FileManager.loadFile("test.txt")

if __name__ == "__main__":
    main()
    
    
