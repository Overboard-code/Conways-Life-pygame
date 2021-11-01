import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame_widgets as pw
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
import sys
import time
import random
import numpy as np 
import webcolors  # because Pygame_widgets slider does not use colors  just RGB tuples

#
#  A Pygame version of Conway's Game of Life (Again) 
#  https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules
#  I added different colors for new,adult,lonely and overcrowded cells
#  I used pygame_widgets for the buttons and sliders, You can use them or just write your own GUI widgets (Again)
#  Andy Richter  New changes to pygame_widgets Oct, 2021,  Original code Jan, 2020
#  Free to use change or whatever
#

rules = '''
    1. Any live cell with fewer than two live neighbours dies, as if caused by under-population.
    2. Any live cell with two or three live neighbours lives on to the next generation.
    3. Any live cell with more than three live neighbours dies, as if by overcrowding.
    4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.'''

#Initializations:

#CONSTANTS
#Set up colors for ease of use  Change them to suit
bkgnd_color = 'grey88' # also used for 'empty' cells
lonely = 'deepskyblue'
crowded = 'brown4'
adult ='forestgreen'
new_baby = 'chartreuse2'
top_color = 'darkgreen' 
text_color = 'snow'
shadows = 'grey23'
hover_color = 'grey46'
click_color = 'grey66'
cell_colors = [bkgnd_color,new_baby,adult,lonely,crowded]
# Window sizes
thesize = 85   # This decides how large the window will be 
thehigh = thesize - 6
cellSize = 10
buttonSize = 100  # Play with this until they look right
buttonSlots = 8   # allows even spacing of buttons without fancy math
windowsize = thesize*cellSize
bottomRow = windowsize-60  # Spaces buttons off of the bottom  Assumes butons are 40 tall
#-------------------
# global variables  Changes here change the game 
global FPS
FPS = 0
initFPS = 10  # for the slider
global generation
generation = 0
global Single
Single = False  # Single step  Run one Flip/flop then stop if True
global flop
flop = False  # flip/flop for showing the board with all live and with some dead cells
global run
run = False  
global possibilities
possibilities = [0, 0, 0, 2]  # Decides how full the random board will be  Add more zeros for a sparser board
global minF
minF = 1  # for the slider 
global maxF
maxF = 88  # for the slider 
#-------------------

#Define a 2D board List containing 0
global board
board = np.zeros((thesize,thesize),dtype=int)
global tempboard
tempboard = np.zeros((thesize,thesize),dtype=int)

#Set up pygame
pygame.init()
global surface
surface = pygame.display.set_mode((windowsize, windowsize)) # Define the surface for the simulation to run on
pygame.display.set_caption('Conway\'s Game of Life')
surface.fill(bkgnd_color) # Fill the screen bkgnd_color
pygame.display.update()
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None,30)

# Commands for buttons and keys
def runFlop():  # Key RETURN
    global run
    global Single
    run = not run
    Single = False
def setSingle(): # key SPACE
    global run
    global Single
    global flop
    run = True
    Single = True
    flop = True
def newRandom():  # Key 'r'
    global generation
    global board
    global thesize
    global thehigh
    generation = 0
    pygame.display.set_caption('Conway\'s Game of Life')
    for r in range(thesize):
        for c in range(thehigh):
            board[r,c] = random.choice(possibilities)
def boardClear(): # Key 'c'
    global generation
    global board
    global thesize
    global thehigh
    generation = 0
    pygame.display.set_caption('Conway\'s Game of Life')
    board.fill(0)
def game_quit():  # key ESCAPE
    pygame.quit()
    sys.exit()

#Function to round to the nearest base
def myround(x, base=5):
    return int(base * round(float(x)/base))

#Function for returning the segment that a number is in
def whichSlot(x, groupsize=cellSize):
    return x // groupsize

#function Is live
def isLive(cell):
    return (cell != 0)

#Function for returning which row and column the mouse is in
def where():
    x, y = pygame.mouse.get_pos()
    return (whichSlot(x), whichSlot(y))

#Function to run Conway's Rules agains a cell board[r,c]
def runConwayRules(r,c):
    adj = status = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            rangeX = range(0, board.shape[0])  # X bounds
            rangeY = range(0, board.shape[1])  # Y bounds          
            (newX, newY) = (r+dx, c+dy)  # adjacent cell            
            if (newX in rangeX) and (newY in rangeY) and (dx, dy) != (0, 0):
                if isLive(board[newX, newY]):
                    adj += 1  
    if board[r,c] == 1 or board[r,c] == 2: # any currently live cell
        if adj < 2:   # with less than two 'live' neighbors
           status = 3 # dies alone 
        if adj > 3: # With more than three 'live' neighbors
            status = 4 # dies crowded
        if adj == 2 or adj == 3: # with 2 or 3 'live' neighbors
            status = 2 # lives on to the next generation 
    if board[r,c] == 0: # any empty spot
         if adj == 3: #  with exactly three 'live' neighbors
            status = 1 # becomes a new live cell
    return status

