import numpy as np

cols = 200
rows = 200
cell_w = 1
cell_h = 1

grid = np.zeros((rows, cols))  # 2D grid of dead celsls

def count_neighbors(g):
    n = np.zeros_like(g)  # empty array 
    n[1:,  :]  += g[:-1, :]  # up
    n[:-1, :]  += g[1:,  :]  # down
    n[:,  1:]  += g[:, :-1]  # left
    n[:, :-1]  += g[:,  1:]  # right
    n[1:, 1:]  += g[:-1, :-1] # up and left
    n[1:, :-1] += g[:-1, 1:] # up and right
    n[:-1, 1:] += g[1:, :-1] # down and eft
    n[:-1,:-1] += g[1:, 1:] # down and right
    return n

def setup():
    size(200, 200)
    cx = cols // 2 
    cy = rows // 2 
    grid[cy-4:cy+5, cx-3] = 1   
    grid[cy-4:cy+5, cx+3] = 1   
    grid[cy, cx-3:cx+4] = 1   

def draw(): #i forgot about trans and did trans in draw
    global grid
    background(0)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:
                fill(255, 0, 0)  # alive red
            else:
                fill(0)          # dead black
            no_stroke()
            rect(c * cell_w, r * cell_h, cell_w, cell_h)

    n = count_neighbors(grid)
    alive = grid == 1  
    dead  = grid == 0  
    next_grid = np.zeros_like(grid)
    next_grid[alive & (n % 2 == 0)] = 1
    next_grid[dead & (n % 2 == 1)] = 1
    grid = next_grid
