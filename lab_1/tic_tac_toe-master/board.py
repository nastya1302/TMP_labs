import numpy as np

from utils import log


class Board(object):
    """
    The environment for the reinforcement learning project.

    It should:
        - Have a matrix of size = NxN (which is basically N rows and N columns where N is a positive integer, greater than 0)
            - I have taken N as 3, but that is not necessary.
        - Initialize the matrix with zeroes.
            - The values in the matrix will be represented by integers: 0, 1, 2.
                - 0: empty cell represented by ' '.
                - 1: cell occupied by symbol 'O'.
                - 2: cell occupied by symbol 'X'.
            - 'X' or 'O' can be chosen by the player at initialization step by providing a choice in `player_sym`, defaults to 'x'
            - The other symbol will be chosen for the bot.
        - Have a property of winner, initialized by None.
        - Have a method to reset the board.
        - Have a method to represent the board in a human friendly form using 'X', 'O' and ' ' instead of the respective integers 2, 1, and 0.
        - Have a method which lets a user play by plotting a symbol of 'X' or 'O' only! anywhere within the matrix.
        - Calculates if there is a winner after each symbol is plotted.
            - A win is defined by any row, column or diagonal being filled with the same symbol, with the symbol as the winner.
        - If there is a winner, prints a message for the same.
    """
    def __init__(self, n: int = 3, player_sym: str = 'x') -> None:
        """
        Constructor of the Board class, creates board objects.

        - n(default=3) int: The number of rows and columns in the tic-tac-toe board.
        - player_sym(default='x') str: The symbol chosen by a human player.
        """
        self.board = None
        self.reset_board(n)
        self.stale = False

        self.sym_o = {'mark': 'O', 'value': 1}
        self.sym_x = {'mark': 'X', 'value': 2}
        self.sym_empty = {'mark': ' ', 'value': 0}

        self.player_sym, self.bot_sym = (
            (self.sym_x, self.sym_o)
            if player_sym.lower() == 'x'
            else (self.sym_o, self.sym_x)
        )
        self.winner = None

    def reset_board(self, n: int = 3) -> None:
        """
        params:

        - n(default=3): int: The number of rows and columns in the tic-tac-toe board.
        Clear the board when the game is to be restarted or a new game has to be started.
        """
        self.board = np.zeros((n, n)).astype(int)
        self.winner = None

    def draw_char_for_item(self, item: int):
        """
        Returns the string mapping of the integers in the matrix
        which can be understood by, but is not equal to:
        {
            0: ' ',
            1: 'O',
            2: 'X'
        }
        (The exact mapping is present in the constructor)

        params:

        - item int: One of (1, 2, 0) representing the mark of the player, bot or empty.
        return: str
        """
        if item == self.sym_x.get('value'):
            return self.sym_x.get('mark')
        elif item == self.sym_o.get('value'):
            return self.sym_o.get('mark')
        else:
            return self.sym_empty.get('mark')

    def draw_board(self) -> None:
        """
        Prints a human friendly representation of the tic-tac-toe board.
        """
        elements_in_board = self.board.size

        items = [
            self.draw_char_for_item(self.board.item(item_idx))
            for item_idx in range(elements_in_board)
        ]
        board = """
             {} | {} | {}
            -----------
             {} | {} | {}
            -----------
             {} | {} | {}
        """.format(
            *items
        )
        print(board)

    def have_same_val(self, axis: int, item: int, item_x: int, item_y: int) -> bool:
        """
        Oh boy! without the documentation this would be just 12-14 lines of code.

        Checks if a row(if axis = 0) of the board matrix has same values throughout.
                                    or
        Checks if a column(if axis = 1) of the board matrix has same values throughout.

        This is useful to check if a row or column is filled up by the symbol which was added the latest.

        params:

        - axis int: The direction along which operations are to be performed. Can have a value of 0 or 1 only.
            - 0 means row
            - 1 means column
        - item_x int: The row of the matrix in which item has been inserted.
        - item_y int: The column of the matrix in which the item has been inserted.
        - item int: The latest integer inserted into the matrix at row-index = item_x, and column-index = item_y.
        """
        max_limit, _ = self.board.shape
        result = True
        row_idx = col_idx = 0

        main_idx, fixed_idx, ignore_idx = (
            (col_idx, item_x, item_y) if axis == 0 else (row_idx, item_y, item_x)
        )

        while main_idx < max_limit:
            if main_idx != ignore_idx:

                board_item = (
                    self.board[fixed_idx][main_idx]
                    if axis == 0
                    else self.board[main_idx][fixed_idx]
                )

                if board_item != item or board_item == 0:
                    result = False
                    break
            main_idx += 1
        return result

    def left_diagonal_has_same_values(self, item: int, item_x: int, item_y: int) -> bool:
        """
        params

        - item_x int: The row of the matrix in which item has been inserted.
        - item_y int: The column of the matrix in which the item has been inserted.
        - item int: The latest integer inserted into the matrix at row-index = item_x, and column-index = item_y.
        """
        i = j = 0
        result = True
        max_limit, _ = self.board.shape

        while i < max_limit:
            if i != item_x:
                if self.board[i][j] != item or self.board[i][j] == 0:
                    result = False
                    break
            i += 1
            j += 1
        return result

    def right_diagonal_has_same_values(self, item: int, item_x: int, item_y: int) -> bool:
        """
        params

        - item_x int: The row of the matrix in which item has been inserted.
        - item_y int: The column of the matrix in which the item has been inserted.
        - item int: The latest integer inserted into the matrix at row-index = item_x, and column-index = item_y.
        """
        result = True
        max_limit, _ = self.board.shape
        i = 0
        j = max_limit - 1
        while i < max_limit:
            if i != item_x:
                if self.board[i][j] != item or self.board[i][j] == 0:
                    result = False
                    break
            i += 1
            j -= 1
        return result

    def cols_have_same_values(self, item: int, item_x: int, item_y: int) -> bool:
        """
        Check if any of the columns have same values

        params

        - item_x int: The row of the matrix in which item has been inserted.
        - item_y int: The column of the matrix in which the item has been inserted.
        - item int: The latest integer inserted into the matrix at row-index = item_x, and column-index = item_y.
        """
        axis = 1
        return self.have_same_val(axis, item, item_x, item_y)

    def rows_have_same_values(self, item: int, item_x: int, item_y: int) -> bool:
        """
        Check if any of the rows have same values

        params

        - item_x int: The row of the matrix in which item has been inserted.
        - item_y int: The column of the matrix in which the item has been inserted.
        - item int: The latest integer inserted into the matrix at row-index = item_x, and column-index = item_y.
        """
        axis = 0
        return self.have_same_val(axis, item, item_x, item_y)

    def element_diagonal_has_same_value(self, item: int, item_x: int, item_y: int) -> bool:
        """
        Check if any of the diagonals have same values

        params

        - item_x int: The row of the matrix in which item has been inserted.
        - item_y int: The column of the matrix in which the item has been inserted.
        - item int: The latest integer inserted into the matrix at row-index = item_x, and column-index = item_y.
        """
        max_limit, _ = self.board.shape
        if item_x == item_y and item_x + item_y == max_limit - 1:
            return self.left_diagonal_has_same_values(
                item, item_x, item_y
            ) or self.right_diagonal_has_same_values(item, item_x, item_y)

        if item_x == item_y:
            return self.left_diagonal_has_same_values(item, item_x, item_y)

        if item_x + item_y == max_limit - 1:
            return self.right_diagonal_has_same_values(item, item_x, item_y)
        return False

    def is_game_over(self, item: int, item_x: int, item_y: int) -> bool:
        """
        Check if the game is over, which is defined by a row, column or diagonal having
        the same values as the latest inserted integer `item`.

        params

        - item_x int: The row of the matrix in which item has been inserted.
        - item_y int: The column of the matrix in which the item has been inserted.
        - item int: The latest integer inserted into the matrix at row-index = item_x, and column-index = item_y.
        """
        return (
            self.cols_have_same_values(item, item_x, item_y)
            or self.rows_have_same_values(item, item_x, item_y)
            or self.element_diagonal_has_same_value(item, item_x, item_y)
        )

    def is_winning_move(self, player: str, item: int, item_x: int, item_y: int) -> bool:
        """
        Check if the last move was a winning move, which is defined by a row, column or diagonal having
        the same values as the latest inserted integer `item`.

        params

        - item_x int: The row of the matrix in which item has been inserted.
        - item_y int: The column of the matrix in which the item has been inserted.
        - item int: The latest integer inserted into the matrix at row-index = item_x, and column-index = item_y.
        """
        if self.is_game_over(item, item_x, item_y):
            self.winner = player
            return True
        return False

    def is_stale(self) -> bool:
        """
        Checks if there is no vacant space on the board.
        """
        x, y = np.where(self.board == 0)
        if len(x) == 0 and len(y) == 0:
            self.stale = True
        log('is game stale? ', self.stale)
        return self.stale

    def player_move(self, input_symbol: str, item_x: int, item_y: int):
        """
        The method which facilitates insertion of values into the board matrix.

        params:

        - input_symbol: 'X' or 'O'
        - item_x int: The row of the matrix in which item has been inserted.
        - item_y int: The column of the matrix in which the item has been inserted.
        """
        symbol = None

        if input_symbol == self.sym_o.get('mark'):
            symbol = self.sym_o

        elif input_symbol == self.sym_x.get('mark'):
            symbol = self.sym_x

        else:
            return
        if self.board[item_x][item_y] == 0:
            self.board[item_x][item_y] = symbol.get('value')
            self.draw_board()

            if self.is_winning_move(
                symbol.get('mark'), symbol.get('value'), item_x, item_y
            ):
                print('Winner is: {}'.format(self.winner))
                return self.winner
            elif self.is_stale():
                print('Draw')
                return 'draw'

    def play(self, item_x: int, item_y: int) -> None:
        """
        The method exposed to a human user
        facilitates insertion of values into the board matrix.

        params:

        - input_symbol: 'X' or 'O'
        - item_x int: The row of the matrix in which item has been inserted.
        - item_y int: The column of the matrix in which the item has been inserted.
        """
        max_limit, _ = self.board.shape
        if item_x > max_limit - 1 or item_y > max_limit:
            return
        self.player_move(self.player_sym.get('mark'), item_x, item_y)

    def bot_play(self, item_x: int, item_y: int) -> None:
        """
        The method exposed to a bot
        facilitates insertion of values into the board matrix.

        params:

        - input_symbol: 'X' or 'O'
        - item_x int: The row of the matrix in which item has been inserted.
        - item_y int: The column of the matrix in which the item has been inserted.
        """
        max_limit, _ = self.board.shape
        if item_x > max_limit - 1 or item_y > max_limit:
            return
        self.player_move(self.bot_sym.get('mark'), item_x, item_y)
 