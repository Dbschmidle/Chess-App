'''
Handles the logic for the computer chess 'bot'. 

Currently just gets a random move

'''

import random
from Engine import Move



class ChessBot:
    
    @staticmethod
    def getRandomMove(validMoves: list[Move]) -> Move:
        return random.choice(validMoves)