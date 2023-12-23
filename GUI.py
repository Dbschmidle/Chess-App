import sys
from constants import *
from colorama import Fore, Back, Style, just_fix_windows_console

"""
The GUI class handles all the user interaction and displaying of the game.
Currently the 'GUI' is only through interaction with the command line, for now...

Functionality:
    - Displaying the board
    - Displaying the menu
    - Checking for user exit
    - Changing settings
    
"""
class GUI:
    DEFAULT = (Back.LIGHTWHITE_EX, Back.LIGHTGREEN_EX, Fore.WHITE, Fore.BLACK)
    RED_BLUE = (Back.WHITE, Back.BLACK, Fore.RED, Fore.BLUE)
    THEMES_LIST = (DEFAULT, RED_BLUE)
    
    
    def __init__(self):
        self.theme = GUI.DEFAULT 
        self.size = 2 #size of the squares, currently not used
        self.firstLoad = True
        self.showLabels = True
    
    def displayBoard(self, board, turn):
        white_sqaure_color = self.theme[0]
        black_square_color = self.theme[1]
        white_piece_color = self.theme[2]
        black_piece_color = self.theme[3]
        
        print("-"*24)
        # reverse the printing of the board if the player is playing as black
        board = reversed(board) if turn == COLORS[1] else board
        for i, row in enumerate(board):
            print(Fore.WHITE + str(8-i), end=" ") if self.showLabels == True else ""
            for square in row:
                
                piece_abb = " "+str(square)+" "
                piece_abb = Style.NORMAL + piece_abb
                
                # determine the background color
                piece_abb = white_sqaure_color + piece_abb if square.color == COLORS[0] else black_square_color+ piece_abb
                # determine the piece color (if the square has a piece)
                if(square.hasPiece()):
                    piece_abb = white_piece_color + piece_abb if square.piece.color == COLORS[0] else black_piece_color + piece_abb
                
                print(piece_abb, end="")
                
            # reset the style
            print(Style.RESET_ALL, end="")
            print()
        
        # print the labels
        if(self.showLabels):
            print(" "*2, end="") # some padding
            for letter in UPP_LETTERS:
                print(Fore.WHITE + " "+letter+" ", end="")
            print()    
        print("-"*24)
    
    def firstTimeLoad(self):
        s = Fore.RED+"-"*24
        print(f"\n\n{s}Chess Game{s}\n")
        return
          
    def displayMenu(self):
        if self.firstLoad:
            self.firstTimeLoad()
            self.firstLoad = False
            just_fix_windows_console()
            
        while(1): 
            print(Fore.GREEN+"-"*24+"MENU"+"-"*24)
            options = ("\t1) Start Game", "\t2) Change Theme", "\t3) Change Labels","\t4) Quit")
            for option in options:
                print(Fore.BLUE + option)
                    
            user_input = input("\t>")
            if self.checkExit(user_input):
                sys.exit()
            
            try:
                user_input = int(user_input)
            except:
                print(Fore.RED+"Invalid selection...")
                continue
            
            # check for in bounds
            if(user_input-1 >= len(options) or user_input-1 < 0):
                print(Fore.RED+"Invalid selection...")
                continue


            if user_input == 1:
                break
            
            elif user_input == 2:
                self.setTheme()
                
            elif user_input == 3:
                self.setLabels()
        
            elif user_input == 4:
                print(Fore.GREEN+"Goodbye...")
                print(Style.RESET_ALL)
                sys.exit()
               
    def setTheme(self):
        while(1):
            print(Fore.GREEN+"THEME CHANGE")
            options = ("\t1) White/Green (Default)", "\t2) Red/Blue")
            for option in options:
                print(Fore.BLUE + option)

            selection = int(input("\t>"))
            try:
                self.theme = self.THEMES_LIST[selection-1]
                return
            except:
                print(Fore.RED+"Invalid selection...")
                continue
           
    def setLabels(self):
        while 1:
            print(Fore.GREEN+"LABEL CHANGE")
            options = ("\t1) On", "\t2) Off")
            if self.showLabels:
                print(Fore.BLUE + options[0] + " [X]")
                print(Fore.BLUE + options[1] + " [ ]")
            else: 
                print(Fore.BLUE + options[0] + " [ ]")
                print(Fore.BLUE + options[1] + " [X]")
                
            selection = input("\t>")
            if(selection.lower() == "on"):
                self.showLabels = True
                return
            if(selection.lower() == "off"):
                self.showLabels = False
                return
            
            selection = int(selection)
            if(selection == 1):
                self.showLabels = True
                return
            if(selection == 2):
                self.showLabels = False
                return
            print(Fore.RED+"Invalid input...")
                  
    """
    Checks if the user has entered input that indicates they want to exit the game.
    Returns True or False
    """        
    def checkExit(self, user_input) -> bool:
        if type(user_input) != str:
            return False
            
        user_input = user_input.lower()
        for exit in ("q", "quit", "exit", "stop"):
            if(user_input == exit):
                return True
        return False