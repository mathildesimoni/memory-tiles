# Memory Tiles game
# Board dimension has to be > 600 in order to play correctly
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
                if self.count_correct != self.number_tiles_displayed:
                    self.correct_tile_sound.rewind()
                    self.correct_tile_sound.play()
            
            elif not self.check_tile():
                self.board.update('incorrect', self.tile_clicked_row, self.tile_clicked_col)
                self.count_incorrect+=1
                self.wrong_tile_sound.rewind()
                self.wrong_tile_sound.play()
            
    def initialization(self):
        background(0)
        image(self.img1,BOARD_DIMENSION/3,BOARD_DIMENSION/2.2)
        image(self.img2,5,15,BOARD_DIMENSION/5,BOARD_DIMENSION/5)
        fill(255)
        textSize(BOARD_DIMENSION/12)
        text('Memory Tiles',BOARD_DIMENSION/4.5,BOARD_DIMENSION/3)
        textSize(30)
        text('Choose the mode: ',BOARD_DIMENSION/3.75,BOARD_DIMENSION/2.4)
        rect(BOARD_DIMENSION/20, BOARD_DIMENSION/1.9, 170, 50,10)
        rect(BOARD_DIMENSION/2.85, BOARD_DIMENSION/1.9, 170, 50,10)
        rect(BOARD_DIMENSION/1.55, BOARD_DIMENSION/1.9, 170, 50,10)
        fill(0)
        text('EASY', BOARD_DIMENSION/20+43, BOARD_DIMENSION/1.9+38)
        text('NORMAL', BOARD_DIMENSION/2.9+22, BOARD_DIMENSION/1.9+38)
        text('DIFFICULT',BOARD_DIMENSION/1.55+6, BOARD_DIMENSION/1.9+38)
    
    def endBoard(self):
        fill(40)
        noStroke()
        rect(0,0,BOARD_DIMENSION, 75)
        fill(0)
        stroke(255)
        strokeWeight(3)
        rect(BOARD_DIMENSION/6,BOARD_DIMENSION/4,BOARD_DIMENSION/1.5,BOARD_DIMENSION/3)
        fill(250)
        textSize(BOARD_DIMENSION/12)
        text('GAME OVER',BOARD_DIMENSION/4.15,BOARD_DIMENSION/2.75)
        textSize(BOARD_DIMENSION/20)
        text("Level: "+str(self.level-1),BOARD_DIMENSION/2.5, BOARD_DIMENSION/2.30)
        textSize(BOARD_DIMENSION/18)
        text('click to restart', BOARD_DIMENSION/3.3, BOARD_DIMENSION/2)
        
       
    def display(self):
        if self.start: # display the initial board, ask the player to choose the mode
            self.initialization()
        elif self.end_game:
            self.endBoard()
            self.computer_turn=True
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
checking=False
refresh=False

def setup():
    size(BOARD_DIMENSION,BOARD_DIMENSION+65)
    background(0)
    myFont = createFont("Georgia", 16)
    textFont(myFont)


def draw():
    global pause, refresh, checking
    if checking:
        g.computer_turn=False
        checking=False
    elif pause:
        delay(1250)
        pause=False
        checking=True
    elif refresh:
        delay(1000)
        refresh=False
        background(40)
        g.display_tiles()
        pause=True
    else:
        if not g.end_game:
            background(40)
        g.display()
        g.check_conditions()
        if g.computer_turn and not g.end_game:
            refresh=True
        
def mouseClicked():
    if g.start:
        if BOARD_DIMENSION/1.9<mouseY<BOARD_DIMENSION/1.9+50:
            if BOARD_DIMENSION/20<mouseX<BOARD_DIMENSION/20+170: 
                # mode easy
                g.time_constraint=5 # the player has 5 sec for the first level and it increases by 1 for each level
                g.start=False
                g.computer_turn=True
            if BOARD_DIMENSION/2.85<mouseX<BOARD_DIMENSION/2.85+170:
                # mode normal
                g.time_constraint=3 # the player has 3 sec for the first level and it increases by 1 for each level
                g.start=False
                g.computer_turn=True
            if BOARD_DIMENSION/1.55<mouseX<BOARD_DIMENSION/1.55+170:
                # mode difficult
                g.time_constraint=1 # the player has 1 sec for the first level and it increases by 1 for each level
                g.start=False
                g.computer_turn=True
    elif not g.computer_turn:
        g.update()
    elif g.end_game:
        g.__init__()
                        
# TO DO

# time constraint + color depends on time
