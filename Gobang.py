import sys
import pdb
import random
import copy

# Defaults
DARK = 1
LIGHT = 2
human_is_dark = True
board_size = 11
depth = 2
board_winner = -1
scoring_combos = dict()
open_board_spots = set()
new_board_winner = None
is_human_turn = None
game_winning_color = None
human_player = {}
com_player = {}
WINNING_SCORE = 2000000

# detects if there is 5 in a row for a given color.
def detect_5(board, col):
    global game_winning_color
    is_win = False

    if len(open_board_spots) == 0:
        is_win = True
        game_winning_color = -1
        return is_win

    for a in range(len(board)-4):
        for b in range(len(board)):
            count = 0
            if board[a][b] == col:
                for vertical in range (1, 5):
                    if board[a + vertical][b] == col:
                        count += 1
                if count == 4:
                    if a != 0 and a != len(board)-5:
                       if board[a-1][b] != col and board[a+5][b] != col:
                           is_win = True
                    if a == 0:
                        if board[a+5][b] != col:
                            is_win = True
                    if a == len(board)-5:
                        if board[a-1][b] != col:
                            is_win = True

    for c in range(len(board)):
        for d in range(len(board)-4):
            count = 0
            if board[c][d] == col:
                for horizontal in range (1,5):
                    if board[c][d + horizontal] == col:
                        count += 1
                if count == 4:
                    if d != 0 and d != len(board)-5:
                       if board[c][d-1] != col and board[c][d+5] != col:
                           is_win = True
                    if d == 0:
                        if board[c][d+5] != col:
                            is_win = True
                    if d == len(board)-5:
                        if board[c][d-1] != col:
                            is_win = True
    for e in range(len(board)-4):
        for f in range(4, len(board)):
            count = 0
            if board[e][f] == col:
                for diagonal2 in range (1, 5):
                    if board [e + diagonal2][f - diagonal2] == col:
                        count+= 1
                if count == 4:
                    if e in range (1, len(board)-5) and f in range (5,len(board)-1):
                        if board[e-1][f+1] != col and board[e+5][f-5] != col:
                           is_win = True
                    if e == 0 or f == len(board)-1:
                        if (e+5 >= len(board)) or (f-5 >= len(board)):
                            is_win = True
                        if board[e+5][f-5] != col:
                            is_win = True
                    if e == len(board)-5 or f == 4:
                        if board[e-1][f+1] != col:
                            is_win = True
    for y in range(len(board)-4):
        for x in range(len(board)-4):
            count = 0
            if board[y][x] == col:
                for diagonal1 in range (1, 5):
                    if board [y + diagonal1][x + diagonal1] == col:
                        count += 1
                if count == 4:
                    if y in range (1, len(board)-5) and x in range (1,len(board)-5):
                        if board[y-1][x-1] != col and board[e+5][f+5] != col:
                           is_win = True
                    if y == 0 or x == 0:
                        if (y+5 >= len(board)) or (x+5 >= len(board)):
                            is_win = True
                        if board[y+5][x+5] != col:
                            is_win = True
                    if y == len(board)-5 or x == len(board)-5:
                        if board[y-1][x-1] != col:
                            is_win = True


    if is_win:
        game_winning_color = col

    return is_win

def parse_input_args():
    global board_size
    global depth
    global human_is_dark

    for index, arg in enumerate(sys.argv):
        if arg == "-l":
            human_is_dark = False
        if arg == "-n":
            board_size = int(sys.argv[index + 1])
        if arg == "-d":
            depth = int(sys.argv[index + 1])

    if (board_size < 5) or (board_size > 26):
        print "ERROR: Board size must be between 4 and 26"
        print "Curr erroneous board size:", board_size
        exit(0)

    if(depth < 0):
        print "ERROR: depth must be 0 or greater"
        exit(0)

    print "Board size:", board_size, ", depth:", depth, "human is dark:", human_is_dark

def print_board(board):
    global board_size

    # Print letters on top
    for index in range(board_size):
        curr_char = chr(index + 97)
        letters_str = "   " + curr_char
        sys.stdout.write(letters_str)
    sys.stdout.write("\n   +")

    for index in range(board_size):
        sys.stdout.write("---+")

    sys.stdout.write("\n")

    for i in range(board_size):
        curr_row_num = str(i + 1) + "  |"
        if i >= 9:
            curr_row_num = str(i + 1) + " |"
        elif i == 10:
            curr_row_num = str(i + 1) + "|"

        sys.stdout.write(curr_row_num)
        for j in range(board_size):
            if board[i][j] == DARK:
                sys.stdout.write(" D |")
            elif board[i][j] == LIGHT:
                sys.stdout.write(" L |")
            else:
                sys.stdout.write("   |")
        # sys.stdout.write("   |")
        sys.stdout.write("\n   +")
        for index in range(board_size):
            sys.stdout.write("---+")
        print
