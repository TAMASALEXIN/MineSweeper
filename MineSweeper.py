import string
import random as rnd

lines = int(input("How many lines should the board have?"))
bombs = int(input("How many bombs should be on the board?"))
board = []
line_start = list(string.ascii_uppercase)


# Making the board
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

for i in range(len(board)):
    print(board[i])

# Placing bombs
b = 0
while b < bombs:
    rows , columns = rnd.randint(1,lines), rnd.randint(1,lines)
    board[rows][columns] = "X"
    b += 1



for i in range(len(board)):
    print(board[i])              

