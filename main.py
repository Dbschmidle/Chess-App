from game import *

def main():
    newgame = Game(Player("David", "White"), Computer())
    newgame.startGame()


if __name__ == "__main__":
    main()    