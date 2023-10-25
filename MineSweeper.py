import string
import random as rnd


# Making the board
def make_board(lines):
    board = []
    line_start = list(string.ascii_uppercase)
    for rows in range(lines+1):
        board.append([rows])
        if rows == 0 :
            for columns in range(lines):
                board[rows].append(f"{columns+1}")
        else : 
            for columns in range(lines):
                if columns == 0:
                    board[rows] = [line_start[rows-1]]
                board[rows].append("#")    
    return board

# Adding bombs
def add_bombs(bombs,game_board):
    b = 0
    while b < bombs:
        rows , columns = rnd.randint(1,len(game_board)-1), rnd.randint(1,len(game_board)-1)
        game_board[rows][columns] = "X"
        b += 1
    return game_board

# Drawing the map out for the player
def print_board(board):
    for i in range(len(board)):
        print(board[i])


# Asks the user which spot to reveal and reveals it on the board
def reveal(board):
    print("Please select a position to reveal on the board: ")
    letter = input("Please select a letter:")
    rows = board.index(f'{letter}')
    columns = int(input("Select a number:"))
    position = board[rows][columns]
    if position == "X":
        print("Game over, you found a bomb!")
    else:
        board[rows][columns] = "O"
        print_board(board)
    return board




lines = int(input("How many lines should the board have?(Please enter a positive number)"))
bombs = int(input("How many bombs should be on the board?")) # majd validáltatni

display_map = make_board(lines).copy()
game_map = make_board(lines).copy()
print_board(display_map)
add_bombs(bombs,game_map)
reveal(game_map)





