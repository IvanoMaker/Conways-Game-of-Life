'''
Conway's Game of Life Automaton Simulation
Evan Mead - @IvanoMaker

This is a replica of Conway's Game of Life written in Python
The game is comprised of a 2d vector of Cell objects who each have 
a boolean state for dead/alive. Each cell is responsible for 
keeping track of its neighbors and updating its own condition.
The program uses PyGame as a visual display of the animation.

The program can read in a design and basic configuration for 
the program stored in a file called 'start.txt' in the same
directory as the python file. The file is structured like this
(height, width, cell size)
00 - - 00
|  \    |
|    \  |
00 - - 00
Each 0 represents a dead starting cell, and a 1 is a live starting
cell.
Included is a directory of some interesting designs I have found.
'''

import pygame                        # import pygame module for visual display

class Cell:                          # Cell class definition
    def __init__(self, x, y, state):    # constructor
        self.pos = [x, y]               # position vector
        self.status = state             # status variable
        self.neighbors = 0              # number of live neighbors

    def get_status(self):            # get_status
        return self.status           # @return the boolean status of the cell
    
    def set_status(self, state):     # set_status @param boolean state
        self.status = state          # set the cells status to the parameter state
    
    def draw(self, cell_size, screen): # draw function to draw a rectangle to the screen based on the state of the cell
        if self.status == True:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.pos[0]*cell_size, self.pos[1]*cell_size, cell_size, cell_size))
        else:
            pygame.draw.rect(screen, (1, 1, 1), pygame.Rect(self.pos[0]*cell_size, self.pos[1]*cell_size, cell_size, cell_size))
        
    def set_neighbors(self, field):  # set neighbors method @param 2d vector of cells
        count = 0                       # counter
        for i in range(-1, 2, 1):       # check all cells within a single unit of the current
            for j in range(-1, 2, 1):   
                if (i != 0 or j != 0):   # ensure were not comparing the current cell to itself
                    nX = self.pos[0] + i # variables for the current neighbors position in the matrix
                    nY = self.pos[1] + j
                    if (nX >= 0 and nX < len(field) and nY >= 0 and nY < len(field[0])): # if the cell is within the fields boundaries
                        if (field[nX][nY].get_status()):                                 # and is alive
                            count += 1                                                   # increase count
        self.neighbors = count           # when this process is done, set the number of neighbors to the count

    def update(self):                                           # Cell Update function
        if self.get_status():                                       # if the current cell is alive...
            if self.neighbors < 2:                                  # and it has less than 2 neighbors..
                self.set_status(False)                              # it dies.
            elif self.neighbors == 2 or self.neighbors == 3:        # or if it has 2 or 3 neighbors..
                self.set_status(True)                               # it stays alive
            elif self.neighbors > 3:                                # or if it has more than 3 neighbors..
                self.set_status(False)                              # it dies
        else:                                                       # if the current cell is dead...
            if self.neighbors == 3:                                 # and it has exactly 3 neighbors..
                self.set_status(True)                               # it comes alive

def update_field(field, cell_size, screen, time):               # Global Update function
    pygame.display.flip()                                       # clear the screen
    for x in field:                                             # for every cell in the 2d matrix
        for c in x:                 
            c.set_neighbors(field)                              # update its neighbor count

    for x in field:                                             # loop through every cell in the matrix again
        for c in x:
            c.update()                                          # update the condition of the cell
            c.draw(cell_size, screen)                           # draw it to the screen
    pygame.time.delay(time)                                     # time delay
    pygame.display.update()                                     # update the screen

def print_field(field):                                         # print field function
    string = ""                                                 # empty string initalizer
    for x in field:                                             
        for c in x:
            if c.get_status():
                string += "1 "                                  # concatenate a 1 if the cell is alive
            else:
                string += "0 "                                  # concatenate a 0 if the cell is dead
        string += "\n"                                          # break this line
    print(string)                                               # print resulting string

def main():                                                     # main function
    pygame.init()                                               # initialize pygame module
    run = True                                                  # running boolean
    time_step = 100                                             # time step for the animation
    
    s = open("start.txt", "r")                                  # open 'start.txt'
    first_line = eval(s.readline())                             # read the first line for the configuration tuple
    s.close()                                                   # close file for now

    n, m = first_line[0], first_line[1]                         # get the width, height, and cell size from the tuple
    cell_size = first_line[2]
    
    screen = pygame.display.set_mode((n*cell_size, m*cell_size))    # setup the screen
    pygame.display.set_caption("Conway's Game of Life")             # change caption
    field = []                                                  # initialize the field
    for i in range(n):                      
        field.append([])
        for j in range(m):
            field[i].append(Cell(i, j, False))                  # populate the field with dead cells

    with open("start.txt", "r") as s:                           # open 'start.txt' to retrive the drawing information
        for i, line in enumerate(s):                            # for each line
            if line != first_line:                              # skip the first line
                for j, char in enumerate(line):                 
                    if char == "1":                             # if the current character in the line is a 1
                        field[j][i].set_status(True)            # set the status of the coresponding cell to true

    screen.fill((1, 1, 1))                                      # paint the screen black at the start  

    while run:                                                  # game running loop
        for event in pygame.event.get():                        # event listener
            if event.type == pygame.QUIT:               
                run = False                                     # set 'run' to false if the game closes
        update_field(field, cell_size, screen, time_step)       # update the field every loop
            
    pygame.quit()                                               # quit pygame

main()                                                          # call main function