def isValid(n, r, c, board):
    badrow = False
    badcol = False
    badcell = False
    cell = 0 # keypad cell designator for selected location (1-9)

    # determine if row is safe
    for i in range(9):
        if board[r][i].value == n:
            badrow = True

    # determine if col is safe
    for i in range(9):
        if board[i][c].value == n:
            badcol = True

    # determine which cell the number is in
    if (c < 3):
        if (r < 3):
            cell = 1
        elif (r < 6):
            cell = 4
        else:
            cell = 7
    elif (c < 6):
        if (r < 3):
            cell = 2
        elif (r < 6):
            cell = 5
        else:
            cell = 8
    elif (c < 9):
        if (r < 3):
            cell = 3
        elif (r < 6):
            cell = 6
        else:
            cell = 9

    # determine if the cell is safe by checking the values in the cell [r][c] is in
    if (cell == 1):
        for i in range(3):
            for j in range(3):
                if (board[i][j].value == n):
                    badcell = True
    elif (cell == 2):
        for i in range(3):
            for j in range(3, 6):
                if (board[i][j].value == n):
                    badcell = True
    elif (cell == 3):
        for i in range(3):
            for j in range(6, 9):
                if (board[i][j].value == n):
                    badcell = True
    elif (cell == 4):
        for i in range(3, 6):
            for j in range(3):
                if (board[i][j].value == n):
                    badcell = True
    elif (cell == 5):
        for i in range(3, 6):
            for j in range(3, 6):
                if (board[i][j].value == n):
                    badcell = True
    elif (cell == 6):
        for i in range(3, 6):
            for j in range(6, 9):
                if (board[i][j].value == n):
                    badcell = True
    elif (cell == 7):
        for i in range(6, 9):
            for j in range(3):
                if (board[i][j].value == n):
                    badcell = True
    elif (cell == 8):
        for i in range(6, 9):
            for j in range(3, 6):
                if (board[i][j].value == n):
                    badcell = True
    else:
        for i in range(6, 9):
            for j in range(6, 9):
                if (board[i][j].value == n):
                    badcell = True

    if (badrow or badcol or badcell):
        return False
    return True

def isFull(board):
    for i in range(9):
        for j in range(9):
            if board[i][j].value == 0:
                return False
    return True

def Solve(board) -> bool:
    # if the board is full, we are done
    if isFull(board) == True:
        return True
    
    found = False

    # find the next unassigned location
    for row in range(9):
        for col in range(9):
            if board[row][col].value == 0:
                found = True
                break
        if found:
            break

    # for every digit, see if it is valid and leads to a solution
    for i in range(1, 10):
        if isValid(i, row, col, board):
            board[row][col].value = i # assign number to empty spot if valid
            if Solve(board) == True: # if this leads to a solution, return true
                return True
            else:
                board[row][col].value = 0 # else, reset the location to 0
    return False # return false if solution not found, this causes the current location to be reset to 0 and a different number to be selected (backtracking)
