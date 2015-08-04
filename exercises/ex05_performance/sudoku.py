# Copyright Peter J.A. Cock, 2006
# All rights reserved.
# Original file name: sudoku_v105.py
# 
# You may choose to be bound by either:
#
# (a) Licenced free for personal non-commercial use.
#      May not be redistributed without prior permission.
#
# Or:
# (b) The GPL version 2, see http://www.gnu.org/licenses/gpl.html

# Distributed here under the GPL version 2
# Modified for Python 3 by Mike Woinoski (michaelw@articulatedesign.us.com)

import os
import time
import sys
# TODO: import functions from measure module
# from measure import measure, get_function_stats

TRIPLETS = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

# Row/Col/3x3 iteration list, each is nine lists of nine (row,col) pairs
ROW_ITER = [[(row, col) for col in range(0, 9)] for row in range(0, 9)]
COL_ITER = [[(row, col) for row in range(0, 9)] for col in range(0, 9)]
TxT_ITER = [[(row, col) for row in rows for col in cols]
            for rows in TRIPLETS for cols in TRIPLETS]


class Sudoku:
    def __init__(self, start_grid=None):
        # Setup list of lists (the rows), each row is a list of 9 cells, which
        # are each a list of integers 1-9 inclusive.
        self.squares = [[list(range(1, 10)) for _ in range(0, 9)]
                        for _ in range(0, 9)]
        
        if start_grid is not None:
            if len(start_grid) == 81:
                for row in range(0, 9):
                    self.set_row(row, start_grid[(row*9):((row+1)*9)])
            else:
                assert len(start_grid) == 9, "Bad input!"
                for row in range(0, 9):
                    self.set_row(row, start_grid[row])
                
        self._changed = False

    def solved(self):
        for row in range(0, 9):
            for col in range(0, 9):
                if len(self.squares[row][col]) > 1:
                    return False
        return True

    def copy(self):
        sudoku_copy = Sudoku(None)
        for row in range(0, 9):
            for col in range(0, 9):
                sudoku_copy.squares[row][col] = self.squares[row][col][:]  # copy!
        sudoku_copy._changed = False
        return sudoku_copy
    
    def set_row(self, row, x_list):
        assert len(x_list) == 9
        for col in range(0, 9):
            try:
                x = int(x_list[col])
            except ValueError:
                x = 0
            self.set_cell(row, col, x)

    def set_cell(self, row, col, x):
        if self.squares[row][col] == [x]:
            # Already done!
            pass
        elif x not in list(range(1, 9+1)):
            # Set to unknown
            pass
        else:
            assert x in self.squares[row][col], \
                "Told to set square (%i,%i) to an impossible entry, %i" % \
                (row, col, x)
            
            self.squares[row][col] = [x]
            self.update_neighbours(row, col, x)
            self._changed = True
            
    def cell_exclude(self, row, col, x):
        assert x in range(1, 9+1)
        if x in self.squares[row][col]:
            # Remove it...
            self.squares[row][col].remove(x)
            # Should be one or more entries left...
            assert len(self.squares[row][col]) > 0, \
                "Removed last possible entry for square (%i,%i) which was %i" \
                % (row, col, x)
            # Now, has this confirmed the value for this square?
            if len(self.squares[row][col]) == 1:
                # This cell is now definite..
                # Need to update its friends...
                self._changed = True
                self.update_neighbours(row, col, self.squares[row][col][0])
        else:
            # Don't need to remove this, already done!
            pass
        return

    def row_exclude(self, row, x):
        assert x in range(1, 9+1)
        for col in range(0, 9):
            self.cell_exclude(row, col, x)

    def col_exclude(self, col, x):
        assert x in range(1, 9+1)
        for row in range(0, 9):
            self.cell_exclude(row, col, x)

    def update_neighbours(self, set_row, set_col, x):
        """
        Call this when the square is set to x, either directly,
        or as a side effect of an exclude leaving only one entry
        """
        # Update the possibilities in this row...
        for row in range(0, 9):
            if row != set_row:
                self.cell_exclude(row, set_col, x)
        # Update the possibilities in this col...
        for col in range(0, 9):
            if col != set_col:
                self.cell_exclude(set_row, col, x)
        # Update the possibilities in this 3x3 square...
        rows = cols = []  # keep pylint happy
        for triplet in TRIPLETS:
            if set_row in triplet:
                rows = triplet[:]
            if set_col in triplet:
                cols = triplet[:]
        # Only need to do four of the eight possibles (well, 9 if you count
        # the cell itself) as did two on the row, and two on the col
        rows.remove(set_row)
        cols.remove(set_col)
        for row in rows:
            for col in cols:
                assert row != set_row or col != set_col 
                self.cell_exclude(row, col, x)
            
    def get_cell_int(self, row, col):
        if len(self.squares[row][col]) == 1:
            return int(self.squares[row][col][0])
        else:
            return 0

    def get_cell_str(self, row, col):
        if len(self.squares[row][col]) == 1:
            return "(%i,%i) = %i" % (row, col, self.squares[row][col][0])
        else:
            return ("(%i,%i) = " % (row, col)) + ",".join(
                [str(x) for x in self.squares[row][col]])

    def get_cell_digit_str(self, row, col):
        if len(self.squares[row][col]) == 1:
            return str(self.squares[row][col][0])
        else:
            return "0"
            
    def as_test_81(self):
        """Return a string of 81 digits"""
        return "".join(self.as_test_list())
            
    def simple_text(self):
        return "\n".join(self.as_test_list())
        
    def as_test_list(self):
        return [("".join([self.get_cell_digit_str(row, col)
                         for col in range(0, 9)])) for row in range(0, 9)]

    def __repr__(self):
        answer = "[" + ",".join([
            ("[" + ",".join([self.get_cell_digit_str(row, col)
                            for col in range(0, 9)]) + "]")
            for row in range(0, 9)])
        return answer

    def __str__(self):
        puzzle = "".join([self.get_cell_digit_str(row, col).replace("0", "?")
                          for row in range(9) for col in range(9)])
        return Sudoku.line_to_puzzle(puzzle)

    @staticmethod
    def line_to_puzzle(puzzle):
        answer = "   123   456   789\n"
        for row in range(0, 9):
            answer = answer + str(row+1) \
                + " [" + "".join([puzzle[row*9+col] for col in range(0, 3)]) \
                + "] [" + "".join([puzzle[row*9+col] for col in range(3, 6)]) \
                + "] [" + "".join([puzzle[row*9+col] for col in range(6, 9)]) \
                + "]\n"
            if row+1 in [3, 6]:
                answer += "   ---   ---   ---\n"
        return answer

    # TODO: add measure decorator to this method
    # @measure
    def check(self, level=0):
        self._changed = True
        while self._changed:
            self._changed = False
            self.check_for_single_occurances()
            self.check_for_last_in_row_col_3x3()
            if level >= 1:
                self.overlapping_3x3_and_row_or_col()  # aka slicing and dicing
            if level >= 2:
                self.one_level_supposition()
            if level >= 3:
                self.two_level_supposition()
            
            # If nothing happened, then self.changed==False (still)
            # and we break the loop
        return
        
    def check_for_single_occurances(self):
        # Want to see if x only occurs once in this row/col/3x3...
        for check_type in [ROW_ITER, COL_ITER, TxT_ITER]:
            for check_list in check_type:
                for x in range(1, 9+1):  # 1 to 9 inclusive
                    x_in_list = []
                    for (row, col) in check_list:
                        if x in self.squares[row][col]:
                            x_in_list.append((row, col))
                    if len(x_in_list) == 1:
                        (row, col) = x_in_list[0]
                        # This position MUST be be x
                        if len(self.squares[row][col]) > 1:
                            self.set_cell(row, col, x)

    def check_for_last_in_row_col_3x3(self):
        # Now, for each row/col/3x3 want to see if there is a single
        # unknown entry...
        for (type_name, check_type) in \
                [("Row", ROW_ITER), ("Col", COL_ITER), ("3x3", TxT_ITER)]:
            for check_list in check_type:
                unknown_entries = []
                unassigned_values = list(range(1, 9+1))  # 1-9 inclusive
                known_values = []
                for (row, col) in check_list:
                    if len(self.squares[row][col]) == 1:
                        assert self.squares[row][col][0] not in known_values, \
                            "Already have %i (%i,%i) in known list [%s] for %s" % \
                            (self.squares[row][col][0], row, col, ",".join(
                                map(str, known_values)), type_name)

                        known_values.append(self.squares[row][col][0])

                        assert self.squares[row][col][0] in unassigned_values, \
                            "Expected %i (%i,%i) in list [%s] for %s" % \
                            (self.squares[row][col][0], row, col, ",".join(
                                map(str, unassigned_values)), type_name)

                        unassigned_values.remove(self.squares[row][col][0])
                    else:
                        unknown_entries.append((row, col))
                assert len(unknown_entries) + len(known_values) == 9
                assert len(unknown_entries) == len(unassigned_values)
                if len(unknown_entries) == 1:
                    # This cell must be the only number 1-9 not in known_values
                    x = unassigned_values[0]
                    (row, col) = unknown_entries[0]
                    self.set_cell(row, col, x)
        return
        
    def diagnosis(self):
        answer = ""
        df = int(1)
        for row in range(0, 9):
            for col in range(0, 9):
                if len(self.squares[row][col]) > 1:
                    answer = answer + str(self.squares[row][col]) + "\n"
                    df *= len(self.squares[row][col])
        answer += "Degrees of freedom: %i" % df
        return answer

    def overlapping_3x3_and_row_or_col(self):
        """Block and Column / Row Interactions (name from Simon Armstrong)

        http://www.simes.clara.co.uk/programs/sudokutechnique3.htm

        Also known as 'slicing and dicing'
        """
        # For a given 3x3, and a given digit, want to see if
        # all the remaining candidates are in a single row or column..
        # Want to see if x only occurs once in this row/col/3x3...
        for check_list in TxT_ITER:
            for x in range(1, 9+1):  # 1 to 9 inclusive
                rows_for_x = []
                cols_for_x = []
                for (row, col) in check_list:
                    if x in self.squares[row][col]:
                        if row not in rows_for_x:
                            rows_for_x.append(row)
                        if col not in cols_for_x:
                            cols_for_x.append(col)
                # Are they all in the same row?
                if len(rows_for_x) == 1 and len(cols_for_x) > 1:
                    # This means, we can remove X from all the rest of the row...
                    row = rows_for_x[0]
                    for col in range(0, 9):
                        if col not in cols_for_x:
                            self.cell_exclude(row, col, x)
                    # We can also remove x from all the rest of this 3x3...
                    for (row, col) in check_list:
                        if col not in cols_for_x:
                            if row not in rows_for_x:
                                self.cell_exclude(row, col, x)
                # Are they all in the same col?
                if len(cols_for_x) == 1 and len(rows_for_x) > 1:
                    # This means, we can remove X from all the rest of the row...
                    col = cols_for_x[0]
                    for row in range(0, 9):
                        if row not in rows_for_x:
                            self.cell_exclude(row, col, x)
                    # We can also remove x from all the rest of this 3x3...
                    for (row, col) in check_list:
                        if col not in cols_for_x:
                            if row not in rows_for_x:
                                self.cell_exclude(row, col, x)

    # TODO: add measure decorator to this function
    # @measure
    def one_level_supposition(self):
        """
        Probably what is known as 'Nishio', try a number and see if it leads to
        a dead end.
        
        For all the ambiguous squares, try each possible each entry and see
        if its OK, or if it leads to a contradiction.  In the case of a
        contradiction we can remove it as a possibility...
        
        Two level suppositions (two guess) may be required for extreme puzzles
        """
        progress = True
        while progress:
            progress = False
            for row in range(0, 9):
                for col in range(0, 9):
                    if len(self.squares[row][col]) > 1:
                        bad_x = []
                        for x in self.squares[row][col]:
                            sudoku_copy = self.copy()
                            try:
                                sudoku_copy.set_cell(row, col, x)
                                sudoku_copy.check(level=1)
                            except AssertionError:
                                # Leads to an error:)
                                # This means that this square cannot be x
                                bad_x.append(x)
                            del sudoku_copy
                        if len(bad_x) == 0:
                            pass
                        elif len(bad_x) < len(self.squares[row][col]):
                            for x in bad_x:
                                self.cell_exclude(row, col, x)
                                self.check() 
                            progress = True
                        else:
                            assert False, "All possible values for square (%i,%i) fail" \
                                % (row, col)

    # TODO: add measure decorator to this function
    # @measure
    def two_level_supposition(self):
        progress = True
        while progress:
            progress = False
            for row in range(0, 9):
                for col in range(0, 9):
                    if len(self.squares[row][col]) > 1:
                        bad_x = []
                        for x in self.squares[row][col]:
                            sudoku_copy = self.copy()
                            try:
                                sudoku_copy.set_cell(row, col, x)
                                sudoku_copy.check(level=2)
                            except AssertionError:
                                # Leads to an error:)
                                # This means that this square cannot be x
                                bad_x.append(x)
                            del sudoku_copy
                        if len(bad_x) == 0:
                            pass
                        elif len(bad_x) < len(self.squares[row][col]):
                            for x in bad_x:
                                self.cell_exclude(row, col, x)
                                self.check() 
                            progress = True
                        else:
                            assert False, "All possible values for square (%i,%i) fail" \
                                % (row, col)

