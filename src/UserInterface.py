"""
This file is responsible for handling user I/O and displaying the current gamestate to the user on the command line
"""

import pygame as p
import Engine
import ChessAI


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
    
    valid_moves = gameState.getValidMoves()
    moveMadeFlag = False
    
    # flags to determine if the player is white or black
    playerOne = True
    playerTwo = False
    
    while(gameRunning):
        
        playerTurn = (gameState.whiteToMove and playerOne) or (not gameState.whiteToMove and playerTwo)
        
        for event in p.event.get():
            if(event.type == p.QUIT):
                gameRunning = False
            elif (event.type == p.KEYDOWN):
                if event.key == p.K_z:
                    gameState.undoMove()
                    valid_moves = gameState.getValidMoves()
                    continue
                
            elif (event.type == p.MOUSEBUTTONDOWN):
                
                if playerTurn: # only allow mouseclicks when its the players turn
                    
                    location = p.mouse.get_pos()
                    row = location[1] // SQUARE_SIZE
                    col = location[0] // SQUARE_SIZE
                    
                    
                    if userDoubleClickedSquare(squareSelected, row, col):
                        # user clicked the same square, clear the clickLocation array
                        squareSelected = []
                        clickLocation = []
                        highlighted_square = []
                    
                    else:
                        
                        squareSelected = [row, col]
                        clickLocation.append(squareSelected)
                        
                    if len(clickLocation) == 1:
                        highlighted_square = [row, col]
                        turnStr = "white" if gameState.whiteToMove else "black"
                        print(f"Valid Moves for {turnStr}: [", end=" ")
                        for move in valid_moves:
                            print(move, end=", ")
                        print("]\n")
                        
                    if len(clickLocation) == 2:
                        # player has clicked two seperate locations, make a move

                        newmove = Engine.Move(clickLocation[0], clickLocation[1], gameState.board)
                            
                        # check if the move is valid
                        for i in range(len(valid_moves)):
                            if valid_moves[i] == newmove:
                                # user selected move is valid
                                moveMadeFlag = True
                                    
                                gameState.move(valid_moves[i])

                                print(valid_moves[i].convertToChessNotation())
                                    
                                clickLocation = [] 
                                highlighted_square = []
                                squareSelected = []
                                break
                                
                            if i == len(valid_moves) - 1:
                                # user tried to make an invalid move
                                highlighted_square = [row, col] if gameState.hasPiece(row, col) else [] # only highlight pieces
                                squareSelected = [row, col]
                                clickLocation = []
                                clickLocation.append(squareSelected)
                                print(f"{newmove} is not a valid move.")
                                
                    
        if not playerTurn:
            # chessbot logic
            chessBotMove = ChessAI.ChessBot.greedyChoice(gameState, valid_moves)
            gameState.move(chessBotMove)
            moveMadeFlag = True
                
                
        if moveMadeFlag == True:
            valid_moves = gameState.getValidMoves()
            moveMadeFlag = False
                    
                    
            
        drawGameState(screen, gameState, highlighted_square)
        clock.tick(MAX_FPS)
        p.display.flip()
                    
    
'''
Draws the background squares, pieces, and highlights the square if applicable.
'''
def drawGameState(screen, gameState: Engine.GameState, highlighted_square) -> None:
    drawBackgroundBoard(screen, highlighted_square)
    drawPieces(screen, gameState.board)

'''
Draws the background squares of the board.
'''
def drawBackgroundBoard(screen, highlighted_square) -> None:
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            p.draw.rect(screen, BACKGROUND_COLOR[((row+col)%2)], p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
    if len(highlighted_square) == 2:
        p.draw.rect(screen, HIGHLIGHT_COLOR, p.Rect(highlighted_square[1]*SQUARE_SIZE, highlighted_square[0]*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

'''
Draws the pieces on the board.
'''
def drawPieces(screen, board) -> None:
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece == '--':
                continue
            piece_fullname = INV_PIECE_ABB[piece]
            screen.blit(IMAGES[piece_fullname], p.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

'''
Checks if the user double clicked the same square.
'''
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
    
    
def drawGameOver(screen):
    font = p.font.Font("Cambria", 32)
    text = font.render("Hello!", True, p.Color("black"))
    textRect = text.get_rect()
    
    textRect.center = (WIDTH//2, HEIGHT//2)



if __name__ == "__main__":
    main()
