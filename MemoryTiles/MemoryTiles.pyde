# Memory Tiles game
BOARD_DIMENSION=600
add_library('minim')
import time, random

# class Tile:
#     def __init__(self):

# class Board:
#     def __init__(self):
            
class Game:
    def __init__(self):
        self.start=True # true if it's the beginning of the game
        
    # def update(self):
        
    def display(self):
        if self.start: # display the initial board, ask the player to choose the mode
            fill(255)
            textSize(50)
            text('Memory Tiles',130,200)
            textSize(30)
            text('Choose the mode: ',160,250)
            rect(30, 320, 170, 50,10)
            rect(210, 320, 170, 50,10)
            rect(390, 320, 170, 50,10)
            fill(0)
            text('EASY', 80, 355)
            text('NORMAL', 230, 355)
            text('DIFFICULT', 400, 355)
        else:
            background(0)

# Instantiation
g=Game()

def setup():
    size(BOARD_DIMENSION,BOARD_DIMENSION)
    background(0)
    
def draw():
    g.display()

def mouseClicked():
    if g.start:              # the player chooses the mode
        if 320<mouseY<370:
            if 30<mouseX<200: 
                # mode easy
                g.start=False
            if 210<mouseX<380:
                # mode normal
                g.start=False
            if 390<mouseX<560:
                # mode difficult
                g.start=False
    # else:

                
        
    
            
        
            
        
    
    
    
    
    
