import sys; args = sys.argv[1:]
puzzles = open("puzzles.txt", "r").read().splitlines()
# Johanna Lohmus Pd 6
import math
import time

WIDTH = int(math.sqrt(len(puzzles[0])))
SUBWIDTH = int(math.sqrt(WIDTH))
SYMBOLSET = {str(i) for i in range(1, 10)}

LISTOFCONSTRAINTSETS = []
LISTOFCONSTRAINTSETS += [{*range(i, i + WIDTH)} for i in range(0, WIDTH * WIDTH, WIDTH)]
LISTOFCONSTRAINTSETS += [{*range(i, WIDTH * WIDTH, WIDTH)} for i in range(0, WIDTH)]
LISTOFCONSTRAINTSETS+=[{row * WIDTH + col for col in range(j, j+SUBWIDTH) for row in range(i, i + SUBWIDTH)} for i in range(0, WIDTH, SUBWIDTH) for j in range(0, WIDTH, SUBWIDTH)]
PLCSI = [[i for i, c in enumerate(LISTOFCONSTRAINTSETS) if p in c] for p in range(WIDTH * WIDTH)]
LISTOFNEIGHBORS = [set.union(*[LISTOFCONSTRAINTSETS[i] for i in PLCSI[pos]]) - {pos} for pos in
                   range(WIDTH * WIDTH)]

def checkSum(puzzle):
    return sum(ord(char) for char in puzzle) - (len(puzzle) * ord(min(SYMBOLSET)))

def bruteForce(puzzle, dots):
    if '.' not in puzzle:
        return puzzle

    best_pos, best_val, best_possibilities = 82, 0, SYMBOLSET
    if not dots:
        return ""
    for dot in dots:
        lenp = dots[dot][0]
        if lenp == 9:
            return ""
        if lenp == 8:
            best_pos, best_val, best_possibilities = dot, lenp, SYMBOLSET - dots[dot][1]
            break
        if lenp > best_val:
            best_pos, best_val, best_possibilities = dot, lenp, SYMBOLSET - dots[dot][1]

    counted_symbols = False

    if best_val < 8:
        least_num, least_positions = 10, {}
        for symbol in best_possibilities:
            possibilities = {dot for dot in dots if symbol not in dots[dot]}
            if len(possibilities) < (9 - best_val):
                counted_symbols = True
                least_num, least_positions = symbol, possibilities
                break

        if counted_symbols == True:
            for pos in least_positions:
                if pos in dots:
                    new_dots = dict(dots)
                    old_len, old_nums = dots[pos]
                    new_dots[pos] = old_len + 1, set.union(old_nums, least_num)
                    new_puzzle = puzzle[0:pos] + least_num + puzzle[pos + 1:]
                    bf = bruteForce(new_puzzle, new_dots)
                    if bf:
                        return bf

    if counted_symbols == False:
        for symbol in best_possibilities:

            new_dots = dict(dots)
            new_dots.pop(best_pos)
            for dot in new_dots:
                if dot in LISTOFNEIGHBORS[best_pos]:
                    old_len, old_possibilities = new_dots[dot]
                    if symbol not in old_possibilities:
                        new_dots[dot] =  old_len + 1, set.union(old_possibilities, {symbol})
            new_puzzle = puzzle[0:best_pos] + symbol + puzzle[best_pos + 1:]
            bf = bruteForce(new_puzzle, new_dots)
            if bf:
                return bf
    return ""

for index, puzzle in enumerate(puzzles):
    t = time.process_time()
    stime = time.process_time()

    dots = {}
    for idx, char in enumerate(puzzle):
        if char == ".":
            possibilities = {puzzle[i] for i in LISTOFNEIGHBORS[idx] if puzzle[i] != "."}
            dots[idx] = len(possibilities), possibilities

    solved = bruteForce(puzzle, dots)
    etime = time.process_time()
    t = t + (etime - stime)

    spaces = " " * len(str(index + 1))
    print(f'{index + 1}: {puzzle}')
    print(f'  {spaces}{solved} {checkSum(solved)} {str(t)[:4]}s')
# Johanna Lohmus p6 2023
