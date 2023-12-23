from game import *
from computer import *

def main():
    newgame = Game(Player("David", "White"), Computer())
    newgame.startGame()


if __name__ == "__main__":
    main()    