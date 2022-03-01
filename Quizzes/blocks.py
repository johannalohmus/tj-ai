import sys; args = sys.argv[1:]
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
puzzle = [11, 12, 3, 6, 2, 5, 4, 10, 7, 9, 1, 1]

def placeBlock(pos, pzl, width, height):
    place = pos
    new_pzl = pzl[:]
    for j in range(height):
        for i in range(width):
            new_pzl[pos] = (height, width)
            pos = pos + 1
        pos = pos - width + W
    return new_pzl

def findDecomposition(pzl):
    seen = []
    ans = []
    if pzl == "":
        return("Puzzle has no solution")
    for item in pzl:
        if item not in seen:
            seen.append(item)
            ans.append(item)

    decomposition = "Decomposition: "
    for block in ans:
        decomposition += str(block[0]) + "x" + str(block[1]) + " "
    return decomposition

def isPossible(pos, pzl, width, height):
    row = pos//W
    for j in range(height):
        for i in range(width):
            if pos >= H * W or pzl[pos] != ".":
                return False
            new_row = pos//W
            if new_row != row:
                return False
            pos += 1
        pos = pos - width + W
        row = pos//W
    return True

def possibilities(height, width, pzl):
    not_possible = set(idx for idx,val in enumerate(pzl) if val != ".")
    possibilities = set()
    poss_rows = W - width + 1
    poss_cols = H - height + 1
    pos = 0
    for j in range(poss_cols):
        for i in range(poss_rows):
            if pos < W * H and pos + width < (pos//W + 1) * W and pos + (height-1) * W < W*H:
                possibilities.add(pos)
            pos = pos + 1
        pos = pos - width + W - 1
    possibilities = possibilities - not_possible
    possibilities2 = possibilities.copy()
    for poss in possibilities2:
        temp = poss
        for j in range(height):
            for i in range(width):
                if temp in not_possible:
                    possibilities.discard(poss)
                    break
                temp += 1
            temp = temp - width + W
    return possibilities

def findBlock(pzl, blocks, used):
    # check if possible
    if len(used) == len(blocks)/2:
        print(pzl)
        return pzl
    for block in blocks:
        height = block[0]
        width = block[1]
        if block not in used:
            possible_positions = possibilities(height, width, pzl)
            if possible_positions:
                for pos in possible_positions:
                    new_pzl = placeBlock(pos, pzl, width, height)
                    new_used = used[:]
                    new_used.append((width, height))
                    new_used.append((height, width))
                    bf = findBlock(new_pzl, blocks, new_used)
                    if bf:
                        return bf
    return ""

H = int(puzzle[0])
W = int(puzzle[1])
pzl = ["."] * (W*H)

blocks = []

for i in range(2, len(puzzle), 2):
    num1 = int(puzzle[i])
    num2 = int(puzzle[i+1])
    blocks.append((num1, num2))
    blocks.append((num2, num1))

used = []
ans = findBlock(pzl, blocks, used)
print(findDecomposition(ans))
# Johanna Lohmus p6 2023