if __name__ == "__main__":
    # Using only check() and one_level_suposition(), completes 82 out of 95 in
    # this test file, http://magictour.free.fr/top95
    if len(sys.argv) == 1:
        print("Usage: {} input_file".format(sys.argv[0]), file=sys.stderr)
        exit(1)

    for test_file in sys.argv[1:]:
        if not os.path.isfile(test_file):
            print("Could not find test file " + test_file, file=sys.stderr)
        else:
            print("Running tests from file %s" % test_file)
            input_file = open(test_file, "r")
            score = 0
            count = 0
            line_copy = None
            solution = None
            start_time = time.time()
            while True:
                line = input_file.readline()
                if not line:
                    break
                if len(line) == 0:
                    break
                if line[-1] == "\n":
                    line = line[:-1]
                if line[-1] == "\r":
                    line = line[:-1]
                line_copy = str(line)
                if len(line) == 81:
                    count += 1
                    solution = Sudoku(line)
                    solution.check(level=2)
                    if not solution.solved():
                        print("Trying level two", end=' ')
                        solution.check(level=3)
                    if solution.solved():
                        # print(" - Done") #MW
                        score += 1
                    else:
                        print("- Failed")
                        print(solution.as_test_list())
                else:
                    print("Bad input at line {}:\n{}".format(count, line))
                if count % 2 == 0:
                    print('.', file=sys.stderr, end='', flush=True)

            print('Done', file=sys.stderr, flush=True)
            job_time = time.time()-start_time
            input_file.close()

            print("Solved {} / {} puzzles in {:0.2f} seconds"
                  .format(score, count, job_time))
            print("\nLast puzzle:\n")
            print(Sudoku.line_to_puzzle(line_copy))
            print("\nSolution:\n")
            print(solution)

            # TODO: print function stats returned by get_function_stats()
            # print('{:^53}'.format('Function Call Stats'))
            # print('{:24s} {:>8s}  {:22s}'
            #       .format('Function name', 'Calls', 'Avg Time (seconds)'))
            # print('-' * 53)
            # for stats in get_function_stats():
            #     print('{:24s} {:8d}  {:13.6f}'.format(*stats))
