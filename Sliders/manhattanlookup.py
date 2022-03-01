import sys;args = sys.argv[1:]
puzzles = open("puzzles.txt", "r").read().splitlines()
# Johanna Lohmus, pd. 6
import time
import math

neighbors_lookup = {}

def neighbors(curr):
    nbors = []
    # checks if neighbors are already in the lookup table
    if curr in neighbors_lookup:
        return neighbors_lookup[curr]

    # finds potential positions of the underscore to switch to either up, down, left, or right
    # swaps underscore with the corresponding number
    # then adds to list of neighbors

    # checks that the underscore is not switched with a number that is on the other side of the puzzle
    # for example, in a 3x3 puzzle, the underscore at index 3 cannot go to index 2
    else:
        cindex = curr.index("_")
        if cindex - width > -1:
            nbors.append(swap(curr, cindex, cindex - width))
        if cindex - 1 > -1 and cindex % width != 0:
            nbors.append(swap(curr, cindex, cindex - 1))
        if cindex + 1 < len(curr) and (cindex % width) != (width - 1):
            nbors.append(swap(curr, cindex, cindex + 1))
        if cindex + width < len(curr):
            nbors.append(swap(curr, cindex, cindex + width))
        neighbors_lookup[curr] = nbors
    return nbors

# swaps two items in a string
def swap(string, a, b):
    swap_list = [*string]
    temp = swap_list[a]
    swap_list[a] = swap_list[b]
    swap_list[b] = temp
    return ''.join(swap_list)

# determines path using difference between parent and child underscore indexes
def get_pos(node, parent):
    p_index = parent.index("_")
    n_index = node.index("_")

    return position_lookup[p_index - n_index]

def count_inversion(puzzle):
    count_and_spacepos = []
    space_pos = puzzle.index("_") // 4 + 1
    puzzle = puzzle.replace("_", "")
    count = 0

    for i in range(len(puzzle)):
        for j in range(0, i):
            if puzzle[j] > puzzle[i]:
                count += 1
    count_and_spacepos.append(count % 2)
    count_and_spacepos.append(space_pos % 2)
    return count_and_spacepos

incremental_manhattan_lookup = {}
manhattan_position_lookup = {}

def incremental_manhattan(f_parent, parent, child):
    swapped_char = ""

    for i in range(len(parent)):
        if parent[i] != "_":
            if parent[i] != child[i]:
                swapped_char = parent[i]
                parent_pos = i
                child_pos = child.index(swapped_char)

    #if (swapped_char, parent_pos, child_pos) in incremental_manhattan_lookup:
    #    return f_parent + incremental_manhattan_lookup(swapped_char, parent_pos, child_pos)

    final_pos = manhattan_lookup[swapped_char]

    #if (swapped_char, parent_pos) in manhattan_position_lookup:
    #    parent_count = manhattan_position_lookup[(swapped_char, parent_pos)]
    #else:
    parent_count = 0
    while parent_pos != final_pos:
        if parent_pos > final_pos and parent_pos // width > final_pos // width:
            parent_pos -= 4
            parent_count += 1
        elif parent_pos < final_pos and parent_pos // width < final_pos // width:
            parent_pos += 4
            parent_count += 1
        else:
            parent_count += abs(parent_pos - final_pos)
            parent_pos = final_pos
    manhattan_position_lookup[(swapped_char, parent_pos)] = parent_count

    #if (swapped_char, child_pos) in manhattan_position_lookup:
    #    child_count = manhattan_position_lookup[(swapped_char, child_pos)]
    #else:

    #gets manhattan distance of tile in child
    child_count = 0
    while child_pos != final_pos:
        if child_pos > final_pos and child_pos // width > final_pos // width:
            child_pos -= 4
            child_count += 1
        elif child_pos < final_pos and child_pos // width < final_pos // width:
            child_pos += 4
            child_count += 1
        else:
            child_count += abs(child_pos - final_pos)
            child_pos = final_pos
    #manhattan_position_lookup[(swapped_char, child_pos)] = child_count

    difference = child_count - parent_count
    #incremental_manhattan_lookup[swapped_char, parent_pos, child_pos] = difference
    return(f_parent + difference)

