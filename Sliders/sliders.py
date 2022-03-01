import sys; args = sys.argv[1:]
#Johanna Lohmus, pd. 6
import time
import math
import random

def neighbors(curr):
    nbors = []
    # finds potential positions of the underscore to switch to either up, down, left, or right
    # swaps underscore with the corresponding number
    # then adds to list of neighbors

    # checks that the underscore is not switched with a number that is on the other side of the puzzle
    # for example, in a 3x3 puzzle, the underscore at index 3 cannot go to index 2
    # makes a list of numbers that the underscore cannot switch to
    minus_nums = [i for i in range(1, len(curr)) if i % width == 0]
    max_nums = [i for i in range(1, len(curr)-1) if i % width == width-1]

    cindex = curr.index("_")
    if cindex - width > -1:
        nbors.append(swap(curr, cindex, cindex - width))
    if cindex - 1 > -1 and cindex not in minus_nums:
        nbors.append(swap(curr, cindex, cindex - 1))
    if cindex + 1 < len(curr) and cindex not in max_nums:
        nbors.append(swap(curr, cindex, cindex + 1))
    if cindex + width < len(curr):
        nbors.append(swap(curr, cindex, cindex + width))
    return nbors

# swaps two items in a string
def swap(string, a, b):
    swap_list = list(string)
    temp = swap_list[a]
    swap_list[a] = swap_list[b]
    swap_list[b] = temp
    return ''.join(swap_list)

def band_print(path, length):

    string = ""
    chunk_start = 0
    chunk_end = width
    i = 0

    while i < width:
        for x in path:
            string += x[chunk_start:chunk_end] + " "
            path_index = path.index(x)+1
            if path_index%length == 0:
                string += "\n"
        chunk_start += width
        chunk_end += width
        i += 1
        string += "\n"
    # splits the string into bands of puzzles
    lines = string.split("\n")

    banded_path = ""
    j = 0
    rows = (round(len(path)/length))
    while j < rows:
        if j != 0:
            lines.pop(0)
        banded_path += "".join(lines[::rows]) + "\n"
        j += 1
    banded_path = banded_path.split()
    banded_print = " "

    if length > len(path):
        length = len(path)

    for i in range(0, len(banded_path), length):
        banded_print += " ".join(banded_path[i:i+length]) + "\n"
    return banded_print

# gets the path of start to goal
def get_path(dict, goal, start):
    if goal == -1:
        return(-1)

        #print(band_print([start], 5))
        #print("Steps: " + str(-1))

    if goal == start:
        return(0)

    # list which starts out with the goal to retrace steps
    path = [goal]
    steps = 0
    # parent of the goal
    parent = dict[goal]
    # while parent is not equal to start, add parent to path and get the parent of the parent
    while parent != start:
        path.append(parent)
        steps += 1
        parent = dict[parent]
    path.append(start)
    # flip the path so it goes from start to goal instead of goal to start
    path = path[::-1]
    steps += 1

    # return 1 if solvable and path length
    return(steps)

    # print path and steps
    #print(band_print(path, 5))
    #print("Steps: " + str(steps))
    #return

def BFS(start, goal):
    # dictionary with key = node, value = parent
    seenNbrs = {start: ""}
    # list with to parse
    parse = [start]

    # if start is goal, then return
    if start == goal:
        return(get_path(seenNbrs, goal, start))

        #print(band_print([start], 3))
        #print("Steps: " + str(0))
        #return 1
    # while there are items in parse, get the first item in the list
    # get the neighbors of the item
    while parse:
        current = parse.pop(0)
        # if the neighbors have not been seen, check if is goal
        for i in neighbors(current):
            if i not in seenNbrs:
                # if yes, get the path and return
                if i == goal:
                    seenNbrs[i] = current
                    return(get_path(seenNbrs, goal, start))
                # if no, add to parse
                parse.append(i)
                seenNbrs[i] = current

    # if no path, band print start and return steps: -1
    # print(band_print([start], 5))
    # print("Steps: " + str(-1))
    return(get_path(seenNbrs, -1, start))


puzzles = args.split("\n")
goal = puzzles.pop(0)
width = int(math.sqrt(len(goal)))
i = 1

while i < len(puzzles):
  start_time = time.time()
  steps = BFS(puzzles[i], goal)
  end_time = time.time()
  time = end_time - start_time
  print("Solved puzzle " + str(i) + " in " + str(steps) + " steps in " + str(time[:3]) + "seconds.")
