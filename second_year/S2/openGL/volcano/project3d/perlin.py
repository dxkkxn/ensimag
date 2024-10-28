import random
import numpy as np

def randomGrid(width, height):
    values = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            values[i][j] = np.random.random()
    return values

def noise(x, y, grid):
    width, height = np.shape(grid)
    return grid[int(x * width % width)][int(y * height % height)] / 2

def perspace(length, count): # linspace version perlin
    delta = length / count
    return np.arange(-delta, length + 2*delta, delta) / length
    
def control(x, contX, width):
    xlim = contX[contX.size - 2]
    if x < 0 or x > xlim:
        return -1        
    if x == xlim:
        indX = contX.size - 3
    else:
        for i in range(1, contX.size-2):
            if x >= contX[i] and x < contX[i+1]:
                indX = i
                break
    card = contX.size - 3
    return contX[indX-1:indX+3], int((indX-1)*width/card), int(indX*width/card)

def bicubic(t, vecf):
    M = np.array([
        [0, 1, 0, 0], 
        [-0.5, 0, 0.5, 0],
        [1, -2.5, 2, -0.5],
        [-0.5, 1.5, -1.5, 0.5]])
    return np.dot(np.matmul(np.array([1, t, t*t, t*t*t]), M), vecf)

def perlinNoise(width, height, nx, ny, octave):
    rand = randomGrid(32, 32)
    grid = np.zeros((width, height))
    fact = pow(2, octave)
    contX = perspace(width, nx*fact)
    contY = perspace(height, ny*fact)
    loc = np.zeros((4, 4))      
    for I in range(1, contX.size-1):
        x0 = contX[I]
        locX, sx, ex = control(x0, contX, width)
        for J in range(1, contY.size-1):
            y0 = contY[J]
            locY, sy, ey = control(y0, contY, height)       
            for i in range(4):
                for j in range(4):
                    randFact = pow(np.pi, octave)
                    x, y = locX[i], locY[j]
                    h = noise(x*randFact, y*randFact, rand) / fact
                    loc[j][i] = rules(x, y, h, octave)
            for i in range(sx, ex):
                x = i/(width-1)
                normX = f(x, locX[1], locX[2])
                x1, x2, x3, x4 = bicubic(normX, loc[0]), bicubic(normX, loc[1]), bicubic(normX, loc[2]), bicubic(normX, loc[3])
                for j in range(sy, ey):
                    y = j/(height-1)
                    normY = f(y, locY[1], locY[2])                    
                    res = bicubic(normY, np.array([x1, x2, x3, x4]))
                    grid[i][j] = res               
    return grid         

def f(x, x0, x1):
    return (x-x0)/(x1-x0)            

def rules(x,y, random_height, octave):
    volcan_height = volcan_rules(x, y, random_height, octave)
    lac_height = 0#lac_rules(x, y)
    return volcan_height + lac_height

def lac_rules(x,y):
    lac_x = 0.2
    lac_y = 0.2
    rayon = 0.2/2
    depth = 1
    dist_lac = ((x-lac_x)**2 + (y-lac_y)**2)**0.5
    if dist_lac <= rayon:
        return-(f(dist_lac, rayon, 0)**2)*depth 
    else:
        return 0

def volcan_rules(x,y, h, o):
    volcan_x = 0.5
    volcan_y = 0.5
    large_rayon = 0.3/4
    tiny_rayon = 0.1/4
    volcan_height = 3
    dist_volcan = ((x-volcan_x)**2 + (y-volcan_y)**2)**0.5
    if dist_volcan <= tiny_rayon:
        return ((np.sin(x*np.pi - np.pi/2)+1)/2)**4*volcan_height
    elif large_rayon >= dist_volcan > tiny_rayon:
        return 3*h + f(dist_volcan, large_rayon, tiny_rayon)*volcan_height
    else:
        if o <= 1:
            return 3*h
        return 0

def completeNoise(width, height, nx, ny, octave, amp):
    grid = np.zeros((width, height))
    for i in range(octave):
        grid += amp*perlinNoise(width, height, nx, ny, i)
    return grid