def initial_manhattan_count(start):
    total_count = 0
    for i in range(len(start)):
        if start[i] != "_":
            pos = start.index(start[i])
            final_pos = manhattan_lookup[start[i]]
            count = 0
            while pos != final_pos:
                if pos > final_pos and pos//width > final_pos//width:
                    pos -= 4
                    count += 1
                elif pos < final_pos and pos//width < final_pos//width:
                    pos += 4
                    count += 1
                else:
                    count += abs(pos - final_pos)
                    pos = final_pos
            total_count += count
    return total_count

# gets the path of start to goal
def get_path(dict, goal, start):
    if goal == -1:
        return ("X")

    if goal == start:
        return (0)

    # list which starts out with the goal to retrace steps
    path = []

    # parent of the goal
    parent = dict[goal]
    path.append(get_pos(goal, parent))

    # while parent is not equal to start, add parent to path and get the parent of the parent
    while parent != start:
        path.append(get_pos(parent, dict[parent]))
        parent = dict[parent]

    # flip the path so it goes from start to goal instead of goal to start
    path = path[::-1]

    # return 1 if solvable and path length
    path = ''.join(path)
    return (path)

def AStar(start, goal):
    parents = {start: ""}
    if start == goal:
        return (get_path(parents, goal, start))

    # gets inversion count of start
    start_inv_count = count_inversion(start)
    openSet = []

    # creates list of buckets with a length of 65
    for i in range(65):
        bucket = [0]
        openSet.append(bucket)
    openSet[0].append((initial_manhattan_count(start), start, 0))
    counter = 0
    closedSet = {}

    # checks if puzzle is possible through inverse counts
    if width % 2 == 0:
        if (((start_inv_count[1] - goal_inv_count[1]) % 2) + start_inv_count[0]) % 2 != goal_inv_count[0]:
            return (get_path(parents, -1, start))
    else:
        if start_inv_count[0] != goal_inv_count[0]:
            return (get_path(parents, -1, start))

    # traversing through the bucket list which is essentially a priority queue
    while openSet:
        #for current in reversed(openSet[counter]):
        while openSet[counter]:
            # goes through the bucket in reverse
            current = openSet[counter].pop(-1)
            if current == 0:
                continue
            current_manhattan = current[0]
            current_puzzle = current[1]
            current_level = current[2]

            if current_puzzle in closedSet:
                continue
            # adds puzzle to closedSet so that it is not checked again
            closedSet[current_puzzle] = current_level + 1

            # traversing through each neighbor and checking if goal
            for nbor in neighbors(current_puzzle):
                if nbor == goal:
                    parents[nbor] = current_puzzle
                    return(get_path(parents, goal, start))
                if nbor in closedSet:
                    continue
                else:
                    # finds manhattan value using incremental
                    manhattan = incremental_manhattan(current_manhattan, current_puzzle, nbor)
                    f = current_level + 1 + manhattan
                    parents[nbor] = current_puzzle
                    # adds puzzle to bucket list according to its f value
                    openSet[f].append((manhattan, nbor, current_level + 1))
                    if f < counter:
                        counter = f
        counter += 1

goal = puzzles[0]
goal_inv_count = count_inversion(goal)
width = int(math.sqrt(len(goal)))
i = 0

t = time.process_time()
manhattan_lookup = {}
position_lookup = {-1: "R", -width: "D", width: "U", 1: "L"}

while i < len(puzzles):
    stime = time.process_time()
    path = AStar(puzzles[i], goal)
    etime = time.process_time()
    t = t + (etime - stime)
    # sets the lookup table for the goal
    for num in range(len(goal)):
        if goal[num] != "_":
            manhattan_lookup[goal[num]] = goal.index(goal[num])
    if not path:
        path = "G"
    print(puzzles[i] + " solved in " + str(t)[:4] + " secs => path " + path)
    i += 1
    #if t > 10:
    #    break
# Johanna Lohmus p6 2023
