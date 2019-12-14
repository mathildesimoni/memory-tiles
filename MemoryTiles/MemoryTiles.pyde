# Memory Tiles game
# Board dimension has to be > 600 in order to play correctly
BOARD_DIMENSION=600
TILES_COLOR=[0,128,200]
WHITE=[255,255,255]
RED_1=[255,204,204]
RED_2=[255,102,102]
RED_3=[255,0,0]
BLACK=[0,0,0]
add_library('minim')
player = Minim(this)
import time, random
path = os.getcwd() + "/"

class Tile:  # defines each tile of the board
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
        for row in range(self.num_row): # creation of the initial board
            rowlist=[]
            for col in range(self.num_row):
                rowlist.append(Tile(10+(((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row))*col+5*col,  
                               75+(((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row))*row+5*row,
                               ((BOARD_DIMENSION-20)/self.num_row)-((5*(self.num_row-1))/self.num_row),
                               TILES_COLOR))
            self.board.append(rowlist)
        
    def update(self, choice, row, col,color): # update the board
        if choice=='correct': # if the player picks a correct tile, the color depends on the time elapsed
            if color=='WHITE':
                self.board[int(row)][int(col)]._color=WHITE
            elif color=='RED_1':
                self.board[int(row)][int(col)]._color=RED_1
            elif color=='RED_2':
                self.board[int(row)][int(col)]._color=RED_2
            elif color=='RED_3':
                self.board[int(row)][int(col)]._color=RED_3
            elif color=='BLACK':
                self.board[int(row)][int(col)]._color=BLACK
        elif choice=='incorrect': # if the player picks an incorrect tile
            self.board[int(row)][int(col)]._color='image' # a cross appears
        elif choice=='same_board' or choice=='new_board': # at the end of each level
            if choice=='new_board':
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
        self.random_tiles=[] # list of the tiles randomly chosen to display for each level
        self.time_constraint=0 # depends on the mode
        self.time=0
        self.computer_turn=False
        self.number_tiles_displayed=None # number of white tiles the program displays randomly
        self.tile_clicked_row=None       # keeps in memory the row of the last tile the player clicked
        self.tile_clicked_col=None       # keeps in memory the column of the last tile the player clicked
        self.count_correct=0 # Number of correct tiles the player has picked 
        self.count_incorrect=0 # Number of incorrect tiles the player has picked
        self.end_game=False # if it is the end of the game
        self.end_music=True 
        self.rules_display=False # if the player wants to display the rules
        self.img1=loadImage(path+'images/'+'brain.png')
        self.img2=loadImage(path+'images/'+'bulb.png')
        self.wrong_tile_sound=player.loadFile(path +'SoundEffects/wrong_tile.mp3')
        self.correct_tile_sound=player.loadFile(path + 'SoundEffects/correct_tile.mp3')
        self.refresh_sound=player.loadFile(path + "SoundEffects/refresh.mp3")
        self.times_up_sound=player.loadFile(path + "SoundEffects/times_up.mp3")
        
    def choose_tiles(self): # chooses randomly the tiles to display
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
            
    def display_tiles(self): # displays the tiles randomly chosen
        self.choose_tiles()
        for tile in self.random_tiles:
            self.board.board[tile[0]][tile[1]]._color=[250,250,250]
        self.display()
        for tile in self.random_tiles:
            self.board.board[tile[0]][tile[1]]._color=TILES_COLOR
    
    def check_tile(self): # after the player picks a tile, this function checks if it is a correct tile or not
        for tile in self.random_tiles:  
            if self.board.board[tile[0]][tile[1]].y<mouseY<self.board.board[tile[0]][tile[1]].y+self.board.board[tile[0]][tile[1]].size:
                if self.board.board[tile[0]][tile[1]].x<mouseX<self.board.board[tile[0]][tile[1]].x+self.board.board[tile[0]][tile[1]].size:
                    if self.board.board[tile[0]][tile[1]]._color==TILES_COLOR:
                        self.tile_clicked_row=tile[0]
                        self.tile_clicked_col=tile[1]
                        return True # correct tile
        for row in self.board.board:
            for el in row:
                if el.y<mouseY<el.y+el.size and el.x<mouseX<el.x+el.size and el._color==TILES_COLOR:
                    self.tile_clicked_row=self.board.board.index(row)
                    self.tile_clicked_col=self.board.board[self.board.board.index(row)].index(el)     
                    return False  # incorrect tile
        return 'no_tile' # the player didn't click on a tile
    
    def check_conditions(self):
        fill(250)
        textSize(30)
        text("Time: "+str(((self.time_constraint-millis()+self.time)/1000)+1), 350, 50) # displays the time the player has to complete the level (update every second)
        if self.life==1 and self.count_incorrect==3: # if the player has used his 3 lives
            if self.end_music:
                self.times_up_sound.rewind()
                self.times_up_sound.play()
                self.end_music=False
            self.end_game=True
            
        else:
            if self.count_correct==self.number_tiles_displayed: # if the player has picked all the correct tiles
                if millis()<=self.time+g.time_constraint: # if the player was fast enough
                    self.refresh_sound.rewind()
                    self.refresh_sound.play()
                    if self.level%2==1:
                        self.board.update('same_board',0,0,0)
                    else:
                        self.board.update('new_board',0,0,0)
                    self.level+=1 # next level
                    self.time_constraint+=1000
                else: # if the player wasn't fast enough
                    self.times_up_sound.rewind()
                    self.times_up_sound.play()
                    self.board.update('same_board',0,0,0) # same level
                self.count_incorrect=0
                self.count_correct=0
                self.computer_turn=True

            if self.count_incorrect==3: #if the player has picked 3 incorrect tiles
                self.life-=1 # he looses a life
                self.board.update('same_board',0,0,0) # he stays on the same level
                self.count_incorrect=0
                self.count_correct=0
                self.times_up_sound.rewind()
                self.times_up_sound.play()
                self.computer_turn=True
            
    def update(self): # update the board every time the player picks a tile
        if self.check_tile()!='no_tile':
            if self.check_tile(): # if it is a correct tile
                if millis()<=self.time+(g.time_constraint/4):
                    self.board.update('correct', self.tile_clicked_row, self.tile_clicked_col,'WHITE')
                elif self.time+(g.time_constraint/4)<millis()<=self.time+((2*g.time_constraint)/4):
                    self.board.update('correct', self.tile_clicked_row, self.tile_clicked_col,'RED_1')
                elif self.time+((2*g.time_constraint)/4)<millis()<=self.time+((3*g.time_constraint)/4):
                    self.board.update('correct', self.tile_clicked_row, self.tile_clicked_col,'RED_2')
                elif self.time+((3*g.time_constraint)/4)<millis()<=self.time+g.time_constraint:
                    self.board.update('correct', self.tile_clicked_row, self.tile_clicked_col,'RED_3')
                else:
                     self.board.update('correct', self.tile_clicked_row, self.tile_clicked_col,'BLACK')   
                self.count_correct+=1
                if self.count_correct != self.number_tiles_displayed:
                    self.correct_tile_sound.rewind()
                    self.correct_tile_sound.play()
            
            elif not self.check_tile(): # if it is an incorrect tile
                self.board.update('incorrect', self.tile_clicked_row, self.tile_clicked_col,0)
                self.count_incorrect+=1
                if self.count_incorrect!=3:
                    self.wrong_tile_sound.rewind()
                    self.wrong_tile_sound.play()
            
    def initialization(self): # displays the initial board
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
        rect(20, BOARD_DIMENSION, 115, 50, 10)
        fill(0)
        text('EASY', BOARD_DIMENSION/20+43, BOARD_DIMENSION/1.9+38)
        text('NORMAL', BOARD_DIMENSION/2.9+22, BOARD_DIMENSION/1.9+38)
        text('DIFFICULT',BOARD_DIMENSION/1.55+6, BOARD_DIMENSION/1.9+38)
        text('RULES', 26, BOARD_DIMENSION+38)
        
    def endBoard(self): # displays the final board
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
        
    def rules(self): # displays the rules
        background(40)
        fill(255)
        rect(20, BOARD_DIMENSION, 115, 50, 10)
        fill(0)
        textSize(30)
        text('OK', 50, BOARD_DIMENSION+38)
        fill(255)
        textSize(BOARD_DIMENSION/12)
        text('Game rules', BOARD_DIMENSION/4,BOARD_DIMENSION/5)
        textSize(20)
        text('- Memory Tiles is a visual memory game for one player',30, BOARD_DIMENSION/3)
        text('- The mode you choose controls the time constraint of the game ', 30, BOARD_DIMENSION/3+30)
        text('- You have a starting number of 3 lives', 30, BOARD_DIMENSION/3+60)
        text('- For each level, white tiles will appear to be memorized', 30, BOARD_DIMENSION/3+90)
        text('- After the white tiles disappear you can pick the tiles by ', 30, BOARD_DIMENSION/3+120)
        text('  clicking with the mouse ', 30, BOARD_DIMENSION/3+150)
        text('  * If you pick the good tiles before the time is up, you', 30, BOARD_DIMENSION/3+180)
        text('    go to the next level ', 30, BOARD_DIMENSION/3+210)
        text('  * If you pick the good tiles but the time is up, you', 30, BOARD_DIMENSION/3+240)
        text('    stay on the same level ', 30, BOARD_DIMENSION/3+270)
        text('  * If you pick the wrong tiles, you loose a life and stay', 30, BOARD_DIMENSION/3+300)
        text('    on the same level', 30, BOARD_DIMENSION/3+330)
        text('- The game ends when tou have used your 3 lives', 30, BOARD_DIMENSION/3+360)
        text('GOOD LUCK! ', 200, BOARD_DIMENSION/3+390)
    
    def display(self):
        if self.start: 
            if self.rules_display:
                self.rules() # displays the rules
            else:
                self.initialization() # display the initial board, ask the player to choose the mode
        elif self.end_game:
            self.endBoard() # displays the final board
            self.computer_turn=True
        else: 
            self.board.display() # displays the board during the game
            fill(250)
            textSize(30)
            text("Level: "+str(self.level), 50, 50) # displays the level
            text("Lives: "+str(self.life), 200, 50) # displays the number of lives
     
                                                                                   
# Instantiation #

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
        g.time=millis()
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
        if not g.start and not g.end_game and not g.computer_turn:
            g.check_conditions()
        if g.computer_turn and not g.end_game:
            refresh=True
        
def mouseClicked():
    if g.start: # the game has not started yet
        if 26<mouseX<141 and BOARD_DIMENSION<mouseY<BOARD_DIMENSION+50: 
            if not g.rules_display: # if the player wants to read the Game rules
                g.rules_display=True
            else: # when the player has read the rules
                g.rules_display=False
        elif BOARD_DIMENSION/1.9<mouseY<BOARD_DIMENSION/1.9+50: # the player chooses a mode
            if BOARD_DIMENSION/20<mouseX<BOARD_DIMENSION/20+170: 
                # mode easy
                g.time_constraint=6000 # the player has 6 sec for the first level and it increases by 1sec for each level
                g.start=False
                g.computer_turn=True
            if BOARD_DIMENSION/2.85<mouseX<BOARD_DIMENSION/2.85+170:
                # mode normal
                g.time_constraint=4000 # the player has 4 sec for the first level and it increases by 1sec for each level
                g.start=False
                g.computer_turn=True
            if BOARD_DIMENSION/1.55<mouseX<BOARD_DIMENSION/1.55+170:
                # mode difficult
                g.time_constraint=2000 # the player has 2 sec for the first level and it increases by 1sec for each level
                g.start=False
                g.computer_turn=True
    elif g.end_game: # if it 's the end of the game
        g.__init__()
    elif not g.computer_turn:
        g.update()
        
# End of the code #
