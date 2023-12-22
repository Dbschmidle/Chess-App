class Piece:
    def __init__(self, name, color, currentSquare):
        self.name = name
        self.color = color
        self.currentSquare = currentSquare
        
    def setCurrentSquare(self, label):
        self.currentSquare = label    
        
 
    def __str__(self):
        return self.name
       
class Pawn(Piece):
    def __init__(self, name, color, currentSquare):
        super().__init__(name, color, currentSquare)
        self.hasMoved = False 
    
    def __str__(self):
        return "P"
           
class Knight(Piece):
    def __init__(self, name, color, currentSquare):
        super().__init__(name, color, currentSquare)        
                   
        
    def __str__(self):
        return "N"
        
class Bishop(Piece):
    def __init__(self, name, color, currentSquare):
        super().__init__(name, color, currentSquare)        
      
    def __str__(self):
        return "B"
        
class Rook(Piece):
    def __init__(self, name, color, currentSquare):
        super().__init__(name, color, currentSquare)               
        
    def __str__(self):
        return "R"
        
class Queen(Piece):
    def __init__(self, name, color, currentSquare):
        super().__init__(name, color, currentSquare)        
        
    def valid_moves(self):
        currentPosition = toIndexes(self.currentSquare)
        potential_moves = []
        
        # horizontal movement
        for i in range(-1, 2, 2):
            for j in range(1,8):
                newPosition = (currentPosition[0], currentPosition[1]+(i*j))
                if(not withinBoard(newPosition[0], newPosition[1])):
                    break
                potential_moves.append(newPosition)
                
        # vertical movement 
        for i in range(-1, 2, 2):
            for j in range(1,8):
                newPosition = (currentPosition[0]+(i*j), currentPosition[1])
                if(not withinBoard(newPosition[0], newPosition[1])):
                    break
                potential_moves.append(newPosition)
            
        # diagonal movement 
        values = ((-1, 1), (1, 1), (1, -1), (-1, -1)) # multipliers for each direction
        for i in values:
            for j in range(1, 8):
                newPosition = (currentPosition[0]+(j*i[0]), currentPosition[1]+(j*i[1]))
                
                # break out of this loop if outside the board and go to next diagnol
                if(newPosition[0] < 0 or newPosition[0] > 7):
                    break
                if(newPosition[1] < 0 or newPosition[1] > 7):
                    break
                
                potential_moves.append(newPosition)                
            
        return potential_moves
        
    def __str__(self):
        return "Q"
    
    
class King(Piece):
    def __init__(self, name, color, currentSquare):
        super().__init__(name, color, currentSquare)        
               
    def __str__(self):
        return "K"