# make a cell on the grid 
def drawCell(ro, col, colour):
    myXY = (ro*cellSize, col*cellSize)
    circle_radius = int(cellSize/2)
    border_width = 0 # 0 gives a filled circle
    pygame.draw.circle(surface, colour, myXY, circle_radius, border_width)
 
def makeAButton(x,label,routine):  # Add a pygame_widget button along the bottom 
    return Button(surface,x,bottomRow,buttonSize,40,
    text=label,onClick=routine,
    font=gui_font,textColour=text_color,font_size=16,
    margin=20,  # Minimum distance between text/image and edge of button
    inactiveColour=top_color,  # Colour of button when not being interacted with
    hoverColour=hover_color,  # Colour of button when being hovered over
    pressedColour=click_color,  # Colour of button when being clicked
    shadowDistance=5,shadowColor=shadows,
    radius=12 ) # Radius of border corners (leave empty for not curved)
  
#Main loop
run = False
tictoc = True
Single = False
flop = True
# Define a bunch of pygame widgets  I wrote this at version 1
#  https://libraries.io/pypi/pygame-widgets

rndm_button = makeAButton(int(windowsize/buttonSlots*0+3),'Random',newRandom)
play_button = makeAButton(int(windowsize/buttonSlots*1),' >/| | ',runFlop)
step_button = makeAButton(int(windowsize/buttonSlots*2),'Once',setSingle)
quit_button = makeAButton(int(windowsize/buttonSlots*3),"Quit",game_quit)
clear_button = makeAButton(int(windowsize/buttonSlots*4) ,"Clear",boardClear)
FPS_slider = Slider(surface,int(windowsize/buttonSlots*5+20),bottomRow+15, 200,15, 
    min=2,max=88,handleColour=webcolors.name_to_rgb(top_color),initial=initFPS,handleRadius=7)
 
while 1:
    #Draw the board as cells
    for r in range(thesize):
        for c in range(thehigh):
                drawCell(r, c, cell_colors[board[r,c]]) # cell value chooses color 
    #Process Events    
    events =  pygame.event.get()      
    pw.update(events) # Check for button events for pygame_widgets
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            break;
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                game_quit()
                break;
            elif event.key == pygame.K_SPACE:
                setSingle()
            elif event.key == pygame.K_RETURN:
                runFlop()
            elif event.key == pygame.K_c:
                boardClear()
            elif event.key == pygame.K_r:
                newRandom()

    #run the Conway rules 
    if run:
        if tictoc: # Tic
            tictoc = not tictoc # Flip flop displaying and processing cells 
            tempboard.fill(0)
            for r in range(len(board)):
                for c in range(thehigh):
                    tempboard[r,c] = runConwayRules(r, c)
            if np.array_equal(board, tempboard):  # Stop if nothing changed
                run = False 
            else: 
                board[:] = tempboard
                generation += 1
            pygame.display.set_caption('Conway\'s Game of Life Generation=' + str(generation) + " Speed=" + str(FPS))
            if Single:
                flop = not flop                  
        else: # Toc
            tictoc = not tictoc # Flip flop displaying and processing cells 
            for r in range(len(board)):
                for c in range(thehigh):
                    if board[r,c] > 2: # dead or dying cell
                       board[r,c] = 0 # clear it
            if Single:
                if not flop:                
                    run = False
    # Add new cells if clicked and delete if Right Cliked
    presses = pygame.mouse.get_pressed()
    if presses[0]:
        putx, puty = where()   
        if puty < thehigh:   
            board[putx,puty] = 1
            if not run:
                generation = 0
                pygame.display.set_caption('Conway\'s Game of Life')
    if presses[2]:
        putx, puty = where()
        board[putx,puty] = 0
        if not run:
            generation = 0
            pygame.display.set_caption('Conway\'s Game of Life')
    # Get Speed from Slider
    FPS = FPS_slider.getValue()
    if run:
        clock.tick(FPS)
    if Single and not flop:  # Let user see the 'dead' cells for a flicker
        pygame.time.wait(50)
    pygame.display.flip()
    
