import sys; args = sys.argv[1:]
words = open("words.txt", "r").read()

words = words.split("\n")

import time

start_time = time.time()

if len(args) > 1:
    first = args[1]
    second = args[2]
else:
    first = "shades"
    second = "shares"

# get neighbors of given word
def get_neighbors(key):
    neighbors = []
    for word in words:
        diff_letters = 0
        i = 0
        # if words have exactly 5 matching characters, add to neighbors
        if key != word:
            while i < 6:
                if diff_letters > 1:
                    break
                if key[i] != word[i]:
                    diff_letters += 1
                i += 1
            if diff_letters == 1:
                neighbors.append(word)
    return neighbors

# find connected components of graph
def connected_components(graph):
    seen = []
    seenNbrs = []
    # list to store every connected component
    all_connected = []
    # for each word in the graph...
    for i in graph:
        parse = [i]
        path = []
        # while there are items in parse...
        for current in parse:
            # if first item has not yet been seen as a starting points...
            if current not in seen:
                for x in graph.get(current):
                    # if the neighbors have not yet been seen as neighbors...
                    if x not in seenNbrs:
                        # append to parse and seenNeighbors
                        parse.append(x)
                        path.append(x)
                        seenNbrs.append(x)
            seen.append(current)

        # check if length of path is greater than 0 to avoid adding empty lists if vertex has already been seen
        if len(path) > 0:
            all_connected.append(path)

        # if there are no connecting neighbors, add the vertex to every connected component list
        if len(graph.get(i)) == 0:
            all_connected.append([i])
    return(all_connected)

def shortest_path(graph, start, end):
    seenNbrs = []
    # list to hold potential paths
    parse = [[start]]

    if start == end:
        return [start]

    for path in parse:
        # get the most recently added node of a path to check its neighbors
        last_item = path[-1]
        if last_item not in seenNbrs:
            for neighbor in graph.get(last_item):
                # convert path to list and add neighbor to it, then add to parse
                path_with_neighbor = list(path)
                path_with_neighbor.append(neighbor)
                parse.append(path_with_neighbor)

                # if the most recently added node of a path is the goal, return path
                if path_with_neighbor[-1] == end:
                    return path_with_neighbor
        # add to seenNbrs to avoid recounting
        seenNbrs.append(last_item)
    return -1

# construct the graph by finding neighbors of all words
def all_word_neighbors(words):
    dict = {}
    for word in words:
        dict[word] = get_neighbors(word)
    return dict

# check if connected components are in a klique
def klique(graph, item):
    for x in item:
        # if the neighbors of all the vertices in the list are equal to the list...
        # aka if all the vertices are only connected to one another
        neighbors = graph.get(x) + [x]
        if sorted(neighbors) != sorted(item):
                return False
    return True

def wordLadder(words):
    max_degree = 0
    edge_count = 0
    seenSize = set()
    max_size = 0
    connected_two = 0
    connected_three = 0
    connected_four = 0
    max_length = 0
    farthest = ""

    # finds neighbors of all words
    graph = all_word_neighbors(words)

    # gets the number of total edges as well as the highest degree
    for word in graph:
        edge_num = len(graph.get(word))
        if edge_num > max_degree:
            max_degree = edge_num
        edge_count += edge_num

    # creates degree list
    degree_list = [0] * (max_degree + 1)
    for word in graph:
        degree_list[len(graph.get(word))] += 1

    # prints word count
    print("Word count: " + str(len(graph)))

    # prints edge count
    print("Edge count: " + str(edge_count//2))

    # prints degree list
    print("Degree list: " + " ".join(str(i) for i in degree_list))

    # prints construction time
    print("Construction time: " + str((round(time.time() - start_time, 1))) + "s")
    if first != "":
        # finds connected components of all words
        connectedcomponents = connected_components(graph)
        print(connectedcomponents)
        # calculates unique lengths of connected components, largest connected component, and # of k2, k3, and k4 connected components
        for i in connectedcomponents:
            seenSize.add(len(i))
            # if len(i) > max_size:
            #    max_size = len(i)
            if len(i) == 2:
                connected_two += 1
            if len(i) == 3:
                if klique(graph, i):
                    connected_three += 1
            if len(i) == 4:
                if klique(graph, i):
                    connected_four += 1
            if first in i:
                for x in i:
                    path = len(shortest_path(graph, first, x))
                    if path > max_length:
                        farthest = x
                        max_length = path

        # finds list of words with second highest degree and prints out first one
        second_highest_degree = max_degree - 1
        second_degree_words = []
        for word in graph:
            if len(graph.get(word)) == second_highest_degree:
                second_degree_words.append(word)


        # prints example of word of 2nd highest degree
        print("Second degree word: " + second_degree_words[0])

        # number of different connected component sizes
        print("Connected component size count: " + str(len(seenSize)))

        # largest connected component size
        print("Largest component size: " + str(max(len(i) for i in connectedcomponents)))

        # number of k2 connected components
        print("K2 count: " + str(connected_two))

        # number of k3 connected components
        print("K3 count: " + str(connected_three))

        # number of k4 connected components
        print("K4 count: " + str(connected_four))

        # neighbors of first input word
        print("Neighbors: " + " ".join(graph.get(first)))

        #word that is farthest from first input word
        print("Farthest: " + farthest)

        # shortest path from first input to second input
        path = shortest_path(graph, first, second)
        if path == -1:
            print("Path: No path found.")
        else:
            print("Path: " + " ".join(path))

wordLadder(words)

# Johanna Lohmus p6 2023
