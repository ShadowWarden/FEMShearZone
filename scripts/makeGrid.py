# Name: Anthony Tracy
# Email: antr9811@colorado.edu

import numpy as np
import argparse

ap=argparse.ArgumentParser()
ap.add_argument("-x",
                type=int,
                required=False,
                default=10,
                help="The number of cells in x-dimension")
ap.add_argument("-y",
                type=int,
                required=False,
                default=10,
                help="The number of cells in y-dimension")
ap.add_argument("-E",
                type=float,
                required=False,
                default=10e5,
                help="The Young's Modulous for the material")
ap.add_argument("-o",  # Forgot the name for the time being
                type=int,
                required=False,
                default=6,
                help="The other term that we need to use... change this later")
ap.add_argument("-gridName",
                type=str,
                required=False,
                default='rename_this',
                help="Name the text file that will be written to")
args=ap.parse_args()


# X / Y dimesnsions of the grid being made
dims=[args.x,args.y]
# Youngs Modulous and stress? <- forgot what the two values neeeded where but they are included in code...
params=[args.E,args.o]

# Total number of elements due to the grid
N = dims[0]*dims[1]-1
print range(N)

# Now to test writting to a file:

file=open(args.gridName+'.txt','w')
file.write("V1 V2 V3 Young's Stress\n")
# This loop is done so that only the wanted elements are made in the right hand rule pattern:
for i in range(N-dims[0]):
  if (i+1)%dims[0]:
    file.write('{0} {1} {2} {3} {4}\n'.format(i, i+1,i+dims[0],params[0],params[1]))
    file.write('{0} {1} {2} {3} {4}\n'.format(i+1, i+1+dims[0],i+dims[0],params[0],params[1]))
file.close()

