# Conways Game of Life
### Overview
This is a replica of **Conway's Game of Life** written in Python.
The game is comprised of a 2d vector of Cell objects who each have a boolean state for dead/alive. 
Each cell is responsible for keeping track of its neighbors and updating its own condition.
The program uses Pygame as a visual display of the animation.

The program can read in a design and basic configuration for the program stored in a file called 'start.txt' in the same directory as the python file.

The file is structured like this
(height, width, cell size)
```
00 - - 00
|  \    |
|    \  |
00 - - 00
```
Each 0 represents a dead starting cell, and a 1 is a live starting cell.
Included is a directory of some interesting designs I have found.

### Requirments
* pgame
