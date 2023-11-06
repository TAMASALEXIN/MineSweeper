import string
import random as rnd


def make_board(lines):
    """
    This function takes the lines input, and creates
    the board according to this number.
    """
    board = []
    line_start = list(string.ascii_uppercase)
    for rows in range(lines + 1):
        board.append([rows])
        if rows == 0:
            for columns in range(lines):
                board[rows].append(f"{columns+1}")
        else:
            for columns in range(lines):
                if columns == 0:
                    board[rows] = [line_start[rows - 1]]
                board[rows].append("#")
    return board


def add_bombs(bombs, game_board):
    """
    This function adds bombs to the board,
    based on the number of bombs input by the player
    """
    b = 0
    while b != bombs:
        rows, columns = rnd.randint(1, len(game_board) - 1), rnd.randint(
            1, len(game_board) - 1
        )
        if game_board[rows][columns] == "X":
            rows, columns = rnd.randint(1, len(game_board) - 1), rnd.randint(
                1, len(game_board) - 1
            )
            game_board[rows][columns] = "X"
        else:
            game_board[rows][columns] = "X"
        b += 1
    return game_board


def print_board(board):
    """
    A helper function to print the board
    """
    for i in range(len(board)):
        print(board[i])


def find_position(board, letter):
    """
    Also a helper function, that finds the position of the
    first character input by the player, and returns
    with the row number of that character
    """
    for rows in range(len(board)):
        for columns in range(len(board)):
            if board[rows][columns] == letter:
                return rows


def reveal(board, display_board, to_reveal, position_str):
    """
    This is the main function of the program it takes an input
    and converts it to a row and a column number, then checks if
    the player hit a bomb or if they have revealed all the cells
    that need to be revealed. If not then it checks the positiion
    that the player picked, then displays the amount of mines
    beside it, if there are 0 it discovers the nearby cells until
    it finds a bomb, then asks for the next position to reveal.
    """
    letter = position_str[0].upper()
    rows = find_position(board, letter)
    columns = int(position_str[1::])
    revealed_non_mine_cells = count_revealed(board)
    if board[rows][columns] == "X":
        print("Game over, you found a bomb!")
        print_board(board)
        try:
            print(input("Press enter to play another round(ctrl+C to quit)"))
            play_game()
        except KeyboardInterrupt:
            print()
    elif revealed_non_mine_cells + 1 == to_reveal:
        print("Congratulations, You WIN!!!!")
        board[rows][columns] = count_surrounding_mines(board, rows, columns)
        print_board(board)
        try:
            print(input("Press enter to play another round(ctrl+C to quit)"))
            play_game()
        except KeyboardInterrupt:
            print()
    elif revealed_non_mine_cells < to_reveal:
        board[rows][columns] = count_surrounding_mines(board, rows, columns)
        display_board[rows][columns] = board[rows][columns]
        if board[rows][columns] == "0":
            reveal_surrounding_empty(board, rows, columns, display_board)
        print_board(display_board)
        position_str = input("Please enter another position to reveal: ")
        reveal(board, display_board, to_reveal, position_str)

    return board


def count_revealed(board):
    """
    Counts the amount of revealed cells on the board
    """
    count = 0
    for i in range(1, len(board)):
        for j in range(1, len(board)):
            if board[i][j] in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]:
                count += 1
    return count


def count_non_mine_cells(board):
    """
    Counts the maximum amount of cells that can be counted
    """
    count = sum(row.count("#") for row in board)
    return count


def reveal_surrounding_empty(board, rows, columns, display_board):
    """
    This function uses a directions list to check every position
    surrounding itself, if there are no bombs, then reveal around
    the surrounding ones and apply this same logic until there is a bomb
    """
    if board[rows][columns] != "0":
        return
    directions = [
        (i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0
    ]

    for dx, dy in directions:
        new_row, new_col = rows + dx, columns + dy
        if (
            0 <= new_row < len(board)
            and 0 <= new_col < len(board[0])
            and board[new_row][new_col] == "#"
        ):
            board[new_row][new_col] = count_surrounding_mines(board, new_row, new_col)
            display_board[new_row][new_col] = board[new_row][new_col]
            reveal_surrounding_empty(board, new_row, new_col, display_board)


def count_surrounding_mines(board, rows, columns):
    """
    Count the number of mines surrounding a position,
    with the help of the directions list
    """
    mine_count = 0
    directions = [
        (i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0
    ]

    for dx, dy in directions:
        new_row, new_col = rows + dx, columns + dy
        if (
            0 <= new_row < len(board)
            and 0 <= new_col < len(board[0])
            and board[new_row][new_col] == "X"
        ):
            mine_count += 1
    return f"{mine_count}"


def play_game():
    """
    This is the main function that has all the other necessary
    functions and variables to play a game inside a function
    """
    while True:
        try:
            lines = int(input("How big should the board be?"))
            bombs = int(input("How many bombs there should be?"))
            break
        except (ValueError, TypeError):
            print("Please enter a valid number")
    display_map = make_board(lines).copy()
    game_map = make_board(lines).copy()
    print_board(display_map)
    add_bombs(bombs, game_map)
    to_reveal = count_non_mine_cells(game_map)
    position_str = input("Please enter a position to reveal: ")
    reveal(game_map, display_map, to_reveal, position_str)


play_game()
