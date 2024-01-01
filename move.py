from util import *
"""
A move is defined as a piece abbreviation ex. 'Q', 'R', (also 'P' for pawn in this game), 
followed by a 'label' ex. 'e4', 'g5' that defines the square that the piece wants to go to.

A move can also involve other symbols, such as 
1) The 'takes' symbol: 'x'
    - ex. 'Qxb5', 'Bxg4'
2) The 'check' symbol: '+'
    - ex. 'Ra8+', 'Qxh7+'
3) The 'checkmate' symbol: '#'
    - ex. 'Qb4#'
4) The 'ambiguity' symbol, where there are two same pieces that can move to the same square
    - ex. 'Rab1', 'Rhb1'
    The second letter defines the file / column of the piece     
    
"""
class Move:        
    """
    Checks if the user entered valid input for a move, converts it to proper form if incorrect
        x: captures
        0-0: kingside castle
        0-0-0: queenside castle
        +: check
        #: checkmate
    Sets the move to the valid user input
    """ 
    def parseUserInput(self, user_input) -> str:
        user_input = user_input.strip() # strip whitespace
        
        if(len(user_input) <= 1 or len(user_input) >= 6):
            return None
        
        # check for the special cases first
        SPECIAL = ("0-0", "0-0-0")
        if(user_input == SPECIAL[0] or user_input == SPECIAL[1]):
            return user_input
        
        # should be the first letter in input ex: "Qa4", "Nxf3", "Bxb5+", "Rab1", "Raxb1", "Raxb1+"
        # convert it to upper
        user_piece_abb = user_input[0].upper()
        ambiguity_specifier = ""
        user_square_label = ""
        takes_symbol = ""
        suffix_symbol = ""
        
        
        if(user_input[1] in LETTERS):
            # ambiguity specifier (or bad notation)
            ambiguity_specifier = user_input[1]
            if(user_input[2] == "x"):
                takes_symbol = user_input[2]
                user_square_label = user_input[3:5]
                if(user_input[-1] == "+" or user_input[-1] == "#"):
                    suffix_symbol = user_input[-1]
                return user_piece_abb+ambiguity_specifier+takes_symbol+user_square_label+suffix_symbol
            
            user_square_label = user_input[2:4]
            if(user_input[-1] == "+" or user_input[-1] == "#"):
                suffix_symbol = user_input[-1]
                
            return user_piece_abb+ambiguity_specifier+takes_symbol+user_square_label+suffix_symbol
            
            
        
        # check if the user is trying to capture
        if(user_input[1] == "x"):
            takes_symbol = "x"
            user_square_label = user_input[2:4].lower()
        else:
            takes_symbol = "x"
            # get the square label and lowercase it
            user_square_label = user_input[1:3].lower()
        
        

        if(user_input[-1] == "+" or user_input[-1] == "#"):
            suffix_symbol = user_input[-1]
        
        # make sure that the piece abbreviation is correct 
        if ( user_piece_abb not in PIECE_ABB ):
            print("Incorrect piece abbreviation")
            return None
            
        return user_piece_abb+takes_symbol+user_square_label+suffix_symbol
        
        
    """
    Gets the label of the move
        - ex. 'Pe4' -> 'e4'
    """
    def getLabel(self):
        if self.hasAmbiguitySymbol():
            if self.hasTakesSymbol():
                return self.move[3:5]
            return self.move[2:4]
        
        if self.hasTakesSymbol():
            return self.move[2:4]
        return self.move[1:3]        
        
    """
    Converts the label of the move into cartestian coordinates in tuple form.
        - ex. 'Pe4' -> (4,4)
    """
    def toIndexes(self) -> (int, int):
        if (len(self.label) != 2):
            print("Board coordiantes out of range...")
            return -1
        self.label = self.label.lower()
        col = -1
        # get the col
        for i, letter in enumerate(LETTERS):
            if self.label[0] == letter:
                col = i
                
        row = 8 - int(self.label[1]) 
        
        return (row, col)
        
    """
    Checks if the move contains an ambiguity symbol.
    """
    def hasAmbiguitySymbol(self) -> bool:
        if(len(self.move) >= 4):
            if(self.move[1] in LETTERS):
                return True
            return False 
        return False 
    
    """
    Gets the ambiguity symbol of a move.
    If the move does not have an ambiguity symbol, then None is returned
    """
    def getAmbiguitySymbol(self) -> str:
        if(self.hasAmbiguitySymbol()):
            return self.move[1]
        return None

    """
    Checks if the move contains a takes symbol.
    """
    def hasTakesSymbol(self) -> bool:
        if self.hasAmbiguitySymbol():
            if self.move[2] == "x":
                return True
            return False
        if self.move[1] == "x":
            return True
        return False
    
    """
    Converts a tuple of indexes (int, int) to a label
    """
    def toLabels(indexes):
        if(len(indexes) == 0):
            return []
        if(type(indexes[0]) == tuple):
            # multiple tuples specified
            labels = []
            for index in indexes:
                row = index[0]
                col = index[1]

                label_letter = LETTERS[col]
                label_num = str(8-row)
                labels.append(label_letter+label_num)

            return labels
                

        row = indexes[0]
        col = indexes[1]

        label_letter = LETTERS[col]
        label_num = str(8-row)
        
        return label_letter+label_num 
    
    """
    Returns true if the move is in the specified listOfMoves
    """
    def isIn(self, listOfMoves):
        for move in listOfMoves:
            if(move.move == self.move):
                return True
        return False
    
      
    """
    Initalize the variables of a move.
        - Move: The chess notation of the move as a string. Ex. 'Nc3'
        - toSquare: The label of the square that the piece wants to go to. Ex. 'Nc3' -> 'c3'
        - fromSquare: The label of the square that the piece is currently on. Ex. 'Nc3' -> 'b1'
    """
    def __init__(self, move: str, toSquare=None, fromSquare=None):
        self.move = self.parseUserInput(move)
        self.toSquare = self.getLabel() if toSquare == None else toSquare
        self.fromSquare = fromSquare
        
        
    def __eq__(self, other):
        if(type(other) == str):
            return True if self.move == other else False
        if type(other) == Move:
            return True if self.move == other.move else False
    
        return False
    
    def __str__(self):
        return self.move
    
    def __repr__(self):
        return self.move