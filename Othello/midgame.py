import sys; args = sys.argv[1:]
# Johanna Lohmus

LIMIT_AB = 13
LIMIT_MIDAB = 4
import random, time

directions = [1, 11, 9, 10, -1, -11, -9, -10]
corners = [0, 7, 56, 63]
cornerdict = {0: [1, 8, 9], 7: [6, 14, 15], 56: {48, 49, 57}, 63: {54, 55, 62}}
topedges = [1, 2, 3, 4, 5, 6]
leftedges = [8, 16, 24, 32, 40, 48]
rightedges = [15, 23, 31, 39, 47, 55]
bottomedges = [57, 58, 59, 60, 61, 62]
edges = [1, 2, 3, 4, 5, 6, 8, 16, 24, 32, 40, 48, 15, 23, 31, 39, 47, 55, 57, 58, 59, 60, 61, 62]
lookup = {}

def makeMove(board, player, move):
    move = int(move)
    board = board.lower()

    new_board = board[:]
    new_board = new_board[:move] + player.upper() + new_board[move + 1:]

    if player == "x":
        opponent = "o"
    else:
        opponent = "x"

    border = "B" * 10
    for i in range(8):
        row = i * 8
        border += "B" + board[row:row + 8] + "B"
    border += "B" * 10

    const_move = ((move // 8) + 1) * 10 + ((move % 8) + 1)

    for direction in directions:
        if border[const_move + direction] != opponent: continue
        new_move = const_move
        flip = []
        while border[new_move + direction] == opponent:
            new_move = new_move + direction
            next = new_move + direction
            i = (new_move // 10 - 1) * 8 + (new_move % 10 - 1)
            flip.append(i)
        if border[next] == player and len(flip) > 0:
            for f in flip:
                new_board = new_board[:f] + player + new_board[f + 1:]

    new_board = new_board[:move] + player.upper() + new_board[move + 1:]
    return new_board

def printBoard(board, poss):
    board2d = ""
    for i in range(0, 64, 8):
        for j in range(i, i + 8):
            if j in poss: board2d += "*"
            else: board2d += board[j]
        board2d += "\n"
    print(board2d)

def allPossibilities(board, player):
    board = board.lower()
    allMoves = set()

    if (board, player) in lookup:
        return lookup[board, player]

    opponent = "xo"[player == "x"]

    border = "B" * 10
    for i in range(8):
        row = i * 8
        border += "B" + board[row:row + 8] + "B"
    border += "B" * 10

    for idx, token in enumerate(border):
        if token == player:
            for direction in directions:
                bracketed_tokens = 0
                current = idx
                if border[current + direction] != opponent: continue
                while border[current + direction] == opponent:
                    current = current + direction
                    next = current + direction
                    bracketed_tokens += 1
                if border[next] == "." and bracketed_tokens > 0:
                    row = (next) // 10 - 1
                    col = (next) % 10 - 1
                    i = row * 8 + col
                    allMoves.add(int(i))
                else: continue
    lookup[(board, player)] = allMoves
    return allMoves

def safeEdge(move, player, board):
    opponent = "xo"[player=="x"]

    if move in topedges:
        if opponent not in board[0:move] and '.' not in board[0:move] or opponent not in board[move+1:8] and '.' not in board[move+1:8]: return True
    if move in bottomedges:
        if opponent not in board[56:move] and '.' not in board[56:move] or opponent not in board[move+1:64] and '.' not in board[move+1:64]: return True
    if move in leftedges:
        tokens = [board[i] for i in range(0, 64, 8)]
        if opponent not in tokens[0:move//8] and '.' not in tokens[0:move//8] or opponent not in tokens[move//8:8] and '.' not in tokens[move//8:8]: return True
    if move in rightedges:
        tokens = [board[i] for i in range(7, 64, 8)]
        if opponent not in tokens[0:move//8] and '.' not in tokens[0:move//8] or opponent not in tokens[move//8:8] and '.' not in tokens[move//8:8]: return True

def scoring(board, player):
    board = board.lower()
    score = 0
    opponent = "xo"[player=="x"]

    pposs = allPossibilities(board, player)
    oposs = allPossibilities(board, opponent)

    pcount = board.count(player)
    ocount = board.count(opponent)

    if len(pposs) == 0:
        if len(oposs) == 0:
            if pcount > ocount:
                return 1000 + pcount - ocount
            if ocount > pcount:
                return -1000 + pcount - ocount
            else:
                return 0
        else: score = -200

    else: score += (len(pposs) - len(oposs)) * 10

    for corner in cornerdict:
        if board[corner] == player: score += 50
        if board[corner] == opponent: score -= 50
        for next_to_corner in cornerdict[corner]:
            if board[next_to_corner] == player:
                if board[corner] == player: score += 25
                else: score -= 25
            if board[next_to_corner] == opponent:
                if board[corner] == opponent: score -= 25
                else: score += 25

    for edge in edges:
        if safeEdge(edge, player, board): score += 10
        if safeEdge(edge, opponent, board): score -= 10
    return score

def alphabeta(board, player, lower_bound, upper_bound, depth):
    if player == "x":
        opponent = "o"
    else:
        opponent = "x"
    if depth == 0: return scoring(board, player), []
    moves = allPossibilities(board, player)
    if not moves:
        opp_moves = allPossibilities(board, opponent)
        if not opp_moves: return scoring(board, player), []
        score, move_path = alphabeta(board, opponent, -1 * upper_bound, -1 * lower_bound, depth - 1)
        move_path.append(-1)
        return (-1*score, move_path)
    best = (lower_bound - 1, [])
    for move in moves:
        new_board = makeMove(board, player, move).lower()
        score, move_path = alphabeta(new_board, opponent, -1 * upper_bound, -1 * lower_bound, depth - 1)
        move_path.append(move)
        score = -1 * score
        if score < lower_bound: continue
        if score > upper_bound: return (score, move_path)
        best = (score, move_path)
        lower_bound = score + 1
    return best

def quickMove(board, player):
    moves = [*allPossibilities(board, player)]
    min_possibilities = 64
    best_move = moves[0]
    cornermoves = []
    for move in moves:
        if move in corners: cornermoves.append(move)

        move_brd = makeMove(board, player, move)
        next_token = "o"
        if player == "o":
            next_token = "x"
        next_possibilities = allPossibilities(move_brd, next_token)

        if move in [1, 8, 9] and board[0] != player: continue
        if move in [6, 14, 15] and board[7] != player: continue
        if move in [48, 49, 57] and board[56] != player: continue
        if move in [62, 55, 54] and board[63] != player: continue

        if len(next_possibilities) < min_possibilities:
            min_possibilities = len(next_possibilities)
            best_move = move
    if cornermoves:
        best_move = random.choice(cornermoves)
    return best_move

def random_move(board, player):
    return random.choice([*allPossibilities(board, player)])

cache = {}
def terminal_alphabeta(board, player, lower_bound, upper_bound):
    if player == "x":
        opponent = "o"
    else:
        opponent = "x"

    moves = allPossibilities(board, player)

    if not moves:
        opp_moves = allPossibilities(board, opponent)
        if not opp_moves: return (board.count(player) - board.count(opponent), [])
        score, move_path = terminal_alphabeta(board, opponent, -1 * upper_bound, -1 * lower_bound)
        move_path.append(-1)
        return (-1*score, move_path)

    best = (lower_bound - 1, [])
    for move in moves:
        new_board = makeMove(board, player, move).lower()
        score, move_path = terminal_alphabeta(new_board, opponent, -1 * upper_bound, -1 * lower_bound)
        move_path.append(move)
        score = -1 * score
        if score < lower_bound: continue
        if score > upper_bound: return (score, move_path)
        best = (score, move_path)
        lower_bound = score + 1
    return best

def play_tournament(script):
    t = time.process_time()
    stats = []
    token = "x"
    for i in range(100):
        player = "x"
        board = "...........................ox......xo..........................."
        transcript = []
        while True:
            if not allPossibilities(board, player):
                player = "xo"[player == "x"]
                if not allPossibilities(board, player): break
                transcript.append(-1)
            if player != token:
                if script == terminal_alphabeta:
                    if board.count('.') < LIMIT_AB:
                        move = script(board, player, -64, 64)[1][-1]
                    else:
                        move = quickMove(board, player)
                else:
                    move = script(board, player)
                transcript.append(move)
                board = makeMove(board, player, move).lower()
            else:
                if board.count('.') < LIMIT_AB:
                    qm = alphabeta(board, player, -100000, 100000, LIMIT_AB)
                else:
                    qm = alphabeta(board, player, -100000, 100000, LIMIT_MIDAB)
                move = qm[1][-1]
                board = makeMove(board, player, move).lower()
                transcript.append(move)
            player = "xo"[player == "x"]
        player_tokens = board.count(token)
        enemy_tokens = 64 - player_tokens - board.count(".")
        score = player_tokens - enemy_tokens
        all_tokens = player_tokens + enemy_tokens
        string_transcript = ''.join([f"_{move}"[-2:] for move in transcript])
        stats.append((score, token, player_tokens, all_tokens, string_transcript))
        if i != 0 and i % 10 == 0:
            print()
        if len(str(score)) == 1:
            print(" " + str(score), end="  "),
        else:
            print(str(score), end="  "),
        token = "xo"[token == "x"]

    et = time.process_time()
    total_time = et - t
    total_player_tokens = 0
    total_tokens = 0
    for game in stats:
        total_player_tokens += game[2]
        total_tokens += game[3]

    worst_game = min(stats)
    game_num = stats.index(worst_game) + 1
    stats.remove(worst_game)
    second_worst_game = min(stats)
    game_num_2 = stats.index(second_worst_game) + 2

    print()
    print(f'My tokens: {total_player_tokens}; Total tokens: {total_tokens}')
    print(f'Score: {str(float((total_player_tokens / total_tokens) * 100))[:4]}%')
    print(f'NM/AB LIMIT: {LIMIT_AB}')
    print(f'Game {game_num} as {worst_game[1]} => {worst_game[0]}:')
    print(worst_game[4])
    print(f'Game {game_num_2} as {second_worst_game[1]} => {second_worst_game[0]}:')
    print(second_worst_game[4])
    print(f'Elapsed time: {str(total_time)[:4]}s')

def main():
    board = "...........................ox......xo..........................."
    player = "x"
    moves = []
    alpha = "abcdefgh"
    hasToken = False

    if args:
        for arg in args:
            if arg in "xXoO":
                hasToken = True
                player = arg.lower()
            elif len(arg) == 64 and "x" in arg:
                board = arg.lower()
            elif len(arg) > 2:
                condensed = [arg[i:i+2] for i in range(0, len(arg), 2)]
                for m in condensed:
                    if m[0] == "_":
                        moves.append(int(m[1]))
                    elif int(m) >= 0:
                        moves.append(int(m))
            else:
                if arg[0].isalpha():
                    arg = arg.lower()
                    num = (int(arg[1]) - 1) * 8 + alpha.index(arg[0])
                    moves.append(int(num))
                elif int(arg) >= 0:
                    moves.append(int(arg))
        if hasToken == False:
            if not allPossibilities(board, "x"):
                player = "o"
            elif not allPossibilities(board, "o"):
                player = "x"
            elif board.count("o") < board.count("x"):
                player = "o"

        poss_moves = allPossibilities(board, player)
        if moves and moves[0] not in poss_moves:
            player = "xo"[player == "x"]
        poss_moves = allPossibilities(board, player)
        string_moves = ", ".join(str(move) for move in poss_moves)
        printBoard(board, poss_moves)
        print(f'{board} {board.count("x")}/{board.count("o")}')
        print(f'Possible moves for {player}: {string_moves}')

        for move in moves:
            poss_moves = allPossibilities(board, player)
            if move not in poss_moves:
                player = "xo"[player == "x"]
            board = makeMove(board, player, move)
            print(f'{player} moves to {move}')

            player = "xo"[player == "x"]

            poss_moves = allPossibilities(board, player)
            if not poss_moves:
                player = "xo"[player == "x"]
                poss_moves = allPossibilities(board, player)
            string_moves = ", ".join(str(move) for move in poss_moves)

            printBoard(board, poss_moves)
            print(f'{board} {board.lower().count("x")}/{board.lower().count("o")}')

            print(f'Possible moves for {player}: {string_moves}')

        if board.count(".") == 0 or not allPossibilities(board, player) and not allPossibilities(board, "xo"[player == "x"]):
            print()
        elif board.count(".") < LIMIT_AB:
            qm = alphabeta(board, player, -100000, 100000, LIMIT_AB)
            print(f'Best move: {qm[1][-1]}')
            print(f'Min score: {qm[0]}; move sequence: {qm[1]}')
        else:
            qm = alphabeta(board, player, -100000, 100000, LIMIT_MIDAB)
            print(qm[1])
            print(f'Best move: {qm[1][-1]}')
            print(f'Min score: {qm[0]}; move sequence: {qm[1]}')

    else:
        play_tournament(random_move)
        play_tournament(quickMove)
        play_tournament(terminal_alphabeta)

if __name__ == '__main__': main()

# Johanna Lohmus 6 2023
