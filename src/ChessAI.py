'''
Handles the logic for the computer chess 'bot'. 

Currently just gets a random move

'''

import random
from Engine import *


CHECKMATE_VALUE = 100
STALEMATE_VALUE = 0


MATERIAL_VALUE = {
    'K' : 0,
    'Q' : 9,
    'R' : 5,
    'B' : 3,
    'N' : 3,
    'P' : 1
}


class ChessBot:
    
    '''
    Get the sum of the piece material value,
    black's material is considered negative.
    
    An 'equal' position would return 0.
    '''
    @staticmethod
    def scoreMaterial(board) -> int:
        score = 0
        for row in board:
            for piece in row:
                if piece[0] == 'w':
                    score += MATERIAL_VALUE[piece[1]]
                    
                elif piece[0] == 'b':
                    score -= MATERIAL_VALUE[piece[1]]
                
        return score
        
        
    '''
    A greedy algorithm for the chess bot that determines its move based on how much value it takes away
    from the opponent.
    
    The problem with this algorithm is that it does not consider more than one move in advance.
    
    Returns the move that calculated the best score
    '''
    @staticmethod
    def greedyChoice(gameState: GameState, valid_moves: list[Move]) -> Move:
        max = -1000
        bestMove = valid_moves[0]
        currentScore = None
        
        for playerMove in valid_moves:
            gameState.move(playerMove)
            
            if gameState.checkMate:
                currentScore = CHECKMATE_VALUE
                
            elif gameState.staleMate:
                currentScore = STALEMATE_VALUE
            else:
                mult = -1 if gameState.whiteToMove else 1
                currentScore = mult * ChessBot.scoreMaterial(gameState.board)
                
            if currentScore > max:
                max = currentScore
                bestMove = playerMove
            
            gameState.undoMove()
            
        return bestMove
            
    
    
    @staticmethod
    def getRandomMove(validMoves: list[Move]) -> Move:
        return random.choice(validMoves)