ROWS = 8
COLS = 8

def get_single_moves(board, color, row, col):
    moves = []
    directions = [(1, -1), (1, 1)] if color == "B" else [(-1, -1), (-1, 1)]

    for direction in directions:
        new_row, new_col = row + direction[0], col + direction[1]
        if 0 <= new_row < ROWS and 0 <= new_col < COLS and board[new_row][new_col] == "":
            moves.append((str(row) + str(col), str(new_row)+str(new_col)))

    return moves

def get_single_jumps(board, color, row, col):
    jumps = []
    directions = [(1, -1), (1, 1)] if color == "B" else [(-1, -1), (-1, 1)]

    for direction in directions:
        new_row, new_col = row + direction[0], col + direction[1]

        if (
            0 <= new_row < ROWS
            and 0 <= new_col < COLS
            and board[new_row][new_col]
            and board[new_row][new_col][0] == "X"
        ):
            jump_row, jump_col = row + 2 * direction[0], col + 2 * direction[1]
            if (
                0 <= jump_row < ROWS
                and 0 <= jump_col < COLS
                and board[jump_row][jump_col] == ""
            ):
                jumps.append((row, col, jump_row, jump_col))

    return jumps


def get_double_jumps(board, color, row, col):
    double_jumps = []
    single_jumps = get_single_jumps(board, color, row, col)

    for move in single_jumps:
        new_row, new_col, jump_row, jump_col = move
        temp_board = [row[:] for row in board]
        temp_board[jump_row][jump_col] = temp_board[row][col]
        temp_board[row][col] = "X"
        temp_board[new_row][new_col] = "X"

        next_jumps = get_single_jumps(temp_board, color, jump_row, jump_col)
        if next_jumps:
            for next_jump in next_jumps:
                double_jumps.append(move + next_jump[2:])

    return double_jumps



def get_moves_for_color(board, color):
    moves = []
    for row in range(ROWS):
        for col in range(COLS):
            current_piece = board[row][col]
            if len(current_piece) == 4 and current_piece[0] == color:
                moves.extend(get_single_moves(board, color, row, col))
                moves.extend(get_single_jumps(board, color, row, col))
                moves.extend(get_double_jumps(board, color, row, col))
    return moves

def checkers_main(board, color):
    moves = get_moves_for_color(board, color)

    # Prioritize double jumps
    double_jump_moves = [move for move in moves if len(move) > 4]
    if double_jump_moves:
        return double_jump_moves[0]

    # Then prioritize single jumps
    single_jump_moves = [move for move in moves if len(move) == 4]
    if single_jump_moves:
        return single_jump_moves[0]

    # If no jumps, return the first regular move
    return moves[0] if moves else None

# Example usage:
if __name__ == "__main__":
    example_board = [
        ["X", "R01P", "X", "R03P", "X", "R05P", "X", "R07P"],
        ["R10P", "X", "R12P", "X", "R14P", "X", "R16P", "X"],
        ["X", "X", "X", "X", "X", "X", "X", "X"],
        [" ", "X", " ", "X", " ", "X", " ", "X"],
        ["X", "B52P", "X", " ", "X", " ", "X", " "],
        ["B50P", "X", "", "X", "B54P", "X", "B56P", "X"],
        ["X", "B61P", "X", "B63P", "X", "B65P", "X", "B67P"],
        ["B70P", "X", "B72P", "X", "B74P", "X", "B76P", "X"],
    ]

    # Print the initial board
    print("Initial Board:")
    for row in example_board:
        for col in row:
            print(row)

    # Perform the move for the red player
    red_move = checkers_main(example_board, "R")
    print("\nRed Player's Move:")
    print(red_move)

    # Perform the move for the black player
    black_move = checkers_main(example_board, "B")
    print("\nBlack Player's Move:")
    print(black_move)
