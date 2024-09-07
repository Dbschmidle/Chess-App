"""
This file is responsible for handling user I/O and displaying the current gamestate to the user on the command line
"""

import pygame as p
import src.Engine as Engine


WIDTH, HEIGHT = 256
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {} # TODO: ADD IMAGES

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    
    gameState = Engine.GameState()
    
    gameRunning = True
    
    squareSelected = ()
    clickLocation = [] # tracks the first and second click location of the user 
    
    while(gameRunning):
        for event in p.event.get():
            if(event.type == p.QUIT):
                gameRunning = False
            elif (event.type == p.MOUSEBUTTONDOWN):
                location = p.mouse.get_pos()
                row = location[1] // SQUARE_SIZE
                col = location[0] // SQUARE_SIZE
                
                if squareSelected == (row, col):
                    # user clicked the same square, clear the clickLocation array
                    squareSelected = ()
                    clickLocation = []
                    continue
                
                squareSelected = (row, col)
                clickLocation.append(squareSelected)
                
                if len(clickLocation == 2):
                    # player has clicked two seperate locations, make a move
                    move = Engine.Move(clickLocation[0], clickLocation[1], gameState.board)
                    
                
                
                
                    
    drawGameState(screen, gameState)
    clock.tick(MAX_FPS)
    p.display.flip()
    
def drawGameState(screen: p.display, gameState: Engine.GameState) -> None:
    drawBoard(screen)
    drawPieces(screen, gameState.board)


def drawBoard(screen: p.display) -> None:
    




if __name__ == "__main__":
    main()
