"""
A piece is a baseclass for a type of piece in chess.
    - Pawm, Knight, Bishop, etc.
    - Each piece has a value associated with it. 
    - Each piece has a square that it sits on (unless it has been taken in which case it will be None)

"""
class Piece:
    def __init__(self, name, color, currentSquare):
        self.name = name
        self.color = color
        self.currentSquare = currentSquare
        self.value = 0
        
    def setCurrentSquare(self, label):
        self.currentSquare = label    
        
 
    def __str__(self):
        return self.name
       
       
class Pawn(Piece):
    def __init__(self, name, color, currentSquare):
        super().__init__(name, color, currentSquare)
        self.hasMoved = False 
        self.value = 1
    
    def __str__(self):
        return "P"
           
class Knight(Piece):
    def __init__(self, name, color, currentSquare):
        super().__init__(name, color, currentSquare)        
        self.value = 3
        
    def __str__(self):
        return "N"
        
class Bishop(Piece):
    def __init__(self, name, color, currentSquare):
        super().__init__(name, color, currentSquare)        
        self.value = 3
      
      
    def __str__(self):
        return "B"
        
class Rook(Piece):
    def __init__(self, name, color, currentSquare):
        super().__init__(name, color, currentSquare)               
        self.value = 5
        
        
    def __str__(self):
        return "R"
        
class Queen(Piece):
    def __init__(self, name, color, currentSquare):
        super().__init__(name, color, currentSquare)        
        self.value = 8
        
    def __str__(self):
        return "Q"
    
    
class King(Piece):
    def __init__(self, name, color, currentSquare):
        super().__init__(name, color, currentSquare)        
               
    def __str__(self):
        return "K"