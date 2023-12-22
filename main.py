from game import *
from computer import *

def main():
    newgame = Game(Player("David", "White"), Computer())
    newgame.startGame()
    
    #knight = Knight("Knight", "White", "b1")
    #print(knight.valid_moves())
    

    

if __name__ == "__main__":
    main()    