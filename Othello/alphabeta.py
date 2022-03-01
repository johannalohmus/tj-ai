import sys; args = sys.argv[1:]
# Johanna Lohmus
LIMIT_AB = 1

import random, time

directions = [1, 11, 9, 10, -1, -11, -9, -10]
corners = [0, 7, 56, 63]
lookup = {}
lookup_move = {}
best_moves = {}

def makeMove(board, token_to_play, move):
    move = int(move)
    board = board.lower()
    #if (board, token_to_play, move) in lookup_move:
    #    return lookup_move[(board, token_to_play, move)]
    new_board = board[:]
    new_board = new_board[:move] + token_to_play.upper() + new_board[move + 1:]

    if token_to_play == "x":
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
        if border[const_move + direction] != opponent:
            continue
        new_move = const_move
        flip = []
        while border[new_move + direction] == opponent:
            new_move = new_move + direction
            next = new_move + direction
            i = (new_move // 10 - 1) * 8 + (new_move % 10 - 1)
            flip.append(i)
        if border[next] == token_to_play and len(flip) > 0:
            for f in flip:
                new_board = new_board[:f] + token_to_play + new_board[f + 1:]

    new_board = new_board[:move] + token_to_play.upper() + new_board[move + 1:]
    #lookup_move[(board, token_to_play, move)] = new_board
    return new_board

def printBoard(board, poss):
    board2d = ""
    for i in range(0, 64, 8):
        for j in range(i, i + 8):
            if j in poss:
                board2d += "*"
            else:
                board2d += board[j]
        board2d += "\n"
    print(board2d)

def allPossibilities(board, token_to_play):
    board = board.lower()
    allMoves = set()

    if (board, token_to_play) in lookup:
        return lookup[board, token_to_play]

    opponent = "xo"[token_to_play == "x"]

    border = "B" * 10
    for i in range(8):
        row = i * 8
        border += "B" + board[row:row + 8] + "B"
    border += "B" * 10

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
    lookup[(board, token_to_play)] = allMoves
    return allMoves

def alphabeta(board, token_to_play, lower_bound, upper_bound):
    if token_to_play == "x":
        opponent = "o"
    else:
        opponent = "x"

    moves = allPossibilities(board, token_to_play)

    if not moves:
        opp_moves = allPossibilities(board, opponent)
        if not opp_moves:
            return (board.count(token_to_play) - board.count(opponent), [])
        score, move_path = alphabeta(board, opponent, -1 * upper_bound, -1 * lower_bound)
        move_path.append(-1)
        return (-1*score, move_path)

    best = (lower_bound - 1, [])
    for move in moves:
        new_board = makeMove(board, token_to_play, move).lower()
        score, move_path = alphabeta(new_board, opponent, -1 * upper_bound, -1 * lower_bound)
        move_path.append(move)
        score = -1 * score
        if score < lower_bound:
            continue
        if score > upper_bound:
            return (score, move_path)
        best = (score, move_path)
        lower_bound = score + 1
    return best

def quickMove(board, token_to_play):
    #if (board, token_to_play) in best_moves:
  #      return best_moves[(board, token_to_play)]
    moves = [*allPossibilities(board, token_to_play)]
    best_move = moves[0]
    min_possibilities = 64
    for move in moves:
        if move in corners:
            return move

        move_brd = makeMove(board, token_to_play, move)
        next_token = "o"
        if token_to_play == "o":
            next_token = "x"
        next_possibilities = allPossibilities(move_brd, next_token)

        if move in [1, 8, 9] and board[0] != token_to_play:
            continue
        if move in [6, 14, 15] and board[7] != token_to_play:
            continue
        if move in [48, 49, 57] and board[56] != token_to_play:
            continue
        if move in [62, 55, 54] and board[63] != token_to_play:
            continue

        if len(next_possibilities) < min_possibilities:
            min_possibilities = len(next_possibilities)
            best_move = move
    #best_moves[(board, token_to_play)] = best_move
    return best_move

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
                token_to_play = "o"
            elif not allPossibilities(board, "o"):
                token_to_play = "x"
            elif board.count("o") < board.count("x"):
                token_to_play = "o"

        poss_moves = allPossibilities(board, token_to_play)
        if moves and moves[0] not in poss_moves:
            token_to_play = "xo"[token_to_play == "x"]
        poss_moves = allPossibilities(board, token_to_play)
        string_moves = ", ".join(str(move) for move in poss_moves)
        printBoard(board, poss_moves)
        print(f'{board} {board.count("x")}/{board.count("o")}')
        print(f'Possible moves for {token_to_play}: {string_moves}')

        for move in moves:
            poss_moves = allPossibilities(board, token_to_play)
            if move not in poss_moves:
                token_to_play = "xo"[token_to_play == "x"]
            board = makeMove(board, token_to_play, move)
            print(f'{token_to_play} moves to {move}')

            token_to_play = "xo"[token_to_play == "x"]

            poss_moves = allPossibilities(board, token_to_play)
            if not poss_moves:
                token_to_play = "xo"[token_to_play == "x"]
                poss_moves = allPossibilities(board, token_to_play)
            string_moves = ", ".join(str(move) for move in poss_moves)

            printBoard(board, poss_moves)
            print(f'{board} {board.lower().count("x")}/{board.lower().count("o")}')

            print(f'Possible moves for {token_to_play}: {string_moves}')

        if board.count(".") == 0:
            print()

        elif board.count(".") < LIMIT_AB:
            qm = alphabeta(board, token_to_play, -64, 64)
            print(f'Best move: {qm[1][-1]}')
            print(f'Min score: {qm[0]}; move sequence: {qm[1]}')
        else:
            qm = quickMove(board, token_to_play)
            print(f'Best move: {qm}')

    else:
        t = time.process_time()
        stats = []
        token = "x"
        for i in range(100):
            token_to_play = "x"
            board = "...........................ox......xo..........................."
            transcript = []
            while True:
                if not allPossibilities(board, token_to_play):
                    token_to_play = "xo"[token_to_play == "x"]
                    if not allPossibilities(board, token_to_play):
                        break
                    transcript.append(-1)
                if token_to_play != token:
                    moves = allPossibilities(board, token_to_play)
                    move = random.choice([*moves])
                    transcript.append(move)
                    board = makeMove(board, token_to_play, move).lower()
                else:
                    if board.count(".") < LIMIT_AB:
                        qm = alphabeta(board, token_to_play, -64, 64)
                        move = qm[1][-1]
                    else:
                        move = quickMove(board, token_to_play)
                    board = makeMove(board, token_to_play, move).lower()
                    transcript.append(move)
                token_to_play = "xo"[token_to_play == "x"]
            player_tokens = board.count(token)
            enemy_tokens = 64 - player_tokens - board.count(".")
            score = player_tokens - enemy_tokens
            all_tokens = player_tokens + enemy_tokens
            string_transcript = ''.join([f"_{move}"[-2:] for move in transcript])
            stats.append((score, token, player_tokens, all_tokens, string_transcript))
            if i != 0 and i % 10 == 0:
                print()
            if len(str(score)) == 1:
                print(" " + str(score), end = "  "),
            else:
                print(str(score), end = "  "),


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
        game_num_2 = stats.index(second_worst_game) + 1

        print()
        print(f'My tokens: {total_player_tokens}; Total tokens: {total_tokens}')
        print(f'Score: {str(float((total_player_tokens/total_tokens)*100))[:4]}%')
        print(f'NM/AB LIMIT: {LIMIT_AB}')
        print(f'Game {game_num} as {worst_game[1]} => {worst_game[0]}:')
        print(worst_game[4])
        print(f'Game {game_num_2} as {second_worst_game[1]} => {second_worst_game[0]}:')
        print(second_worst_game[4])
        print(f'Elapsed time: {str(total_time)[:4]}s')

if __name__ == '__main__': main()

# Johanna Lohmus p6 2023
