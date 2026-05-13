import numpy as np
# colors: green and red
clrs = [[255,0,0], [0,255,0]]
def setup_pixels():
    for x in range(width):
        for y in range(height):
            np_pixels[y,x,1:] = clrs[ int(random(2)) ]
    update_np_pixels()
    
def setup():
  global s
  size(250,250)
  s=[[ [[0,0,0] for i in range(8)] for x in range(width)] for y in    range(height)] # empty state list
  background(0) # black
  load_np_pixels()
  setup_pixels()
  
def evaluate_neighbors():
  global s
  for x in range(1,width-1):   # ignore edges
    for y in range(1,height-1):

      # grab the colors of all 8 neighbors (and itself)
      s[x][y]=[ list(c) for pxls in np_pixels[y-1:y+2, x-1:x+2, 1:] for c in pxls ]
      
      # take out the pixel itself
      s[x][y].pop(4)
      
def transition():
    for x in range(1,width-1):
        for y in range(1,height-1):
          # check for each color
          inx = [0]*len(clrs) # use the index as a color count
          for clr in s[x][y]:
              for i in range(2):
                  if clr == clrs[i]:
                    inx[i] +=1 # index of the matching color
     # grab the index of the mode	      
          clr_mode = inx.index( max(inx) )
          # update that pixel’s color		
          np_pixels[y,x,1:] = clrs[ clr_mode ] 
    update_np_pixels()