def print_metadata(last_move, player_name):
    print "Moved played: ", last_move
    next_player = "human" if player_name == "COM" else "COM"
    # next_player = player_name == "COM" ? "human" : "COM"
    print "Next move to be done by", next_player

def update_scoring_dict():
    global scoring_combos
    scoring_combos["AAXAA"] = 100000
    scoring_combos["XAAAAX"] = 100000
    scoring_combos["XXAAAXX"] = 100000
    scoring_combos["XXXAA"] = 100
    scoring_combos["AAXXX"] = 100
    scoring_combos["XAXXAX"] = 200
    scoring_combos["AAAXX"] = 400
    scoring_combos["AXXAA"] = 550
    scoring_combos["XXXAAXXX"] = 600
    scoring_combos["XAAXAX"] = 700
    scoring_combos["XAAAA"] = 1500
    scoring_combos["AXAAA"] = 2000

def game_over(board):
    global board_winner
    global open_board_spots
    global new_board_winner

    board_winner = new_board_winner
    if board_winner == -1 or len(open_board_spots) != 0:
        return False
    else:
        return True

def get_human_move():
    global board_size
    global is_human_turn

    correct_input = False

    print "Human turn:"

    while not correct_input:
        correct_input = True
        move = raw_input("> ")

        # If move is less than 2 char, retry
        if(len(move) < 2):
            print "ERROR: wrong input size for move. Usage: <letter><number>"
            correct_input = False
            continue

        # Convert to rows and cols for the board
        col = move[0]
        row = int(move[1:]) - 1
        col = (ord(col) - 97)
        # Error checking if out of bounds of board
        if(col < 0 or (col + 1) > board_size):
            print "ERROR: move entered is out of bounds of selected game size. Please retry."
            correct_input = False

        if(row < 0 or (row + 1) > board_size):
            print "ERROR: move entered is out of bounds of selected game size. Please retry."
            correct_input = False

    return row, col

def eval_status(row, col, color, board):
    global board_size
    global new_board_winner
    best = 1
    diff = 0

    # Check right side of temp placement
    c1 = 0
    i = col
    while i < board_size:
        if board[row][i] != color:
            break
        c1 += 1
        i += 1

    # Check left side of temp placement
    c2 = 0
    i = col
    while i >= 0:
        if board[row][i] != color:
            break
        c2 += 1
        i = i - 1

    # calculate
    if((c1 + c2 - 1) >= 5):
        new_board_winner = color
        # print "NEW BOARD WINNER FOUND"
        return

    best = max(best, c1 + c2 - 1)

    # Check below
    c1 = 0
    i = row
    while i < board_size:
        if board[i][col] != color:
            break
        c1 += 1
        i += 1

    # Check above
    c2 = 0
    i = row
    while i >= 0:
        if board[i][col] != color:
            break
        c2 += 1
        i = i - 1

    # calculate
    if((c1 + c2 - 1) >= 5):
        new_board_winner = color
        # print "NEW BOARD WINNER FOUND"
        return

    best = max(best, c1 + c2 - 1)

    # Check bottom right diagonal
    c1 = 0
    i = row
    j = col
    while i < board_size and j < board_size:
        if board[i][j] != color:
            break
        c1 += 1
        j += 1
        i += 1

    # Check up left diagonally
    c2 = 0
    i = row
    j = col
    while i >= 0 and j >= 0:
        if board[i][j] != color:
            break
        c2 += 1
        i = i - 1
        j = j - 1

    # calculate
    if((c1 + c2 - 1) >= 5):
        new_board_winner = color
        # print "NEW BOARD WINNER FOUND"
        return

    best = max(best, c1 + c2 - 1)

    # Check right up diagonally
    c1 = 0
    i = row
    j = col
    while i >= 0 and j < board_size:
        if board[i][j] == color:
            break
        c1 += 1
        i = i - 1
        j += 1

    # Check left down diagonally
    c2 = 0
    i = row
    j = col
    while i < board_size and j >= 0:
        if board[i][j] != color:
            break
        c2 += 1
        i += 1
        j = j - 1

    # calculate
    if((c1 + c2 - 1) >= 5):
        new_board_winner = color
        # print "NEW BOARD WINNER FOUND"
        return

    best = max(best, c1 + c2 - 1)

