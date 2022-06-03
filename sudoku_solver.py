# Sudoku Solver

import copy


def flatten(grid) -> list:
    '''Return the flattened (1D) form of a multidimensional list (a list of lists of lists...).'''
    flatList = []
    for item in grid:
        if type(item) is list:
            flatList.extend(flatten(item))
        else:
            flatList.append(item)
    return flatList

class SudokuGame:
    def __init__(self, board: list[list[int]]):
        self.board = [[(num if (num != 0) else list(range(1, 10))) for num in row] for row in board]
        self.iterations = 0
        self.solutions = []

    def __str__(self):
        return self.get_board_picture(self.board)

    def set_cell(self, row: int, column: int, value: int) -> None:
        '''Set the cell in the board at the specificed row and column (indexed at 1) to the specified value.'''
        self.board[row-1][column-1] = value

    def get_row(self, y: int) -> list:
        '''Return the values in the row at the specified position y in the board.'''
        return self.board[y]
    
    def get_column(self, x: int) -> list:
        '''Return the values in the column at the specified position x in the board.'''
        return [row[x] for row in self.board]
        
    def get_box(self, y, x) -> list:
        '''Return the values in the 3x3 box at the specified y, x position in the board.'''
        box_list = []
        for r in range(box_y := y // 3 * 3, box_y + 3):
            for c in range(box_x := x // 3 * 3, box_x + 3):
                box_list.append(self.board[r][c])
        return box_list

    def conflict_checker(self, y: int, x: int, n: int) -> bool:
        '''Return True if the input number n could be placed in the board at row y, column x without an immediate issue. 
        Return false otherwise.'''
        if n in self.get_row(y):
            return False
        if n in self.get_column(x):
            return False
        if n in self.get_box(y, x):
            return False
        return True

    def check_board(self):
        '''Check the full board for any immediate issues. Return True if no conflicts are found and False if otherwise'''
        for num in range(1, 10):
            for r in range(9):
                if self.get_row(r).count(num) > 1:
                    return False
            for c in range(9):
                if self.get_column(c).count(num) > 1:
                    return False
            for r in range(0, 9, 3):
                for c in range(0, 9, 3):
                    if self.get_box(r, c).count(num) > 1:
                        return False
        return True

    def extrapolate(self):
        '''Deduce what numbers must be in the board in its current state and put them there. 
        Update the list in the unfilled cells (this list contains all possible values that could be put there in the current board state).
        Return False if any cell has no possible numbers or a number has no possible occurence in a section. 
        Return True if otherwise.'''
        updating = True
        while updating == True:
            updating = False
            for r in range(9):
                for c in range(9):
                    if type(self.board[r][c]) is list:
                        for num in self.board[r][c].copy():
                            if not self.conflict_checker(r, c, num):
                                self.board[r][c].remove(num)
            for r in range(9):
                for c in range(9):
                    if type(self.board[r][c]) is list:
                        if len(self.board[r][c]) == 0:
                            return False
                        if len(self.board[r][c]) == 1:
                            num = self.board[r][c][0]
                            if not self.conflict_checker(r, c, num):
                                return False
                            self.board[r][c] = num
                            updating = True
                            continue
                        for num in range(1, 10):
                            if flatten(self.get_row(r)).count(num) == 0 or flatten(self.get_column(c)).count(num) == 0 or flatten(self.get_box(r, c)).count(num) == 0:
                                return False
                        for num in self.board[r][c]:
                            if self.conflict_checker(r, c, num):
                                if flatten([x for x in self.get_row(r) if type(x) is list]).count(num) == 1 or flatten([x for x in self.get_column(c) if type(x) is list]).count(num) == 1 or flatten([x for x in self.get_box(r, c) if type(x) is list]).count(num) == 1:
                                    self.board[r][c] = num
                                    updating = True
                                    break
        return True
    
    def solve(self):
        '''Use this backtracking algorithm to solve the sudoku puzzle.'''
        for r in range(9):
            for c in range(9):
                if type(self.board[r][c]) is list:
                    for num in self.board[r][c]:
                        if self.conflict_checker(r, c, num):
                            board_copy = copy.deepcopy(self.board)
                            self.board[r][c] = num
                            self.iterations += 1

                            if self.extrapolate():
                                self.solve()

                            self.board = board_copy
                    return
        print(self)
        print('Iterations:', self.iterations)
        self.solutions.append(copy.deepcopy(self.board))
        # input('Continue?')

    def start_solving(self):
        '''Initiate the sudoku solving process. Return False if no solution is found and return True otherwise.'''
        if not (self.check_board() and self.extrapolate()):
            return False
        self.solve()
        if (solution_count := len(self.solutions)) < 1:
            return False
        print('Solutions:', solution_count)
        return True
        
    @staticmethod
    def get_empty_board() -> list[list[int]]:
        '''Return an empty 9x9 sudoku board.'''
        return [[0] * 9 for i in range(9)]

    @staticmethod
    def get_board_picture(board: list[list[int]]) -> str:
        '''Return the string representation of a 9x9 sudoku board.'''
        board_copy = copy.deepcopy(board)
        board_copy = [[(num if (num != 0 and type(num) is not list) else '.') for num in row] for row in board_copy]

        pic = ''
        h_line = ('|' + '=' * 7) * 3 + '|'

        for i, row in enumerate(board_copy):
            if i % 3 == 0:
                pic += h_line + '\n'
            pic += str.join('', ((f"{num} " if j % 3 != 0 else f"| {num} ") for j, num in enumerate(row))) + '|\n'
        
        pic += h_line
        return pic


if __name__ == "__main__":
    # board = [
    #     [0, 0, 0] + [0, 0, 0] + [0, 0, 0], 
    #     [0, 0, 0] + [0, 0, 0] + [0, 0, 0], 
    #     [0, 0, 0] + [0, 0, 0] + [0, 0, 0], 
    #
    #     [0, 0, 0] + [0, 0, 0] + [0, 0, 0], 
    #     [0, 0, 0] + [0, 0, 0] + [0, 0, 0], 
    #     [0, 0, 0] + [0, 0, 0] + [0, 0, 0], 
    # 
    #     [0, 0, 0] + [0, 0, 0] + [0, 0, 0], 
    #     [0, 0, 0] + [0, 0, 0] + [0, 0, 0], 
    #     [0, 0, 0] + [0, 0, 0] + [0, 0, 0]
    # ]

    # anti brute force
    game = SudokuGame(SudokuGame.get_empty_board())
    game.set_cell(2, 6, 3)
    game.set_cell(2, 8, 8)
    game.set_cell(2, 9, 5)
    game.set_cell(3, 3, 1)
    game.set_cell(3, 5, 2)
    game.set_cell(4, 4, 5)
    game.set_cell(4, 6, 7)
    game.set_cell(5, 3, 4)
    game.set_cell(5, 7, 1)
    game.set_cell(6, 2, 9)
    game.set_cell(7, 1, 5)
    game.set_cell(7, 8, 7)
    game.set_cell(7, 9, 3)
    game.set_cell(8, 3, 2)
    game.set_cell(8, 5, 1)
    game.set_cell(9, 5, 4)
    game.set_cell(9, 9, 9)


    print(game, '\n')
    print(game.start_solving())