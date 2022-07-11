# Conways-Life-pygame
Another version of Game of Life but using pygame_widgets

I wrote this a while back  (2020) but added pygame_widgets to add buttons and a slider to mimic the keyboard functions.  

You'll need to install: </br>
pygame </br>
pygame-widgets </br>
numpy </br>
and webcolors </br>

I used numpy arrays because this whole game is just a couple of arrays and numpy arrays are way faster/cheaper than pythons built in arrays.  
The game is different from many versions I have seen.  It uses colors to show the state of the cells.  Cells have 4 states: 

Empty or dead(0)  Default state </br>
New baby(1)       Just born because 3 and only 3 'live' cells were adjacent to a dead cell </br>
adult(2)          surived at least on round of the game, a grown up baby has 2 or 3 'live' adjacent cells </br>
dying of lonliness(3)  is and adult or baby with less than 2 adjeacent 'live' cells </br>
dying of crowding(4)  has more than 3 adjacent live cells </br>

I didn't use parameters to define colors and sizes  Just constants in the code.  Add parms if you like. 
By the way pygame_widgets didn't document the vertical=True/False parameter for sliders. 

I set up a tic/toc to show the change in state of the cells  

Keyboard Funtions to momic the buttons are: </br>
RETURN:   Play/Pause </br>
SPACE:    Single step the game  </br>
'c':      clear and stop the game  </br>
'r':      stop and fill with a random bunch of cells  </br>
'ESC':    quit the game  </br>
