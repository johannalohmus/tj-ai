import sys; args = sys.argv[1:]
import time
puzzle = []
"""
for arg in args:
    if "x" in arg:
        items = arg.split("x")
        puzzle.append(items[0])
        puzzle.append(items[1])
    if "X" in arg:
        items = arg.split("X")
        puzzle.append(items[0])
        puzzle.append(items[1])
    if "X" not in arg and "x" not in arg:
        puzzle.append(arg)
"""

def findDecomposition(pzl):
    visualize(pzl)
    seen = []
    decomposition = "Decomposition: "
    if pzl == "":
        return("No solution")
    for row in pzl:
        for item in row:
            if item[2] not in seen:
                seen.append(item[2])
                decomposition += str(item[0]) + "x" + str(item[1]) + " "
    return decomposition

def visualize(pzl):
    s = ""
    for k in range(0, H):
        for l in range(0, W):
            if pzl[k][l] != ".":
                s += str(pzl[k][l][0]) + "," + str(pzl[k][l][1]) + " "
            else:
                s += ".   "
        s+= "\n"
    s += "\n"
    print(s)

def isPossible(pzl, height, width, row, col):
    # checks if the edges of the block fit onto the main rectangle or if there are any blocks
    if row + height > H or col + width > W:
        return False
    for x in range(width):
        if pzl[row + height - 1][col + x] != ".":
            return False
        if pzl[row][col + x] != ".":
            return False
    for y in range(height):
        if pzl[row + y][col + width - 1] != ".":
            return False
        if pzl[row + y][col] != ".":
            return False
    return True

def placeBlock(pzl, height, width, row, col, id):
    new_pzl = [item[:] for item in pzl]
    for x in range(row, row+height):
        for y in range(col, col+width):
            new_pzl[x][y] = (height, width, id)
    return new_pzl

def findBlock(pzl, blocks):
    # if no more blocks left to use, return puzzle
    if not blocks:
        return pzl
    # finds the first open position
    col = -1
    row = -1
    for i in range(H):
        if row != -1:
            break
        for j in range(W):
            if pzl[i][j] == ".":
                row = i
                col = j
                break
    for block in blocks:
        height, width = block[2], block[3]
        id = block[1]
        #check if block is possible in given row and column (position)
        if isPossible(pzl, height, width, row, col):
            # finds the new puzzle with the block as well as the positions it took up
            new_pzl = placeBlock(pzl, height, width, row, col, id)
            # removes the block from the total blocks remaining
            new_blocks = [item for item in blocks if item[1] != id]
            # calls findBlock on the new puzzle
            bf = findBlock(new_pzl, new_blocks)
            if bf:
                return bf
    return ""

puzzle = [15,15, 9,4, 6,11, 10,5, 4,7, 5,5, 3,6]
H = int(puzzle[0])
W = int(puzzle[1])
pzl = [["." for i in range(W)] for j in range(H)]

blocks = []
total_area = 0

for i in range(2, len(puzzle), 2):
    num1 = int(puzzle[i])
    num2 = int(puzzle[i+1])
    area = num1*num2
    total_area += area
    if num1 == num2:
        blocks.append((area, i, num1, num2))
    else:
        blocks.append((area, i, num1, num2))
        blocks.append((area, i, num2, num1))

blocks =  sorted(blocks)[::-1]

if total_area < W * H:
    for i in range(W*H - total_area):
        blocks.append((1, i*100, 1, 1))

if total_area > W * H:
    ans = ""

else:
    t = time.process_time()
    ans = findBlock(pzl, blocks)
    etime = time.process_time()

print(findDecomposition(ans))
print(etime - t)
# Johanna Lohmus p6 2023
