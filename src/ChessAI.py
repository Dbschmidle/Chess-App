'''
Handles the logic for the computer chess 'bot'. 

'''

import random
from Engine import *


CHECKMATE_VALUE = 100
STALEMATE_VALUE = 0
MAX_DEPTH = 2


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
    def findMoveMiniMax(gameState: GameState, valid_moves: list[Move]):
        global nextMove
        nextMove = valid_moves[0]
        ChessBot.miniMax(gameState, valid_moves, MAX_DEPTH, gameState.whiteToMove)
        return nextMove


    '''
    Recursive implementation for the minimize-maximize chess algorithm 
    '''
    @staticmethod
    def miniMax(gameState: GameState, valid_moves: list[Move], depth: int, whiteToMove: bool) -> int:
        global nextMove
        if depth == 0:
            return ChessBot.scoreMaterial(gameState.board)
    
        if whiteToMove:
            maxScore = -CHECKMATE_VALUE
            
            for move in valid_moves:
                # make the move
                gameState.move(move)
                
                new_valid_moves = gameState.getValidMoves()
                
                score = ChessBot.miniMax(gameState, new_valid_moves, depth-1, not whiteToMove)
            
                if score > maxScore:
                    maxScore = score
                    if depth == MAX_DEPTH:
                        nextMove = move
    
                gameState.undoMove()
                
            return maxScore

        else: 
            minScore = CHECKMATE_VALUE
            
            for move in valid_moves:
                # make the move
                gameState.move(move)
                
                new_valid_moves = gameState.getValidMoves()
                
                score = ChessBot.miniMax(gameState, new_valid_moves, depth-1, not whiteToMove)
            
                if score < minScore:
                    minScore = score
                    if depth == MAX_DEPTH:
                        nextMove = move
    
                gameState.undoMove()
                
            return minScore
    
    
    @staticmethod
    def getNegaMaxAlphaBeta(gameState: GameState, valid_moves: list[Move], depth: int, turnMult: int, alpha: int, beta: int):
        global nextMove
        if depth == 0:
            return turnMult * ChessBot.scoreMaterial(gameState.board)

        maxScore = -CHECKMATE_VALUE
            
        for move in valid_moves:
            gameState.move(move)
            
            nextMoves = gameState.getValidMoves()
            
            # make a recursive call but flip and negate alpha and beta parameters
            score = -ChessBot.getNegaMaxAlphaBeta(gameState, nextMoves, depth - 1, -turnMult, -beta, -alpha)

            if score > maxScore:
                maxScore = score
                if depth == MAX_DEPTH:
                    nextMove = move
            
            gameState.undoMove()        
            if maxScore > alpha:
                alpha = maxScore
                
            if alpha >= beta:
                break
            
            
        
        return maxScore
            
    @staticmethod
    def getNegaMaxMove(gameState: GameState, valid_moves: list[Move]):
        global nextMove
        nextMove = valid_moves[0]
        
        ChessBot.getNegaMaxAlphaBeta(gameState, valid_moves, MAX_DEPTH, 1 if gameState.whiteToMove else -1, -CHECKMATE_VALUE, CHECKMATE_VALUE)
        
        return nextMove
        
    
    @staticmethod
    def getRandomMove(validMoves: list[Move]) -> Move:
        return random.choice(validMoves)