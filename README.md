<header>
<h1 class="title">Module <code>MineSweeper</code></h1>
  <b> This is a little minesweeper game that I made.</b> 
</header>
<section id="section-intro">
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">import string
import random as rnd


def make_board(lines):
    &#34;&#34;&#34;
    This function takes the lines input, and creates
    the board according to this number.
    &#34;&#34;&#34;
    board = []
    line_start = list(string.ascii_uppercase)
    for rows in range(lines + 1):
        board.append([rows])
        if rows == 0:
            for columns in range(lines):
                board[rows].append(f&#34;{columns+1}&#34;)
        else:
            for columns in range(lines):
                if columns == 0:
                    board[rows] = [line_start[rows - 1]]
                board[rows].append(&#34;#&#34;)
    return board


def add_bombs(bombs, game_board):
    &#34;&#34;&#34;
    This function adds bombs to the board,
    based on the number of bombs input by the player
    &#34;&#34;&#34;
    b = 0
    while b != bombs:
        rows, columns = rnd.randint(1, len(game_board) - 1), rnd.randint(
            1, len(game_board) - 1
        )
        if game_board[rows][columns] == &#34;X&#34;:
            rows, columns = rnd.randint(1, len(game_board) - 1), rnd.randint(
                1, len(game_board) - 1
            )
            game_board[rows][columns] = &#34;X&#34;
        else:
            game_board[rows][columns] = &#34;X&#34;
        b += 1
    return game_board


def print_board(board):
    &#34;&#34;&#34;
    A helper function to print the board
    &#34;&#34;&#34;
    for i in range(len(board)):
        print(board[i])


def find_position(board, letter):
    &#34;&#34;&#34;
    Also a helper function, that finds the position of the
    first character input by the player, and returns
    with the row number of that character
    &#34;&#34;&#34;
    for rows in range(len(board)):
        for columns in range(len(board)):
            if board[rows][columns] == letter:
                return rows


def reveal(board, display_board, to_reveal, position_str):
    &#34;&#34;&#34;
    This is the main function of the program it takes an input
    and converts it to a row and a column number, then checks if
    the player hit a bomb or if they have revealed all the cells
    that need to be revealed. If not then it checks the positiion
    that the player picked, then displays the amount of mines
    beside it, if there are 0 it discovers the nearby cells until
    it finds a bomb, then asks for the next position to reveal.
    &#34;&#34;&#34;
    letter = position_str[0].upper()
    rows = find_position(board, letter)
    columns = int(position_str[1::])
    revealed_non_mine_cells = count_revealed(board)
    if board[rows][columns] == &#34;X&#34;:
        print(&#34;Game over, you found a bomb!&#34;)
        print_board(board)
        try:
            print(input(&#34;Press enter to play another round(ctrl+C to quit)&#34;))
            play_game()
        except KeyboardInterrupt:
            print()
    elif revealed_non_mine_cells + 1 == to_reveal:
        print(&#34;Congratulations, You WIN!!!!&#34;)
        board[rows][columns] = count_surrounding_mines(board, rows, columns)
        print_board(board)
        try:
            print(input(&#34;Press enter to play another round(ctrl+C to quit)&#34;))
            play_game()
        except KeyboardInterrupt:
            print()
    elif revealed_non_mine_cells &lt; to_reveal:
        board[rows][columns] = count_surrounding_mines(board, rows, columns)
        display_board[rows][columns] = board[rows][columns]
        if board[rows][columns] == &#34;0&#34;:
            reveal_surrounding_empty(board, rows, columns, display_board)
        print_board(display_board)
        position_str = input(&#34;Please enter another position to reveal: &#34;)
        reveal(board, display_board, to_reveal, position_str)

    return board


def count_revealed(board):
    &#34;&#34;&#34;
    Counts the amount of revealed cells on the board
    &#34;&#34;&#34;
    count = 0
    for i in range(1, len(board)):
        for j in range(1, len(board)):
            if board[i][j] in [&#34;0&#34;, &#34;1&#34;, &#34;2&#34;, &#34;3&#34;, &#34;4&#34;, &#34;5&#34;, &#34;6&#34;, &#34;7&#34;, &#34;8&#34;]:
                count += 1
    return count


def count_non_mine_cells(board):
    &#34;&#34;&#34;
    Counts the maximum amount of cells that can be counted
    &#34;&#34;&#34;
    count = sum(row.count(&#34;#&#34;) for row in board)
    return count


def reveal_surrounding_empty(board, rows, columns, display_board):
    &#34;&#34;&#34;
    This function uses a directions list to check every position
    surrounding itself, if there are no bombs, then reveal around
    the surrounding ones and apply this same logic until there is a bomb
    &#34;&#34;&#34;
    if board[rows][columns] != &#34;0&#34;:
        return
    directions = [
        (i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0
    ]

    for dx, dy in directions:
        new_row, new_col = rows + dx, columns + dy
        if (
            0 &lt;= new_row &lt; len(board)
            and 0 &lt;= new_col &lt; len(board[0])
            and board[new_row][new_col] == &#34;#&#34;
        ):
            board[new_row][new_col] = count_surrounding_mines(board, new_row, new_col)
            display_board[new_row][new_col] = board[new_row][new_col]
            reveal_surrounding_empty(board, new_row, new_col, display_board)


def count_surrounding_mines(board, rows, columns):
    &#34;&#34;&#34;
    Count the number of mines surrounding a position,
    with the help of the directions list
    &#34;&#34;&#34;
    mine_count = 0
    directions = [
        (i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0
    ]

    for dx, dy in directions:
        new_row, new_col = rows + dx, columns + dy
        if (
            0 &lt;= new_row &lt; len(board)
            and 0 &lt;= new_col &lt; len(board[0])
            and board[new_row][new_col] == &#34;X&#34;
        ):
            mine_count += 1
    return f&#34;{mine_count}&#34;


def play_game():
    &#34;&#34;&#34;
    This is the main function that has all the other necessary
    functions and variables to play a game inside a function
    &#34;&#34;&#34;
    while True:
        try:
            lines = int(input(&#34;How big should the board be?&#34;))
            bombs = int(input(&#34;How many bombs there should be?&#34;))
            break
        except (ValueError, TypeError):
            print(&#34;Please enter a valid number&#34;)
    display_map = make_board(lines).copy()
    game_map = make_board(lines).copy()
    print_board(display_map)
    add_bombs(bombs, game_map)
    to_reveal = count_non_mine_cells(game_map)
    position_str = input(&#34;Please enter a position to reveal: &#34;)
    reveal(game_map, display_map, to_reveal, position_str)


play_game()</code></pre>
</details>
</section>
<section>
</section>
<section>
</section>
<section>
<h2 class="section-title" id="header-functions">Functions</h2>
<dl>
<dt id="MineSweeper.add_bombs"><code class="name flex">
<span>def <span class="ident">add_bombs</span></span>(<span>bombs, game_board)</span>
</code></dt>
<dd>
<div class="desc"><p>This function adds bombs to the board,
based on the number of bombs input by the player</p></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">def add_bombs(bombs, game_board):
    &#34;&#34;&#34;
    This function adds bombs to the board,
    based on the number of bombs input by the player
    &#34;&#34;&#34;
    b = 0
    while b != bombs:
        rows, columns = rnd.randint(1, len(game_board) - 1), rnd.randint(
            1, len(game_board) - 1
        )
        if game_board[rows][columns] == &#34;X&#34;:
            rows, columns = rnd.randint(1, len(game_board) - 1), rnd.randint(
                1, len(game_board) - 1
            )
            game_board[rows][columns] = &#34;X&#34;
        else:
            game_board[rows][columns] = &#34;X&#34;
        b += 1
    return game_board</code></pre>
</details>
</dd>
<dt id="MineSweeper.count_non_mine_cells"><code class="name flex">
<span>def <span class="ident">count_non_mine_cells</span></span>(<span>board)</span>
</code></dt>
<dd>
<div class="desc"><p>Counts the maximum amount of cells that can be counted</p></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">def count_non_mine_cells(board):
    &#34;&#34;&#34;
    Counts the maximum amount of cells that can be counted
    &#34;&#34;&#34;
    count = sum(row.count(&#34;#&#34;) for row in board)
    return count</code></pre>
</details>
</dd>
<dt id="MineSweeper.count_revealed"><code class="name flex">
<span>def <span class="ident">count_revealed</span></span>(<span>board)</span>
</code></dt>
<dd>
<div class="desc"><p>Counts the amount of revealed cells on the board</p></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">def count_revealed(board):
    &#34;&#34;&#34;
    Counts the amount of revealed cells on the board
    &#34;&#34;&#34;
    count = 0
    for i in range(1, len(board)):
        for j in range(1, len(board)):
            if board[i][j] in [&#34;0&#34;, &#34;1&#34;, &#34;2&#34;, &#34;3&#34;, &#34;4&#34;, &#34;5&#34;, &#34;6&#34;, &#34;7&#34;, &#34;8&#34;]:
                count += 1
    return count</code></pre>
</details>
</dd>
<dt id="MineSweeper.count_surrounding_mines"><code class="name flex">
<span>def <span class="ident">count_surrounding_mines</span></span>(<span>board, rows, columns)</span>
</code></dt>
<dd>
<div class="desc"><p>Count the number of mines surrounding a position,
with the help of the directions list</p></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">def count_surrounding_mines(board, rows, columns):
    &#34;&#34;&#34;
    Count the number of mines surrounding a position,
    with the help of the directions list
    &#34;&#34;&#34;
    mine_count = 0
    directions = [
        (i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0
    ]

    for dx, dy in directions:
        new_row, new_col = rows + dx, columns + dy
        if (
            0 &lt;= new_row &lt; len(board)
            and 0 &lt;= new_col &lt; len(board[0])
            and board[new_row][new_col] == &#34;X&#34;
        ):
            mine_count += 1
    return f&#34;{mine_count}&#34;</code></pre>
</details>
</dd>
<dt id="MineSweeper.find_position"><code class="name flex">
<span>def <span class="ident">find_position</span></span>(<span>board, letter)</span>
</code></dt>
<dd>
<div class="desc"><p>Also a helper function, that finds the position of the
first character input by the player, and returns
with the row number of that character</p></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">def find_position(board, letter):
    &#34;&#34;&#34;
    Also a helper function, that finds the position of the
    first character input by the player, and returns
    with the row number of that character
    &#34;&#34;&#34;
    for rows in range(len(board)):
        for columns in range(len(board)):
            if board[rows][columns] == letter:
                return rows</code></pre>
</details>
</dd>
<dt id="MineSweeper.make_board"><code class="name flex">
<span>def <span class="ident">make_board</span></span>(<span>lines)</span>
</code></dt>
<dd>
<div class="desc"><p>This function takes the lines input, and creates
the board according to this number.</p></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">def make_board(lines):
    &#34;&#34;&#34;
    This function takes the lines input, and creates
    the board according to this number.
    &#34;&#34;&#34;
    board = []
    line_start = list(string.ascii_uppercase)
    for rows in range(lines + 1):
        board.append([rows])
        if rows == 0:
            for columns in range(lines):
                board[rows].append(f&#34;{columns+1}&#34;)
        else:
            for columns in range(lines):
                if columns == 0:
                    board[rows] = [line_start[rows - 1]]
                board[rows].append(&#34;#&#34;)
    return board</code></pre>
</details>
</dd>
<dt id="MineSweeper.play_game"><code class="name flex">
<span>def <span class="ident">play_game</span></span>(<span>)</span>
</code></dt>
<dd>
<div class="desc"><p>This is the main function that has all the other necessary
functions and variables to play a game inside a function</p></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">def play_game():
    &#34;&#34;&#34;
    This is the main function that has all the other necessary
    functions and variables to play a game inside a function
    &#34;&#34;&#34;
    while True:
        try:
            lines = int(input(&#34;How big should the board be?&#34;))
            bombs = int(input(&#34;How many bombs there should be?&#34;))
            break
        except (ValueError, TypeError):
            print(&#34;Please enter a valid number&#34;)
    display_map = make_board(lines).copy()
    game_map = make_board(lines).copy()
    print_board(display_map)
    add_bombs(bombs, game_map)
    to_reveal = count_non_mine_cells(game_map)
    position_str = input(&#34;Please enter a position to reveal: &#34;)
    reveal(game_map, display_map, to_reveal, position_str)</code></pre>
</details>
</dd>
<dt id="MineSweeper.print_board"><code class="name flex">
<span>def <span class="ident">print_board</span></span>(<span>board)</span>
</code></dt>
<dd>
<div class="desc"><p>A helper function to print the board</p></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">def print_board(board):
    &#34;&#34;&#34;
    A helper function to print the board
    &#34;&#34;&#34;
    for i in range(len(board)):
        print(board[i])</code></pre>
</details>
</dd>
<dt id="MineSweeper.reveal"><code class="name flex">
<span>def <span class="ident">reveal</span></span>(<span>board, display_board, to_reveal, position_str)</span>
</code></dt>
<dd>
<div class="desc"><p>This is the main function of the program it takes an input
and converts it to a row and a column number, then checks if
the player hit a bomb or if they have revealed all the cells
that need to be revealed. If not then it checks the positiion
that the player picked, then displays the amount of mines
beside it, if there are 0 it discovers the nearby cells until
it finds a bomb, then asks for the next position to reveal.</p></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">def reveal(board, display_board, to_reveal, position_str):
    &#34;&#34;&#34;
    This is the main function of the program it takes an input
    and converts it to a row and a column number, then checks if
    the player hit a bomb or if they have revealed all the cells
    that need to be revealed. If not then it checks the positiion
    that the player picked, then displays the amount of mines
    beside it, if there are 0 it discovers the nearby cells until
    it finds a bomb, then asks for the next position to reveal.
    &#34;&#34;&#34;
    letter = position_str[0].upper()
    rows = find_position(board, letter)
    columns = int(position_str[1::])
    revealed_non_mine_cells = count_revealed(board)
    if board[rows][columns] == &#34;X&#34;:
        print(&#34;Game over, you found a bomb!&#34;)
        print_board(board)
        try:
            print(input(&#34;Press enter to play another round(ctrl+C to quit)&#34;))
            play_game()
        except KeyboardInterrupt:
            print()
    elif revealed_non_mine_cells + 1 == to_reveal:
        print(&#34;Congratulations, You WIN!!!!&#34;)
        board[rows][columns] = count_surrounding_mines(board, rows, columns)
        print_board(board)
        try:
            print(input(&#34;Press enter to play another round(ctrl+C to quit)&#34;))
            play_game()
        except KeyboardInterrupt:
            print()
    elif revealed_non_mine_cells &lt; to_reveal:
        board[rows][columns] = count_surrounding_mines(board, rows, columns)
        display_board[rows][columns] = board[rows][columns]
        if board[rows][columns] == &#34;0&#34;:
            reveal_surrounding_empty(board, rows, columns, display_board)
        print_board(display_board)
        position_str = input(&#34;Please enter another position to reveal: &#34;)
        reveal(board, display_board, to_reveal, position_str)

    return board</code></pre>
</details>
</dd>
<dt id="MineSweeper.reveal_surrounding_empty"><code class="name flex">
<span>def <span class="ident">reveal_surrounding_empty</span></span>(<span>board, rows, columns, display_board)</span>
</code></dt>
<dd>
<div class="desc"><p>This function uses a directions list to check every position
surrounding itself, if there are no bombs, then reveal around
the surrounding ones and apply this same logic until there is a bomb</p></div>
<details class="source">
<summary>
<span>Expand source code</span>
</summary>
<pre><code class="python">def reveal_surrounding_empty(board, rows, columns, display_board):
    &#34;&#34;&#34;
    This function uses a directions list to check every position
    surrounding itself, if there are no bombs, then reveal around
    the surrounding ones and apply this same logic until there is a bomb
    &#34;&#34;&#34;
    if board[rows][columns] != &#34;0&#34;:
        return
    directions = [
        (i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0
    ]

    for dx, dy in directions:
        new_row, new_col = rows + dx, columns + dy
        if (
            0 &lt;= new_row &lt; len(board)
            and 0 &lt;= new_col &lt; len(board[0])
            and board[new_row][new_col] == &#34;#&#34;
        ):
            board[new_row][new_col] = count_surrounding_mines(board, new_row, new_col)
            display_board[new_row][new_col] = board[new_row][new_col]
            reveal_surrounding_empty(board, new_row, new_col, display_board)</code></pre>
</details>
</dd>
</dl>
</section>
<section>
</section>
</article>
<nav id="sidebar">
<h1>Index</h1>
<div class="toc">
<ul></ul>
</div>
<ul id="index">
<li><h3><a href="#header-functions">Functions</a></h3>
<ul class="">
<li><code><a title="MineSweeper.add_bombs" href="#MineSweeper.add_bombs">add_bombs</a></code></li>
<li><code><a title="MineSweeper.count_non_mine_cells" href="#MineSweeper.count_non_mine_cells">count_non_mine_cells</a></code></li>
<li><code><a title="MineSweeper.count_revealed" href="#MineSweeper.count_revealed">count_revealed</a></code></li>
<li><code><a title="MineSweeper.count_surrounding_mines" href="#MineSweeper.count_surrounding_mines">count_surrounding_mines</a></code></li>
<li><code><a title="MineSweeper.find_position" href="#MineSweeper.find_position">find_position</a></code></li>
<li><code><a title="MineSweeper.make_board" href="#MineSweeper.make_board">make_board</a></code></li>
<li><code><a title="MineSweeper.play_game" href="#MineSweeper.play_game">play_game</a></code></li>
<li><code><a title="MineSweeper.print_board" href="#MineSweeper.print_board">print_board</a></code></li>
<li><code><a title="MineSweeper.reveal" href="#MineSweeper.reveal">reveal</a></code></li>
<li><code><a title="MineSweeper.reveal_surrounding_empty" href="#MineSweeper.reveal_surrounding_empty">reveal_surrounding_empty</a></code></li>
</ul>
</li>
</ul>
</nav>
</main>
<footer id="footer">
<p>Generated by <a href="https://pdoc3.github.io/pdoc" title="pdoc: Python API documentation generator"><cite>pdoc</cite> 0.10.0</a>.</p>
</footer>
</body>
</html># MineSweeper
