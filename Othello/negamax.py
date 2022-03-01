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
    allMoves = set()

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
                    allMoves.add(int(i))
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

cache = {}

def negamax(board, token_to_play, depth):
    key = (board, token_to_play)
    if token_to_play == "x":
        opponent = "o"
    else:
        opponent = "x"

    if key in cache:
        return cache[key]

    moves = allPossibilities(board, token_to_play)

    min_score = 10000
    best_move_path = []

    if not moves:
        opp_moves = allPossibilities(board, opponent)
        if not opp_moves:
            return_val = (board.count(token_to_play) - board.count(opponent), [])

            return return_val
        score, move_path = negamax(board, opponent, depth -  1)
        if score < min_score:
            min_score = score
            best_move_path = move_path[:]
            best_move_path.append(-1)

    for move in moves:
        new_board = makeMove(board, token_to_play, move).lower()
        key = (board, token_to_play)
        if key in cache:
            score, move_path = cache[key]
        else:
            score, move_path = negamax(new_board, opponent, depth - 1)
        if score < min_score:
            min_score = score
            best_move_path = move_path[:]
            best_move_path.append(move)
            if depth == 0:
                print(f'Best move: {best_move_path[-1]}')
                print(f'Min score: {min_score}; move sequence: {best_move_path}')

    return_val = (-1*min_score, best_move_path)
    cache[key] = return_val
    return return_val

def quickMove(board, token_to_play):
    score = 1000

    if board.count(".") < 11:
        score, best_move = negamax(board, token_to_play, 0)

    else:
        moves = allPossibilities(board, token_to_play)
        min_possibilities = 64
        best_move = list(moves)[0]

        for move in moves:
            if move in [0, 7, 56, 63]:
                best_move = move
                break

            if safeEdge(move, token_to_play, board):
                best_move = move
                break

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
    return (score, best_move)

def show2D(brd, tkn, mv, findMovesFunc):
    # Display a snapshot:
    # Move played, 2D board, 1D board w. score, psbl moves
    # brd is a string, tkn just moved to mv
    next = 'xo'[tkn=="x"]
    psblMv = findMovesFunc(brd, next) # Possible moves
    if not psblMv: # If one side must pass
        psblMv = findMovesFunc(brd, (next:=tkn))
    brdL = [*brd] # Listify brd to show asterisks
    for m in psblMv: brdL[m] = "*"
    brdL[mv] = brdL[mv].upper() # Show most recent move
    b2 = "".join(brdL)
    print(f"'{tkn}' played to {mv}")
    print("\n".join([b2[rs:rs+8] for rs in range(0,len(b2),8)]))
    print(f"\n{brd} {brd.count('x')}/{brd.count('o')}")
    if psblMv: # If game not over, show possible moves
        print(f"Possible moves for '{next}': {sorted([*psblMv])}\n")

def playGame(findBestMove, findMoves, makeMove, token):
    # plays a game between findBestMove and Random
    # findMove(brd, tkn)
    # findBestMove(brd, tkn, psblMoves)
    # makeMove(brd, tkn, mv, psblMoves)
    # Csaba Gabor, 10 Dec 2021
    brd = '.'*27+'ox......xo'+'.'*27 # Starting board
    tknToPlay = 'x'
    transcript = [] # Transcript of the game
    while True:
        if not (moves:=findMoves(brd, tknToPlay)):
            tknToPlay = 'xo'[tknToPlay=='x'] # Swap players if pass
            if not (moves:=findMoves(brd, tknToPlay)): break
            transcript.append(-1) # Note the pass
        if tknToPlay != token: # if it's Random's turn:
            transcript.append(random.choice([*moves]))
            brd = makeMove(brd, tknToPlay, transcript[-1])
            show2D(brd, tknToPlay, transcript[-1], findMoves)
        else: # else it's Our turn
            transcript.append(findBestMove(brd, tknToPlay))
            brd = makeMove(brd, tknToPlay, transcript[-1])
            show2D(brd, tknToPlay, transcript[-1], findMoves)
        brd = brd.lower() # Just in case
        tknToPlay = 'xo'[tknToPlay=='x'] # Switch to other side

    # Game is over:
    tknCt = brd.count(token)
    enemy = len(brd) - tknCt - brd.count('.')
    print(f"\nScore: Me as {token=}: {tknCt} vs Enemy: {enemy}\n")
    xscript = [f"_{mv}"[-2:] for mv in transcript]
    print(f"Game transcript: {''.join(xscript)}")


def main():
    board = "...........................ox......xo..........................."
    token_to_play = "x"
    moves = []
    alpha = "abcdefgh"

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
    else:
        token_to_play = "o"
        for i in range(100):
            if token_to_play == "o":
                token_to_play = "x"
            else:
                token_to_play = "o"
            playGame(quickMove, allPossibilities, makeMove, token_to_play)

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

    qm = quickMove(board, token_to_play)
    print(f'Best move: {qm[1][-1]}')
    print(f'Min score: {qm[0]}; move sequence: {qm[1]}')
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

if __name__ == '__main__': main()

# Johanna Lohmus p6 2023
