# sudoku-solver

sudoku_solver.py implements a system that can find all possible solutions (ideally only one) to a 9x9 sudoku puzzle, stored as a 9x9 list of lists. 

sudoku_mouse_keyboard_controller.py provides assistance filling in the cells on an online sudoku puzzle.
After the user runs the script, they need to hit lShift when they are ready to start the following sequence:

1. The user first clicks the top left and the bottom right corners of the sudoku box. Care needs to be taken to make sure the location of the box on screen is not moved. Then, they press Shift.
2. The user clicks on all the 1's in the puzzle. Then, they press Shift.
3. Step 2 is repeated for all the other numbers in the puzzle.
4. Afterwards, the pynput mouse and keyboard controllers takes over and inputs the proper numbers into the sudoku board.

Note that at any point, rShift can be used to remove a click (Shift or Mouse) from the list. 
