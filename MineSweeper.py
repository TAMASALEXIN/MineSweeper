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

# Finds the position of the letter 
def find_position(board, letter):
    for rows in range(len(board)):
        for columns in range(len(board)):
            if board[rows][columns] == letter:
                return rows

# Reveals a given poisition on the board
def reveal(board,display_board,to_reveal,position_str):
    letter = position_str[0].upper()
    rows = find_position(board, letter)
    columns = int(position_str[1::])  
    revealed_non_mine_cells = count_revealed(board)
    if revealed_non_mine_cells + 1 == to_reveal:
        print("Congratulations, You WIN!!!!")
        board[rows][columns] = count_surrounding_mines(board, rows, columns)
    elif revealed_non_mine_cells < to_reveal:
        board[rows][columns] = count_surrounding_mines(board, rows, columns)
        display_board[rows][columns] = board[rows][columns]
        # If the selected cell is empty, reveal all surrounding empty cells
        if board[rows][columns] == "0":

            reveal_surrounding_empty(board,rows,columns,display_board)
        print_board(display_board)
        position_str = input("Please enter another position to reveal: ")
        reveal(board,display_board,to_reveal,position_str)
    elif board[rows][columns] == "X":
        print("Game over, you found a bomb!")         
        
       
    return board

def count_revealed(board):
    count = 0
    for i in range(1,len(board)):
        for j in range(1,len(board)):
            if board[i][j] in ['0','1','2','3','4','5','6','7','8']:
                count += 1
    return count

def count_non_mine_cells(board):
    count = sum(row.count('#') for row in board)
    return count

def reveal_surrounding_empty(board, rows, columns,display_board):
    if board[rows][columns] != '0':
        return

    directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]

    for dx, dy in directions:
        new_row, new_col = rows + dx, columns + dy
        if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]) and board[new_row][new_col] == '#':
            board[new_row][new_col] = count_surrounding_mines(board,new_row,new_col)
            display_board[new_row][new_col] = count_surrounding_mines(board,new_row,new_col)
            reveal_surrounding_empty(board, new_row, new_col,display_board)

def count_surrounding_mines(board, rows, columns):
    mine_count = 0
    directions = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]

    for dx, dy in directions:
        new_row, new_col = rows + dx, columns + dy
        if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]) and board[new_row][new_col] == 'X':
            mine_count += 1
    return f"{mine_count}"
    

        


lines = int(input("How many lines should the board have?(Please enter a positive number)"))
bombs = int(input("How many bombs should be on the board?")) # majd validáltatni

display_map = make_board(lines).copy()
game_map = make_board(lines).copy()
print_board(display_map)
add_bombs(bombs,game_map)
to_reveal = count_non_mine_cells(game_map)
position_str = input("Please enter a position to reveal: ")
reveal(game_map,display_map,to_reveal,position_str)
print_board(game_map)




