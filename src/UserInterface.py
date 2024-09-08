"""
This file is responsible for handling user I/O and displaying the current gamestate to the user on the command line
"""

import pygame as p
import Engine


WIDTH, HEIGHT = 512,512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
BACKGROUND_COLOR = [p.Color("white"), p.Color("chartreuse4")]
HIGHLIGHT_COLOR = p.Color("gold")

PIECE_ABB = {'white_pawn': 'wP', 
             'black_pawn': 'bP', 
             'white_bishop': 'wB', 
             'black_bishop': 'bB', 
             'white_knight': 'wN', 
             'black_knight': 'bN', 
             'white_rook': 'wR', 
             'black_rook': 'bR',
             'white_queen': 'wQ', 
             'black_queen': 'bQ', 
             'white_king': 'wK', 
             'black_king': 'bK'}

INV_PIECE_ABB = {v: k for k, v in PIECE_ABB.items()}

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    
    gameState = Engine.GameState()
    
    gameRunning = True
    
    loadImages()
    
    squareSelected = []
    clickLocation = [] # tracks the first and second click location of the user 
    
    highlighted_square = []
    
    while(gameRunning):
        for event in p.event.get():
            if(event.type == p.QUIT):
                gameRunning = False
            elif (event.type == p.KEYDOWN):
                if event.key == p.K_z:
                    gameState.undoMove()
                    continue
                
            elif (event.type == p.MOUSEBUTTONDOWN):
                location = p.mouse.get_pos()
                row = location[1] // SQUARE_SIZE
                col = location[0] // SQUARE_SIZE
                
                print(f"Click Registered at: ({row}, {col})")
                
                if userDoubleClickedSquare(squareSelected, row, col):
                    # user clicked the same square, clear the clickLocation array
                    squareSelected = []
                    clickLocation = []
                    highlighted_square = []
                    continue
                
                squareSelected = [row, col]
                clickLocation.append(squareSelected)
                
                if len(clickLocation) == 1:
                    highlighted_square = [row, col]
                
                if len(clickLocation) == 2:
                    # player has clicked two seperate locations, make a move
                    newmove = Engine.Move(clickLocation[0], clickLocation[1], gameState.board)
                    gameState.move(newmove)
                    print(newmove.convertToChessNotation())
                    clickLocation = [] # reset the click locations
                    highlighted_square = []
                    squareSelected = []
            
        drawGameState(screen, gameState, highlighted_square)
        clock.tick(MAX_FPS)
        p.display.flip()
                    
    
    
    
def drawGameState(screen, gameState: Engine.GameState, highlighted_square) -> None:
    drawBackgroundBoard(screen, highlighted_square)
    drawPieces(screen, gameState.board)


def drawBackgroundBoard(screen, highlighted_square) -> None:
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            p.draw.rect(screen, BACKGROUND_COLOR[((row+col)%2)], p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
    if len(highlighted_square) == 2:
        p.draw.rect(screen, HIGHLIGHT_COLOR, p.Rect(highlighted_square[1]*SQUARE_SIZE, highlighted_square[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen, board) -> None:
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece == '--':
                continue
            piece_fullname = INV_PIECE_ABB[piece]
            screen.blit(IMAGES[piece_fullname], p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def userDoubleClickedSquare(squareSelected: list[int], row: int, col: int):
    return squareSelected == [row, col]


'''
Initalize the Global 'IMAGES' hashmap with the images from 'chess/images/'
'''
def loadImages() -> None:
    PIECE_FULLNAMES = ('white_pawn', 'black_pawn', 'white_bishop', 'black_bishop', 'white_knight', 'black_knight', 'white_rook', 'black_rook', 'white_queen','black_queen', 'white_king', 'black_king')
    
    for name in PIECE_FULLNAMES:
        local_path = "images/"+name+".png"
        IMAGES[name] = p.transform.scale(p.image.load(local_path), (SQUARE_SIZE, SQUARE_SIZE))
    

if __name__ == "__main__":
    main()