def calc_score(curr_str):
    global scoring_combos
    score = 0
    for key in scoring_combos:
        if key in curr_str:
            score += scoring_combos[key]

    return score

def plyr_score_update(board, row, col, player):
    global board_size
    color = player['color']
    # Score in that row (going right)
    curr_str = ""
    for j in range(board_size):
        if board[row][j] == 0:
            curr_str += 'X'
        elif board[row][j] == color:
            curr_str += 'A'
        else:
            curr_str += 'B'

    score = calc_score(curr_str)
    player['score'] += score - player['rows'][row]
    player['rows'][row] = score

    # Score in that col (going down)
    curr_str = ""
    for i in range(board_size):
        if board[i][col] == 0:
            curr_str += 'X'
        elif board[i][col] == color:
            curr_str += 'A'
        else:
            curr_str += 'B'

    score = calc_score(curr_str)
    player['score'] += score - player['cols'][col]
    player['cols'][col] = score
    r_c_sum = row + col
    curr_str = ""
    start = (board_size - 1) if r_c_sum >= (board_size - 1) else r_c_sum
    while start >= 0:
        if ((r_c_sum - start < 0) or (r_c_sum - start >= board_size)):
            break
        if board[start][r_c_sum - start] == 0:
            curr_str += 'X'
        elif board[start][r_c_sum - start] == color:
            curr_str += 'A'
        else:
            curr_str += 'B'
        start = start - 1

    score = calc_score(curr_str)
    player['score'] += score - player['rdiags'][r_c_sum]
    player['rdiags'][r_c_sum] = score
    diff = col - row
    curr_str = ""
    start = diff if diff >= 0 else 0
    while start < board_size:
        if ((start - diff < 0) or (start - diff >= board_size)):
            break
        if board[start - diff][start] == 0:
            curr_str += 'X'
        elif board[start - diff][start] == color:
            curr_str += 'A'
        else:
            curr_str += 'B'
        start = start - 1

    score = calc_score(curr_str)
    player['score'] += score - player['ldiags'][board_size + diff - 1]
    player['ldiags'][board_size + diff - 1] = score
    x = 5

def minimax_move(com_player, human_player, my_move, board, alpha, beta, row, col, open_board_spots):
    global depth
    global board_size
    global new_board_winner

    # Base case
    if depth == 0:
        return [human_player['score'] - com_player['score'], -1]

    depth = depth - 1

    # Create new temp board
    new_board = copy.deepcopy(board)
    minimax_open_spots = copy.deepcopy(open_board_spots)

    # human is player 1
    new_player_one = copy.deepcopy(human_player)
    # com is player 2
    new_player_two = copy.deepcopy(com_player)
    # pdb.set_trace()
    # Update new board
    if not my_move:
        new_board[row][col] = human_player['color']
        minimax_open_spots.remove(row * board_size + col)
        eval_status(row, col, human_player['color'], new_board)
        if new_board_winner == human_player['color']:
            return [-WINNING_SCORE, depth]
    else:
        new_board[row][col] = com_player['color']
        minimax_open_spots.remove(row * board_size + col)
        eval_status(row, col, com_player['color'], new_board)
        if new_board_winner == com_player['color']:
            return [WINNING_SCORE, depth]

    # Update scores for both players
    plyr_score_update(new_board, row, col, new_player_one)
    plyr_score_update(new_board, row, col, new_player_two)

    if len(minimax_open_spots) == 0:
        return [new_player_one['score'] - new_player_two['score'], -1]

    my_move = not my_move

    valid_moves = copy.deepcopy(minimax_open_spots)
    # pdb.set_trace()
    best_score_diff = []
    # pdb.set_trace()

    best_score_diff.append((WINNING_SCORE + 1) if not my_move else (-WINNING_SCORE - 1))
    best_score_diff.append(-1)
    i = 0
    for m in valid_moves:
        i += 1
        new_move = m
        new_move_row = new_move / board_size
        new_move_col = new_move % board_size
        new_score_diff = minimax_move(new_player_one, new_player_two, my_move, new_board, alpha, beta, new_move_row, new_move_col, minimax_open_spots)
        if my_move:
            if best_score_diff[0] == new_score_diff [0]:
                if best_score_diff[1] < new_score_diff[1]:
                    best_score_diff[1] = new_score_diff[1]
            elif best_score_diff[0] < new_score_diff[0]:
                best_score_diff[0] = new_score_diff[0]
                best_score_diff[1] = new_score_diff[1]
        elif best_score_diff[0] == new_score_diff[0]:
            if best_score_diff[1] > new_score_diff[1]:
                best_score_diff[1] = new_score_diff[1]
        elif best_score_diff[0] > new_score_diff[0]:
            best_score_diff[0] = new_score_diff[0]
            best_score_diff[1] = new_score_diff[1]

    return best_score_diff

