PIECE_NAMES = ("Pawn", "Knight", "Bishop", "Rook", "Queen", "King")
PIECE_ABB = ("P", "N", "B", "R", "Q", "K")
LETTERS = ("a", "b", "c", "d", "e", "f", "g", "h")
COLORS = ("White", "Black")


def is_even(num : int) -> bool:
    if(num % 2 == 0):
        return True
    return False

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




def main():
    return

if __name__ == "__main__":
    main()
    
    
