In this folder I was aiming to just have python scripts.

makeGrid.py takes 5 arguments. None of them are required as they all have defaults set for them. They are as follows

  -x        : the x dimension of the grid.                       : Default=10
  -y        : the y dimension of the grid.                       : Default=10
  -E        : young's modulous for the material used in the grid : Default=10e5
  -o        : the other parameter that I forgot the name of...   : Default=6
  -gridName : the name of the txt file that will be saved        : Default='rename_this'

Things I am thinking of adding / changing:

  1. set this to take in lists for x,y,E, and o. The idea I am thinking is to be able to 
     make a grid of multiple materials. Such that the x[0],y[0] have E[0] and o[0] parameters.
      - For this the easy next step would be to only let x or y change. Not both. Not until I think
        about it enough to find a way to add certain values in the center...
  2. change the -o command to whatever it should be I just have o for o(ther) for the time being.
  3. 
