import numpy as np

def setup_pixels():
    state = [[82, 107, 49],[88, 76, 58],[16, 12, 8],[215, 207, 206]] #list of the colors 
    for y in range(height): #loop every y value 
        for x in range(width): #loop every x value
            np_pixels[y,x,1:] = state[int(random(4))] #set the color
    update_np_pixels() #load friggin pixels yo
    
def setup():
    global p
    size(200,200)
    p = [[]]
    background(0)
    load_np_pixels()
    setup_pixels()
    
def evaluate_neighbors():
    global p
    for y in range(1, height-1):
        for x in range(1, width-1):
            np_pixels[y-1:y+1, x-1:x+1, 1:]
            
            
    
def trans():
    update_np_pixels()
    
def draw():
    evaluate_neighbors()
    trans()
