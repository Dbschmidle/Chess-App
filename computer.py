import random

class Computer:
    
    def __init__(self, difficulty=1, color="Black"):
        """
        1) Easy - random moves by computers
        (others) define later
        """
        self.difficulty = difficulty
        self.color = color 
    
    
    """
    Find a random move for the computer to play
    Returns a tuple of the coordinates that the computer wants to go
    """
    def computerMove(game):
        # Get all the possible moves 
        allMoves = game.getAllMoves(game.turn)
        print("All moves for computer: ", end="")
        print(allMoves)
        
        randomMove = random.choice(allMoves) # random choice of piece
        return randomMove