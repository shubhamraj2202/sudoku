from datetime import datetime, timedelta
import re

EMPTY_ENTRY = 0
DEFAULT_STR = "2.....9..6..25..13.53..876........7452.417.8687........625..83.19..76..5..5.....7"


class Sudoku:
    def __init__(self, board=None):
        """
        Saves the puzzle data after converting it from a string to
        2-D list and saving other puzzle specific information.
        """
        if board is None:
            board = DEFAULT_STR
        self.board = self.convert_sudoku(board)
        self.totalBands, self.totalStacks = len(self.board), len(self.board[0])
        self.subGridSize = int(self.totalBands ** 0.5)
        self.allowedRange = range(1, self.totalBands + 1)
        self.global_timeout = None

    def sudoku_solution(self):
        """
        Wrapper which initiates the solution process for sudoku puzzle.
        The global_timeout maintains the time taken by the process so
        that infinite recursive calls can be avoided. It returns the
        final state of the puzzle (whether solved or not) and time taken
        to complete it.
        """
        try:
            start_time = datetime.now()
            self.global_timeout = start_time + timedelta(seconds=5)
            sudoku_solved = self.can_solve_sudoku_from_cell(0, 0)
            end_time = datetime.now()
        except TimeoutError:
            return self.timing_delta(timedelta(seconds=5)), False
        return self.timing_delta(end_time - start_time), sudoku_solved

    @staticmethod
    def validator(board):
        """
        Validates the authenticity of puzzle data received.
        """
        re_exp = "^[1-9.]*$"
        return re.match(re_exp, board) is not None and len(board) == 81

    @staticmethod
    def convert_sudoku(board):
        """
        Converts data from string to a 2-D list and replaces "." with 0.
        """
        sudoku_board, temp = [], []
        for index, i in enumerate(board):
            if index != 0 and index % 9 == 0:
                sudoku_board.append(temp)
                temp = []
            if i != ".":
                temp.append(int(i))
            else:
                temp.append(0)
        sudoku_board.append(temp)
        return sudoku_board

    @staticmethod
    def timing_delta(td):
        """
        Created so that the time can be easily mocked in test cases.
        Returns the time difference in timedelta format.
        """
        return td

    def template_printable(self):
        """
        Returns the saved 2-D puzzle which would be rendered
        to the HTML page after changing 0 to empty string.
        """
        temp = []
        for i in range(self.totalBands):
            temp.append(list(self.board[i]))
            for j in range(self.totalStacks):
                if temp[i][j] == 0:
                    temp[i][j] = ""
        return temp

    def can_solve_sudoku_from_cell(self, row, col):
        """
        Recursively called so that the solution of the puzzle can be
        obtained by the backtracking algorithm by filling the empty
        entries with valid values between 1 to 9.
        params:
        row, column: Current row and column to be assigned with a value
        """
        if datetime.now() > self.global_timeout:
            raise TimeoutError
        if col == self.totalStacks:
            col, row = 0, row + 1
            if row == self.totalBands:
                return True
        if self.board[row][col] != EMPTY_ENTRY:
            return self.can_solve_sudoku_from_cell(row, col + 1)
        for value in self.allowedRange:
            if self.can_place_value(row, col, value):
                self.board[row][col] = value
                if self.can_solve_sudoku_from_cell(row, col + 1):
                    return True
            self.board[row][col] = EMPTY_ENTRY
        return False

    def can_place_value(self, row, col, value_to_place):
        """
        Checks whether the value to be placed in the current row and
        column follows all the three rules i.e. the value should not be
        present in whole same column, the value should not be present
        in whole same row, and the value should not be present in whole
        same sub-grid (3x3). If the value violates any of the conditions
        then the value cannot be used at the current place.
        """
        if value_to_place in self.board[row]:
            return False
        for row_num in range(self.totalStacks):
            if value_to_place == self.board[row_num][col]:
                return False
        if self.value_present_in_sub_grid(row, col, value_to_place):
            return False
        return True

    def value_present_in_sub_grid(self, row, col, value_to_place):
        """
        Check whether value exists in the sub-grid or not.
        """
        vertical_grid_index, hor_grid_index = (row // self.subGridSize,
                                               col // self.subGridSize)
        top_left_row, top_left_col = (self.subGridSize * vertical_grid_index,
                                      self.subGridSize * hor_grid_index)
        for inc_row in range(self.subGridSize):
            for inc_col in range(self.subGridSize):
                if value_to_place == self.board[top_left_row + inc_row][top_left_col + inc_col]:
                    return True
        return False
