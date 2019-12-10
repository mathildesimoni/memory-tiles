# Memory Tiles game

BOARD_DIMENSION=600
TILES_COLOR=[0,128,200]
add_library('minim')
player = Minim(this)
import time, random
path = os.getcwd() + "/"

class Tile: 
    def __init__(self,x,y,size,color):
        self.x=x
        self.y=y
        self.size=size
        self._color=color
        
class Board:
    def __init__(self):
        self.num_row=3 # the initial board is 3x3
        self.cross=loadImage(path+'images/'+'cross.png')
        self.board=[] # the list which represents the board
        for row in range(self.num_row):
            rowlist=[]
            for col in range(self.num_row):
                rowlist.append(Tile(10+(((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row))*col+5*col,
                               75+(((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row))*row+5*row,
                               ((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row),
                               TILES_COLOR))
            self.board.append(rowlist)
        
    def update(self, choice, row, col): # update the board 
        if choice=='correct':
            self.board[int(row)][int(col)]._color=[255,255,255]
        elif choice=='incorrect':
            self.board[int(row)][int(col)]._color='image'
        elif choice=='same_board':
            self.board=[]
            for row in range(self.num_row):
                rowlist=[]
                for col in range(self.num_row):
                    rowlist.append(Tile(10+(((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row))*col+5*col,
                                75+(((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row))*row+5*row,
                                ((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row),
                                TILES_COLOR))
                self.board.append(rowlist)
        elif choice=='new_board':
            self.num_row+=1
            self.board=[]
            for row in range(self.num_row):
                rowlist=[]
                for col in range(self.num_row):
                    rowlist.append(Tile(10+(((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row))*col+5*col,
                                75+(((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row))*row+5*row,
                                ((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row),
                                TILES_COLOR))
                self.board.append(rowlist)
            
    def display(self): # display the board
        for row in self.board:
            for el in row:
                if el._color=='image':
                    fill(TILES_COLOR[0], TILES_COLOR[1], TILES_COLOR[2])
                    noStroke()
                    rect(el.x, el.y,el.size,el.size,5)
                    image(self.cross, el.x, el.y, el.size, el.size)
                else:
                    fill(el._color[0],el._color[1],el._color[2])
                    noStroke()
                    rect(el.x, el.y,el.size,el.size,5)
                
class Game:
    def __init__(self):
        self.start=True # true if it's the beginning of the game
        self.board=Board()
        self.level=1
        self.life=3
        self.img1=loadImage(path+'images/'+'brain.png')
        self.img2=loadImage(path+'images/'+'bulb.png')
        self.random_tiles=[]
        self.time_constraint=None # depends om the mode
        self.player_turn=False
        self.computer_turn=False
        self.number_tiles_displayed=None # number of white tiles the program displays randomly
        self.tile_clicked_row=None       # keep in memory the row of the last tile the player clicked
        self.tile_clicked_col=None       # keep in memory the column of the last tile the player clicked
        self.wrong_tile_sound=player.loadFile(path +'SoundEffects/wrong_tile.mp3')
        self.correct_tile_sound=player.loadFile(path + 'SoundEffects/correct_tile.mp3')
        self.refresh_sound=player.loadFile(path + "SoundEffects/refresh.mp3")
        self.times_up_sound=player.loadFile(path + "SoundEffects/times_up.mp3")
        self.count_correct=0
        self.count_incorrect=0
        self.end_game=False
        self.refresh=False
        
    def check_tile(self):
        for tile in self.random_tiles:  
            if self.board.board[tile[0]][tile[1]].y<mouseY<self.board.board[tile[0]][tile[1]].y+self.board.board[tile[0]][tile[1]].size:
                if self.board.board[tile[0]][tile[1]].x<mouseX<self.board.board[tile[0]][tile[1]].x+self.board.board[tile[0]][tile[1]].size:
                    if self.board.board[tile[0]][tile[1]]._color==TILES_COLOR:
                        self.tile_clicked_row=tile[0]
                        self.tile_clicked_col=tile[1]
                        return True
        for row in self.board.board:
            for el in row:
                if el.y<mouseY<el.y+el.size and el.x<mouseX<el.x+el.size and el._color==TILES_COLOR:
                    self.tile_clicked_row=self.board.board.index(row)
                    self.tile_clicked_col=self.board.board[self.board.board.index(row)].index(el)     
                    return False    
        return 'no_tile'
    
    def check_conditions(self):
        # check time constraint (TO DO)
        # check if the player has completed the level of not
        # check check that the player didn't click on more than 3 wrong squares
        # check the number of lives
        # => call update board
        if self.life==1 and self.count_incorrect==3:
            self.end_game=True
            # self.computer_turn=True
        else:
            if self.count_correct==self.number_tiles_displayed:
                self.refresh_sound.rewind()
                self.refresh_sound.play()
                if self.level%2==1:
                    self.board.update('same_board',0,0)
                else:
                    self.board.update('new_board',0,0)
                self.count_incorrect=0
                self.count_correct=0
                self.level+=1
                self.computer_turn=True
                
            if self.count_incorrect==3:
                self.life-=1
                self.board.update('same_board',0,0)
                self.count_incorrect=0
                self.count_correct=0
                self.computer_turn=True
        
    def update(self):
        if self.check_tile()!='no_tile':
            if self.check_tile():
                self.board.update('correct', self.tile_clicked_row, self.tile_clicked_col)
                self.count_correct+=1
                self.correct_tile_sound.rewind()
                self.correct_tile_sound.play()
            
            elif not self.check_tile():
                self.board.update('incorrect', self.tile_clicked_row, self.tile_clicked_col)
                self.count_incorrect+=1
                self.wrong_tile_sound.rewind()
                self.wrong_tile_sound.play()
            
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
    
    def endBoard(self):
        fill(0)
        rect(125,150,400,150)
        fill(250)
        textSize(30)
        text("Level: "+str(self.level-1), 50, 50)
        textSize(50)
        text('GAME OVER', 200, 200)
        text('click to restart', 150, 250)
       
    def display(self):
        if self.start: # display the initial board, ask the player to choose the mode
            self.initialization()
        elif self.end_game:
            self.endBoard()
            self.player_turn=False
        else:
            self.board.display()
            fill(250)
            textSize(30)
            text("Level: "+str(self.level), 50, 50)
            text("Lives: "+str(self.life), 200, 50)
            
    def choose_tiles(self):
        self.random_tiles=[]
        if self.level%2!=0:
            self.number_tiles_displayed=((self.board.num_row)**2)//3
        else:
            self.number_tiles_displayed=((self.board.num_row**2)//3)+1
        for i in range(0, self.number_tiles_displayed):
                Mylist=[]
                check=False
                while not check:
                    row=random.randint(0,self.board.num_row-1)
                    col=random.randint(0,self.board.num_row-1)
                    check2=True
                    for ele in self.random_tiles:
                        if row==ele[0] and col==ele[1]:
                            check2=False
                    if check2==True:
                        check=True
                Mylist.append(row)
                Mylist.append(col)     
                self.random_tiles.append(Mylist)
            
    def display_tiles(self):
        self.choose_tiles()
        for tile in self.random_tiles:
            self.board.board[tile[0]][tile[1]]._color=[250,250,250]
        self.display()
        for tile in self.random_tiles:
            self.board.board[tile[0]][tile[1]]._color=TILES_COLOR
            
                                        
# Instantiation

g=Game()
pause=False
refresh=False

def setup():
    size(BOARD_DIMENSION,BOARD_DIMENSION+65)
    background(0)
    frameRate(200)

def draw():
    global pause
    if pause:
        delay(1250)
        g.computer_turn=False
        g.player_turn=True
        pause=False
    if g.refresh:
        delay(1000)
        g.refresh=False
        background(40)
        g.display_tiles()
        pause=True
    else:
        if not g.end_game:
            background(40)
        g.display()
        g.check_conditions()
        if g.computer_turn:
            g.refresh=True
        
        

def mouseClicked():
    if g.start:
        # g.computer_turn=True
        # beginning=True
        if 320<mouseY<370:
            if 30<mouseX<200: 
                # mode easy
                g.time_constraint=5 # the player has 5 sec for the first level and it increases by 1 for each level
                g.start=False
                g.computer_turn=True
            if 210<mouseX<380:
                # mode normal
                g.time_constraint=3 # the player has 3 sec for the first level and it increases by 1 for each level
                g.start=False
                g.computer_turn=True
            if 390<mouseX<560:
                # mode difficult
                g.time_constraint=1 # the player has 1 sec for the first level and it increases by 1 for each level
                g.start=False
                g.computer_turn=True
    elif g.player_turn:
        g.update()
    elif g.end_game:
        g.__init__()
                        
# TO DO
# game over screen (personalize)
# time constraint + color depends on time
# 
    
# def draw():
#     if g.refresh:
#         delay(2000)
#         g.refresh=False
#     else:
#         global pause
#         if pause:
#             delay(1250)
#             g.computer_turn=False
#             g.player_turn=True
#             pause=False
#         background(40)
#         g.check_conditions()
#         g.display()
#         if g.computer_turn:
#             g.display_tiles()
#             pause=True    
