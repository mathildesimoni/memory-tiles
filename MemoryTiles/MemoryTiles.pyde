# Memory Tiles game
BOARD_DIMENSION=600
TILES_COLOR=[0,128,200]
# add_library('minim')
import time, random
path = os.getcwd() + "/"

class Tile: 
    def __init__(self,x,y,size,color):
        self.x=x
        self.y=y
        self.size=size
        self.color=color
        
class Board:
    def __init__(self):
        self.num_row=3
        self.board=[] # the list which represents the board
        for row in range(self.num_row):
            rowlist=[]
            for col in range(self.num_row):
                rowlist.append(Tile(10+(((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row))*col+5*col,
                               75+(((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row))*row+5*row,
                               ((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row),
                               TILES_COLOR))
            self.board.append(rowlist)
            
    # def update(self):
        
    def display(self): # display the board
        for row in self.board:
            for el in row:
                fill(el.color[0],el.color[1],el.color[2])
                noStroke()
                rect(el.x, el.y,el.size,el.size)
                
class Game:
    def __init__(self):
        self.start=True # true if it's the beginning of the game
        self.board=Board()
        self.level=1
        self.life=3
        self.img1=loadImage(path+'brain.png')
        self.img2=loadImage(path+'bulb.png')
        
    # def update(self):
        # self.board.update()
    
    def initialization(self):
        background(0)
        image(self.img1,200,275)
        image(self.img2,5,15,125,125)
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
        
    def display(self):
        if self.start: # display the initial board, ask the player to choose the mode
            self.initialization()
        else:
            self.board.display()
            fill(250)
            textSize(30)
            text("Level: "+str(self.level), 50, 50)
            text("Lives: "+str(self.life), 200, 50)
                
# Instantiation

g=Game()

def setup():
    size(BOARD_DIMENSION,BOARD_DIMENSION+65)
    background(0)
    
def draw():
    background(40)
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

                
        
    
            
        
            
        
    
    
    
    
    