def get_comp_move(board, human_player, com_player, is_dark_move):
    global open_board_spots
    global human_is_dark
    global board_size
    print "COM is calculating its next move, please wait up to 30 seconds"
    if (len(open_board_spots) == 0):
        return None, None

    # Calculating best move for computer
    best_score = -WINNING_SCORE - 1
    best_possible_moves = set()
    best_win_depth = -1
    # Explore each possible candidate for next move
    for m in open_board_spots:
        alpha = best_score
        beta = -best_score
        res = None
        move = m
        move_row = move / board_size
        move_col = move % board_size
        if is_dark_move:
            res = minimax_move(human_player, com_player, True, board, alpha, beta, move_row, move_col, open_board_spots)
        else:
            res = minimax_move(com_player, human_player, True, board, alpha, beta, move_row, move_col, open_board_spots)

        new_score = res[0]
        new_win_depth = res[1]

        if new_score == best_score:
            if new_win_depth > best_win_depth:
                best_possible_moves = set()
                best_possible_moves.add(int(move))
                best_win_depth = new_win_depth
            elif new_win_depth == best_win_depth:
                best_possible_moves.add(int(move))
        elif new_score > best_score:
            best_score = new_score
            best_possible_moves = set()
            best_possible_moves.add(int(move))
            best_win_depth = new_win_depth


    best_move = None
    rand_i = random.randint(0, len(best_possible_moves))

    for index, m in enumerate(best_possible_moves):
        move = m
        if index == rand_i:
            best_move = m

    if not best_move:
        best_move = random.sample(best_possible_moves, 1)
        best_move = best_move[0]
    best_move_row = best_move / board_size
    best_move_col = best_move % board_size
    return best_move_row, best_move_col


def create_new_player(player, is_human):
    global board_size

    player['rows'] = []
    player['cols'] = []
    player['ldiags'] = []
    player['rdiags'] = []

    for x in range(board_size):
        player['rows'].append(0)

    for x in range(board_size):
        player['cols'].append(0)

    for x in range(board_size * 2 - 1):
        player['ldiags'].append(0)

    for x in range(board_size * 2 - 1):
        player['rdiags'].append(0)

    player['color'] = DARK if is_human and human_is_dark else LIGHT
    player['score'] = 0
    player['last_move_row'] = -1
    player['last_move_col'] = -1

def make_move(board, row, col, color, player):
    global open_board_spots
    global board_size


    ####################### UPDATE BOARD: ###########################
    # pdb.set_trace()
    x = 5
    y = 10
    # update board mark
    board[row][col] = color


    x = 5
    y = 10
    # pdb.set_trace()
    # remove candidate squares
    if (row * board_size + col) in open_board_spots:
        open_board_spots.remove((row * board_size + col))
    # update game status
    eval_status(row, col, color, board)
    # update score for player
    plyr_score_update(board, row, col, player)

    player['last_move_row'] = row
    player['last_move_col'] = col



def main():
    global human_is_dark
    global open_board_spots
    global human_player
    global com_player
    global is_human_turn
    global is_black_turn

    parse_input_args()
    width = board_size
    height = board_size

    # Create board and board candidates
    board = [[0 for x in range(width)] for y in range(height)]

    create_new_player(human_player, True)
    create_new_player(com_player, False)


    for x in range(board_size*board_size):
        open_board_spots.add(x)


    print_board(board)
    print_metadata("--", "COM")
    update_scoring_dict()
    is_black_turn = True
    is_human_turn = True if is_black_turn and human_is_dark else False

    # Play game here
    while not detect_5(board, com_player['color']) and not detect_5(board, human_player['color']):
        row = None
        col = None
        current_player = human_player if is_human_turn else com_player

        row, col = get_human_move() if is_human_turn else get_comp_move(board, human_player, com_player, is_black_turn)
        if current_player == human_player:
            make_move(board, row, col, current_player['color'], human_player)
        else:
            make_move(board, row, col, current_player['color'], com_player)

        print
        print_board(board)
        last_row = row + 1
        last_col = chr(col + 97)
        last_move = str(str(last_col) + str(last_row))
        print "Last move played:", last_move


        # Switch states for turns
        is_black_turn = not is_black_turn
        is_human_turn = not is_human_turn




    # Game over
    print "Game Over!"
    if game_winning_color == DARK:
        print "WINNER: DARK"
    else:
        print "WINNER: LIGHT"


if __name__ == '__main__':
    main()
