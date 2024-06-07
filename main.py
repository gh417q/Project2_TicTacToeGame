X = 'X'
O = 'O'
rows = {'1': 0, '2': 3, '3': 6}
cols = {'a': 0, 'b': 1, 'c': 2}
last_moves = {0: "a1", 1: "b1", 2: "c1", 3: "a2", 4: "b2", 5: "c2", 6: "a3", 7: "b3", 8: "c3"}

moves = {' O OX    ': 6, ' O  XO   ': 8, '   OX  O ': 0, '    XO O ': 2,  # player starts
         '   OXO   ': 0, ' O  X  O ': 0,
         'O  XXOO  ': 1, '  OOXX  O': 1, 'OXO X  O ': 3, ' O  X OXO': 3,
         'O   X   O': 3, '  O X O  ': 3,
         'O   X  O ': 3, '  O X  O ': 5, ' O  X O  ': 3, ' O  X   O': 5,
         '  OOX    ': 1, '   OX   O': 7, 'O   XO   ': 1, '    XOO  ': 7,
         'O  XXO O ': 2, '  OOXX O ': 0, ' O XXOO  ': 8, ' O OXX  O': 6,
         'OX  XO O ': 6, ' XOOX O  ': 8, ' O  XOOX ': 0, ' O OX  XO': 2,
         'O   X    ': 6, '  O X    ': 0, '    X O  ': 0, '    X   O': 6,  # computer starts
         ' O  X    ': 0, '   OX    ': 0, '    XO   ': 0, '    X  O ': 0,
         'XO  X   O': 6, 'X  OX   O': 2, 'X   XO  O': 2, 'X   X  OO': 6
}

board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

first_move = False  # True


def print_board():
    print("  a   b   c")
    for k in range(3):
        print(f"{k + 1} {board[k * 3]} | {board[k * 3 + 1]} | {board[k * 3 + 2]}")
        if k < 2:
            print("  ---------")


# Prints error message and returns False if the move is not valid.
# Updates the board and returns True otherwise.
def process_move(move: str) -> bool:
    global board
    if len(move) != 2:
        print(f"'{move}' is incorrect, must be c1, 2b, a3, ...")
        return False
    if move[0].isalpha():
        if not move[1].isnumeric():
            print(f"'{move}' is incorrect, must be letter and number (in any order)")
            return False
        if not move[0] in ['a', 'b', 'c']:
            print(f"'{move}' is incorrect, the letter must be 'a', 'b', or 'c'")
            return False
        if not move[1] in ['1', '2', '3']:
            print(f"'{move}' is incorrect, number must be 1, 2, or 3")
            return False
        if board[rows[move[1]] + cols[move[0]]] != ' ':
            print(f"Cell '{move}' is not empty.")
            return False
        board[rows[move[1]] + cols[move[0]]] = O
        return True
    if move[0].isnumeric():
        if not move[1].isalpha():
            print(f"'{move}' is incorrect, must be number and letter (in any order)")
            return False
        if not move[0] in ['1', '2', '3']:
            print(f"'{move}' is incorrect, number must be 1, 2, or 3")
            return False
        if not move[1] in ['a', 'b', 'c']:
            print(f"'{move}' is incorrect, the letter must be 'a', 'b', or 'c'")
            return False
        if board[rows[move[0]] + cols[move[1]]] != ' ':
            print(f"Cell '{move}' is not empty.")
            return False
        board[rows[move[0]] + cols[move[1]]] = O
        return True
    print(f"'{move}' is incorrect, must be number and letter (in any order)")
    return False

def check_board(player: str) -> int:
    for k in range(9):
        row_k = k//3*3
        if board[k] == ' ' and board[row_k: row_k + 3].count(player) == 2:
            return k
    for k in range(3):
        col = [board[m] for m in [k, k + 3, k + 6]]
        for j in range(len(col)):
            if col[j] == ' ' and col.count(player) == 2:
                # print(f"K,J:{k}, {j}")
                return k + j*3
    diag = [board[m] for m in [0, 4, 8]]
    for j in range(len(diag)):
        if diag[j] == ' ' and diag.count(player) == 2:
            return j*4
    diag = [board[m] for m in [2, 4, 6]]
    for j in range(len(diag)):
        if diag[j] == ' ' and diag.count(player) == 2:
            return (j + 1)*2
    return -1


def make_move() -> bool:
    global board
    winning_index = check_board(X)
    # print(f"W:{winning_index}")
    if winning_index != -1:
        board[winning_index] = X
        return True
    losing_index = check_board(O)
    # print(f"L:{losing_index}")
    if losing_index != -1:
        board[losing_index] = X
        return False
    if board[4] == ' ':  # on first answer, unless already taken
        board[4] = X
        return False
    board_line = ''.join(board)
    if board_line == '    O    ':  # otherwise, take the corner
        board[0] = X
        return False
    if board_line == 'X   O   O':  # the only second move with no need to defend
        board[2] = X
        return False
    if board.count(' ') == 2:  # almost over, and neither winning is possible, nore defence is needed
        board[board.index(' ')] = X  # take any of the two
        return False
    board[moves[board_line]] = X
    return False

def play_the_game():
    print_board()
    while True:
        if not first_move and board.count(' ') == 1:  # player started, and now it's the last move
            ind_last = board.index(' ')
            input(f"Last move, please press Enter to fill '{last_moves[ind_last]}'!")
            board[ind_last] = O
            print_board()
            print("It's a draw!")
            return
        move = input("Your move, please enter coordinates of the cell.").lower()
        while not process_move(move):
            move = input("Please try again. Enter coordinates of the cell.").lower()
        print_board()
        if board.count(' ') == 0:
            print("It's a draw!")
            return
        game_over = make_move()
        print_board()
        if game_over:
            print("Computer wins, game over!")
            return
        if board.count(' ') == 0:
            print("It's a draw!")
            return


while True:
    moves_first = "you move"
    if first_move:
        moves_first = "computer moves"
        board[4] = X
    print(f"Playing tic Tac Toe - {moves_first} first.")
    proceed = input(f"Please press Enter to proceed, or type any character and hit Enter to end the game.")
    if proceed != '':
        break
    play_the_game()
    print("============================================")
    board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    first_move = not first_move
