import sys; args = sys.argv[1:]

def makeMove(board, token_to_play, move):
    move = int(move)
    new_board = board[:].lower()
    new_board = new_board[:move] + token_to_play.upper() + new_board[move+1:]

    if token_to_play == "x":
        opponent = "o"
    else:
        opponent = "x"

    board = board.lower()
    border = "B" * 10
    for i in range(8):
        row = i * 8
        border += "B" + board[row:row + 8] + "B"
    border += "B" * 10

    row = ((move) // 8) + 1
    col = ((move) % 8) + 1
    const_move = row * 10 + col

    directions = [1, 9, 10, 11, -1, -9, -10, -11]

    for direction in directions:
        new_move = const_move
        flip = []
        if border[new_move + direction] != opponent:
            continue
        while border[new_move + direction] == opponent:
            new_move = new_move + direction
            next = new_move + direction
            row = (new_move) // 10 - 1
            col = (new_move) % 10 - 1
            i = row * 8 + col
            flip.append(i)
        if border[next] == token_to_play and len(flip) > 0:
            for f in flip:
                new_board = new_board[:f] + token_to_play + new_board[f+1:]

    new_board = new_board[:move] + token_to_play.upper() + new_board[move + 1:]
    return new_board

def printBoard(board, poss):
    board2d = ""
    for i in range(0, 64, 8):
        for j in range(i, i+8):
            if j in poss:
                board2d += "*"
            else:
                board2d += board[j]
        board2d += "\n"
    print(board2d)

def allPossibilities(board, token_to_play):
    board = board.lower()
    allMoves = []

    if token_to_play == "x":
        opponent = "o"
    else:
        opponent = "x"

    border = "B" * 10
    for i in range(8):
        row = i*8
        border += "B" + board[row:row+8] + "B"
    border += "B" * 10

    directions = [1, 9, 10, 11, -1, -9, -10, -11]

    for idx, token in enumerate(border):
        if token == token_to_play:
            for direction in directions:
                bracketed_tokens = 0
                current = idx
                if border[current + direction] != opponent:
                    continue
                while border[current + direction] == opponent:
                    current = current + direction
                    next = current + direction
                    bracketed_tokens += 1
                if border[next] == "." and bracketed_tokens > 0:
                    row = (next) // 10 - 1
                    col = (next) % 10 - 1
                    i = row * 8 + col
                    allMoves.append(int(i))
                else:
                    continue
    return allMoves

def safeEdge(move, token_to_play, board):
    opponent = "o"
    if token_to_play == "o":
        opponent = "x"

    # clean up
    if move in [*range(0, 7)]:
        if opponent not in board[0:move] and '.' not in board[0:move] or opponent not in board[move+1:8] and '.' not in board[move+1:8]:
            return True
    if move in [*range(56, 63)]:
        if opponent not in board[56:move] and '.' not in board[56:move] or opponent not in board[move+1:64] and '.' not in board[move+1:64]:
            return True
    if move in [*range(0, 64, 8)]:
        move_row = move//8
        tokens = [board[i] for i in range(0, 64, 8)]
        if opponent not in tokens[0:move_row] and '.' not in tokens[0:move_row] or opponent not in tokens[move_row:8] and '.' not in tokens[move_row:8]:
            return True
    if move in [*range(7, 64, 8)]:
        move_row = move // 8
        tokens = [board[i] for i in range(7, 64, 8)]
        if opponent not in tokens[0:move_row] and '.' not in tokens[0:move_row] or opponent not in tokens[move_row:8] and '.' not in tokens[move_row:8]:
            return True

def quickMove(board, token_to_play):
    moves = allPossibilities(board, token_to_play)
    min_possibilities = 64
    best_move = moves[0]
    corners = []
    safeEdges = []

    most_tokens = 0.0
    if board.count(".") < 6:
        for move in moves:
            move_brd = makeMove(board, token_to_play, move)
            opponent = "o"
            if token_to_play == "o":
                opponent = "x"
            if move_brd.count(opponent) == 0:
                best_move = move
                break
            else:
                curr_tokens = float(move_brd.count(token_to_play)/move_brd.count(opponent))
                if curr_tokens > most_tokens:
                    most_tokens = curr_tokens
                    best_move = move

    else:
        for move in moves:
            if move in [0, 7, 56, 63]:
                corners.append(move)

            if safeEdge(move, token_to_play, board):
                safeEdges.append(move)

            move_brd = makeMove(board, token_to_play, move)

            next_token = "o"
            if token_to_play == "o":
                next_token = "x"

            next_possibilities = allPossibilities(move_brd, next_token)
            hasCorner = False

            for corner in [0,7,56,63]:
                if corner in next_possibilities:
                    hasCorner = True

            if hasCorner == True:
                continue

            if move in [1, 8, 9]:
                if board[0] != token_to_play:
                    continue
            if move in [6, 14, 15]:
                if board[7] != token_to_play:
                    continue
            if move in [48, 49, 57]:
                if board[56] != token_to_play:
                    continue
            if move in [62, 55, 54]:
                if board[63] != token_to_play:
                    continue

            if len(next_possibilities) < min_possibilities:
                min_possibilities = len(next_possibilities)
                best_move = move

        min_edge_possibilities = 64
        if safeEdges:
            for edge in safeEdges:
                move_brd = makeMove(board, token_to_play, edge)

                next_token = "o"
                if token_to_play == "o":
                    next_token = "x"

                next_possibilities = allPossibilities(move_brd, next_token)
                hasCorner = False

                for c in [0, 7, 56, 63]:
                    if c in next_possibilities:
                        hasCorner = True

                if hasCorner == True:
                    continue
                if len(next_possibilities) <= min_edge_possibilities and len(next_possibilities) < min_possibilities + 3:
                    min_edge_possibilities = len(next_possibilities)
                    best_move = edge

        min_corner_possibilities = 64
        if corners:
            for corner in corners:
                move_brd = makeMove(board, token_to_play, corner)

                next_token = "o"
                if token_to_play == "o":
                    next_token = "x"

                next_possibilities = allPossibilities(move_brd, next_token)
                hasCorner = False

                for c in [0, 7, 56, 63]:
                    if c in next_possibilities:
                        hasCorner = True

                if hasCorner == True:
                    continue
                if len(next_possibilities) <= min_corner_possibilities:
                    min_corner_possibilities = len(next_possibilities)
                    best_move = corner

    return best_move

def main():
    board = "...........................ox......xo..........................."
    token_to_play = "x"
    moves = []
    alpha = "abcdefgh"

    # globals
    corners = [0,7,56,63]

    hasToken = False

    if args:
        for arg in args:
            if arg in "xXoO":
                hasToken = True
                token_to_play = arg.lower()
            elif len(arg) == 64:
                board = arg.lower()
            else:
                if arg[0].isalpha():
                    arg = arg.lower()
                    col = alpha.index(arg[0])
                    row = int(arg[1]) - 1
                    num = row * 8 + col
                    moves.append(int(num))
                elif int(arg) >= 0:
                    moves.append(int(arg))

    if hasToken == False:
        if not allPossibilities(board, "x"):
            token_to_play = "o"
        elif not allPossibilities(board, "o"):
            token_to_play = "x"
        elif board.count("o") < board.count("x"):
            token_to_play = "o"

    poss_moves = allPossibilities(board, token_to_play)
    if moves and moves[0] not in poss_moves:
        if token_to_play == "x":
            token_to_play = "o"
        else:
            token_to_play = "x"
    poss_moves = allPossibilities(board, token_to_play)
    string_moves = ", ".join(str(move) for move in poss_moves)
    printBoard(board, poss_moves)
    print(f'{board} {board.lower().count("x")}/{board.lower().count("o")}')
    print(f'Possible moves for {token_to_play}: {string_moves}')
    print()

    for move in moves:
        poss_moves = allPossibilities(board, token_to_play)
        if move not in poss_moves:
            if token_to_play == "x":
                token_to_play = "o"
            else:
                token_to_play = "x"
        board = makeMove(board, token_to_play, move)
        print(f'{token_to_play} moves to {move}')

        if token_to_play == "x":
            token_to_play = "o"
        else:
            token_to_play = "x"

        poss_moves = allPossibilities(board, token_to_play)
        if not poss_moves:
            if token_to_play == "x":
                token_to_play = "o"
            else:
                token_to_play = "x"
            poss_moves = allPossibilities(board, token_to_play)
        string_moves = ", ".join(str(move) for move in poss_moves)

        printBoard(board, poss_moves)
        print(f'{board} {board.lower().count("x")}/{board.lower().count("o")}')

        print(f'Possible moves for {token_to_play}: {string_moves}')
        print()

if __name__ == '__main__': main()

# Johanna Lohmus p6 2023
