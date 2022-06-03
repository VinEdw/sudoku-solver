# sudoku mouse/keyboard controller

if __name__ == "__main__":
    import pynput
    from time import sleep
    from sudoku_solver import SudokuGame

    action_list = []

    def on_click(x, y, button, pressed):
        # print(x, y, button, pressed)
        pos = (x, y)
        if button == pynput.mouse.Button.left and not pressed:
            if (shift_count := action_list.count('shift')) > 0 : 
                action_list.append(pos)
                print(shift_count - 1, pos)
        # elif button == pynput.mouse.Button.middle and not pressed:
        #     return False

    def on_release(key):
        # print(key)
        if key == pynput.keyboard.Key.shift:
            action_list.append('shift')
            shift_count = action_list.count('shift')
            if shift_count >= 11:
                print('Listeners Stopped')
                mouse.stop()
                keyboard.stop()

            elif shift_count == 1:
                print("Start")
                print('Click the top left corner of the sudoku board. Then, click the bottom right corner of the board. Then press Shift.')
            
            elif shift_count > 1:
                print(f'Click all the {shift_count - 1}s in the puzzle. Then press Shift.')

        elif key == pynput.keyboard.Key.shift_r:
            try:
                print('Removed', action_list.pop())
            except:
                print('Removed Nothing')
        
        elif key == pynput.keyboard.Key.esc:
            mouse.stop()
            keyboard.stop()

    print('Welcome to this sudoku solving script.')
    print('At some points, your mouse and keyboard will be monitored or controlled by the computer.')
    print('If you need to cancel the program, press the Esc button during the listening stage.')
    print('Use the left mouse button for all the clicks described.')
    print('Use the Right Sift Key to remove the last action in the stack.')
    print('Press the Shift key when you are ready to start.')
    

    with pynput.mouse.Listener(on_click=on_click) as mouse, pynput.keyboard.Listener(on_press=on_release) as keyboard:
        mouse.join()
        keyboard.join()

    try:
        assert action_list.count('shift') == 11
        action_list = action_list[action_list.index('shift') + 1:]
        assert type(action_list[0]) is tuple
        assert type(action_list[1]) is tuple
        assert action_list[2] == 'shift'
    except:
        print('Script Cancelled')
        quit()
    
    # print(action_list)

    def action_interpreter(action_list: list, board: list[list[int]], skip_positions: list):
        board_corner = action_list[0]
        board_width = abs(action_list[0][0] - action_list[1][0])
        board_height = abs(action_list[0][1] - action_list[1][1])
        cell_width = board_width / 9
        cell_height = board_height / 9

        num = 0
        for val in action_list[2:]:
            if val == 'shift':
                num += 1
                continue

            row = int((val[1] - board_corner[1]) // cell_height)
            column = int((val[0] - board_corner[0]) // cell_width)

            if row < 0 or row > 8 or column < 0 or column > 8:
                print('Click at', val, 'ignored.')
                continue
            
            board[row][column] = num
            skip_positions.append((row, column))

    def action_initiater(action_list: list, board: list[list[int]], skip_positions: list[tuple]):
        board_corner = action_list[0]
        board_width = abs(action_list[0][0] - action_list[1][0])
        board_height = abs(action_list[0][1] - action_list[1][1])
        cell_width = board_width / 9
        cell_height = board_height / 9

        mouse = pynput.mouse.Controller()
        keyboard = pynput.keyboard.Controller()
        left_button = pynput.mouse.Button.left

        for r in range(9):
            y_pos = board_corner[1] + cell_height/2 + cell_height * r
            for c in range(9):
                if (r, c) in skip_positions:
                    continue
                x_pos = board_corner[0] + cell_width/2 + cell_width * c
                num = board[r][c]
                mouse.position = (x_pos, y_pos)
                mouse.press(left_button)
                mouse.release(left_button)
                sleep(0.05)
                keyboard.press(str(num))
                sleep(0.05)

    board = SudokuGame.get_empty_board()
    skip_positions = []
    action_interpreter(action_list, board, skip_positions)

    print(SudokuGame.get_board_picture(board))
    print(len(skip_positions), 'numbers identified')

    game = SudokuGame(board)
    if game.start_solving():
        if len(game.solutions) > 1:
            print('Too many solutions found. Script Cancelled')
            quit()
        sleep(2)
        action_initiater(action_list, game.solutions[0], skip_positions)
        print('Finished')
    else:
        print('No solution found. Script Cancelled')
        quit()
