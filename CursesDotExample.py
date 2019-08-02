'''
----------------------------------
#Developed by                     |
@user: Dennis Masaya              |
#id: 201503413                    |
#e-mail: dennismasaya@gmail.com   |
----------------------------------
This example demonstrates how to build a simple curses
application that moves a little dot around the screen
using the keypad to change its direction in any given
moment.
'''

import curses #import the curses library
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN #import special KEYS from the curses library

stdscr = curses.initscr() #initialize console
height = 20
width = 60
pos_y = 0
pos_x = 0
window = curses.newwin(height,width,pos_y,pos_x) #create a new curses window
window.keypad(True)     #enable Keypad mode
curses.noecho()         #prevent input from displaying in the screen
curses.curs_set(0)      #cursor invisible (0)
window.border(0)        #default border for our window
window.nodelay(True)    #return -1 when no key is pressed

key = KEY_RIGHT         #key defaulted to KEY_RIGHT
pos_x = 5               #initial x position
pos_y = 5               #initial y position
window.addch(pos_y,pos_x,'*')   #print initial dot
while key != 27:                #run program while [ESC] key is not pressed
    window.timeout(100)         #delay of 100 milliseconds
    keystroke = window.getch()  #get current key being pressed
    if keystroke is not  -1:    #key is pressed
        key = keystroke         #key direction changes

    window.addch(pos_y,pos_x,' ')       #erase last dot
    if key == KEY_RIGHT:                #right direction
        pos_x = pos_x + 1               #pos_x increase
    elif key == KEY_LEFT:               #left direction
        pos_x = pos_x - 1               #pos_x decrease
    elif key == KEY_UP:                 #up direction
        pos_y = pos_y - 1               #pos_y decrease
    elif key == KEY_DOWN:               #down direction
        pos_y = pos_y + 1               #pos_y increase
    window.addch(pos_y,pos_x,'*')       #draw new dot


curses.endwin() #return terminal to previous state
