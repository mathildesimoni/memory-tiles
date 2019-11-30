# Memory Tiles game
BOARD_DIMENSION=600
TILES_COLOR=[0,128,200]
add_library('minim')
import time, random

class Tile: 
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color
        
class Board:
    def __init__(self):
        self.num_row=3
        self.board=[] # the list which represents the board
        for row in range(self.num_row):
            rowlist=[]
            for col in range(self.num_row):
                rowlist.append(Tile((BOARD_DIMENSION/self.num_row)*col,(BOARD_DIMENSION/self.num_row)*row,TILES_COLOR))
            self.board.append(rowlist)
        
            
    # def update(self):
        
    def display(self): # display the board
        for row in self.board:
            for el in row:
                fill(el.color[0],el.color[1],el.color[2])
                strokeWeight(2)
                rect(el.x, el.y, BOARD_DIMENSION/self.num_row,BOARD_DIMENSION/self.num_row)
                
class Game:
    def __init__(self):
        self.start=True # true if it's the beginning of the game
        self.board=Board()
        self.level=1
        self.life=3
        
    # def update(self):
        # self.board.update()
        
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
            background(150)
            self.board.display()
            noFill()
            rect(30,BOARD_DIMENSION+15, 300, 50) 
            fill(0)
            textSize(30)
            text("Level: "+str(self.level), 50, BOARD_DIMENSION+50)
            text("Lives: "+str(self.life), 200, BOARD_DIMENSION+50)
                
# Instantiation

g=Game()

def setup():
    size(BOARD_DIMENSION,BOARD_DIMENSION+80)
    background(0)
    
def draw():
    g.display()

def mouseClicked():
    if g.start:
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
        # g.update()

                
        
    
            
        
            
        
    
    
    
    
    
