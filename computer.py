import random
from util import *

class Computer:
    
    def __init__(self, difficulty=1, color=COLORS[1]):
        """
        1) Easy - random moves by computers
        (others) define later
        """
        self.difficulty = difficulty
        self.color = color 
        