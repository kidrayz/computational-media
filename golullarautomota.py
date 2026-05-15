import numpy as np

cols = 40
rows = 40
cell_w = 5
cell_h = 5

grid = np.zeros((rows, cols))

def draw_H():
    cx = cols // 2
    cy = rows // 2
    grid[cy-4:cy+5, cx-3] = 1
    grid[cy-4:cy+5, cx+3] = 1
    grid[cy, cx-3:cx+4] = 1

def count_neighbors(g):
    n = np.zeros_like(g)

    # all 8 directions
    n[1:,  :]  += g[:-1, :]     # up
    n[:-1, :]  += g[1:,  :]     # down
    n[:,  1:]  += g[:, :-1]     # left
    n[:, :-1]  += g[:,  1:]     # right
    n[1:, 1:]  += g[:-1, :-1]   # up-left
    n[1:, :-1] += g[:-1, 1:]    # up-right
    n[:-1, 1:] += g[1:, :-1]    # down-left
    n[:-1, :-1]+= g[1:, 1:]     # down-right

    return n

def setup():
    size(200, 200)
    draw_H()

def draw():
    global grid
    background(0)

    # draw cells
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1:
                fill(255, 0, 0)
            else:
                fill(0)
            no_stroke()
            rect(c * cell_w, r * cell_h, cell_w, cell_h)

    n = count_neighbors(grid)
    alive = grid == 1
    dead  = grid == 0

    next_grid = np.zeros_like(grid)

    # Conway's Game of Life rules:
    # 1. Any live cell with 2 or 3 neighbors survives
    next_grid[alive & ((n == 2) | (n == 3))] = 1

    # 2. Any dead cell with exactly 3 neighbors becomes alive
    next_grid[dead & (n == 3)] = 1

    # everything else stays dead (default 0)
    grid = next_grid
