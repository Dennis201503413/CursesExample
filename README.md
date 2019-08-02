Is a library that supplies a **terminal-independent screen-painting and keyboard-handling facility for text based terminals**, this library can work with minor quirks in different terminals, the curses library gives a way to display fancy things in otherwise a mostly text and null interface, which is really valuables in cases where GUI is not an option.

### Creating a curses application

We will build a simple curses application that moves a little dot around the screen using the keypad to change its direction in any given moment.

#### Import libraries

Before we even begin, we need to import the curses library to our proyect.

``` python
import curses #import the curses library
```

Since our application will be working with special keys such as KEY_UP or KEY_DOWN, we will need to import these keys from our curses library.

``` python
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN #import special KEYS from the curses library
```

First we need to initialize our console, this can be done thru the following command, please note that we are saving this initialization in the stdscr variable, naming this variable stdscr is a convention and it corresponds to the C variable of the same name.

#### Initialize curses application

``` python
stdscr = curses.initscr() #initialize console
```

Now we need to create a new window, this can be achieved calling newwin which returns a pointer to a new window with the given number of lines an columns and the given x and y position.

``` python
height = 20
width = 60
pos_y = 0
pos_x = 0
window = curses.newwin(height,width,pos_y,pos_x) #create a new curses window
```
*Note that the coordinate system used in curses is unusual, Coordinates are always passed in the order* **(y,x)** *and the top-left corner of a window  is coordinate* **(0,0)** *.*

To make use of special keys during curses application we will need to enable keypad mode, curses will make sure to process the special sequences accordingly.

``` python
window.keypad(True)     #enable Keypad mode
```

Usually curses application turn off the echo keys that are usually printed in a normal terminal application, this can be done thru the following command

``` python
curses.noecho()         #prevent input from displaying in the screen
```

We will also make sure to hide the cursor while our application is running, this can be done thru the command curs_set(int) the int value represents what kind of visibility we want, **0**, **1** and **2** for **invisible**, **normal** or **very visible** respectively.

``` python
curses.curs_set(0)      #cursor invisible (0)
```

In order to identify our working area in a better manner, we will need to paint a border around it, this can be achieved in two ways, by calling the border() function or the box() function, in this tutorial we will be using the **border([ls[, rs[, ts[, bs[, tl[, tr[, bl[, br]]]]]]]])** function but more information van be found about both in the [Python documentation](https://docs.python.org/2/library/curses.html).

``` python
window.border(0)        #default border for our window
```

Note that a 0 value in any parameter of the border function will cause the default character to be used for that parameter. Keyword parameters cannot be used. The defaults are listed int the following table.

| Parameter | Description         | Default value |
|-----------|---------------------|---------------|
| ls        | Left side           | ACS_VLINE     |
| rs        | Right side          | ACS_VLINE     |
| ts        | Top                 | ACS_HLINE     |
| bs        | Bottom              | ACS_HLINE     |
| tl        | Upper-left corner   | ACS_ULCORNER  |
| tr        | Upper-right corner  | ACS_URCORNER  |
| bl        | Bottom-left corner  | ACS_LLCORNER  |
| br        | Bottom-right corner | ACS_LRCORNER  |

We will also configure our getch() function as non-blocking, thru the nodelay() function, this returns curses.ERR (a value of -1), to indicate that the input isn’t ready.

``` python
window.nodelay(True)    #return -1 when no key is pressed
```

To recap we will need to invoke this configuration before starting to work with our curses application.

``` python
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
```

#### Core application

Now we can begin working in the core of our curses application.
First we need to define a starting point and a starting direction for our dot, we will manage this thru 3 variables, pos_x, pos_y and key. Once we have decided this, we will print our first dot on our window.

``` python
key = KEY_RIGHT         #key defaulted to KEY_RIGHT
pos_x = 5               #initial x position
pos_y = 5               #initial y position
window.addch(pos_y,pos_x,'*')   #print initial dot
```

Now we will define a key in our keyboard to be able to end the application once we are finished, I will be using **[ESC] key**, which in **ASCII is 27**, but you are welcome to use your favorite key, our application will keep running until such key is pressed, this can be achieved thru a while loop.

``` python
while key != 27:                #run program while [ESC] key is not pressed
```

We will need to alter the behavior of our windows thru the timeout() function, which can accept three kinds of parameters:
* **negative**, blocking read is used (will wait indefinitely for input)
* **zero**, non-blocking read is used and curses.getch() will return a -1 if no input is waiting.
* **positive**, curses.getch() will be blocked for a delay in milliseconds sent to the function as a parameter, and return a value of -1 if there is no input at that time.

int this case we will use a delay of 100 milliseconds to make our dot moderately fast.

``` python
window.timeout(100)         #delay of 100 milliseconds
```

Since our dot will move freely on the screen and only turn directions in the case that a key is pressed, we need to check whether a key is being pressed at a certain time, otherwise continue the same direction as before.


``` python
keystroke = window.getch()  #get current key being pressed
if keystroke is not  -1:    #key is pressed
    key = keystroke         #key direction changes
```

Finally, we will check the current direction of the dot, and base on that we will not only eliminate the last dot painted on the screen, but paint the next one, creating the illusion that the dot is moving in our window.

``` python
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
```

#### End application

To return the terminal to its previous state we need to call

``` python
curses.endwin() #return terminal to previous state
```

Note that this project includes different bugs (for example dot cannot crash into walls), as this is an example and a blank canvas that can be modified to suit different kinds of needs, you could make a Tetris, Snake or Pong game, playing with the position of the dot(s) and the delay of the game, the possibilities are just as endless as your imagination.

Check this project on [GitHub](https://github.com/Dennis201503413/CursesDotExample).
