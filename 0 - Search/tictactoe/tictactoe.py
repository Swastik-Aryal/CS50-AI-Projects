"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    O_count = 0
    X_count = 0

    for row in range(3):
        for column in range(3):
            if board[row][column] == X:
                X_count += 1
            elif board[row][column] == O:
                O_count += 1

    if X_count > O_count:
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                possible_actions.add((row, column))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid Move")

    board_copy = copy.deepcopy(board)

    board_copy[action[0]][action[1]] = player(board)

    return board_copy


def check_rows_columns(board, player):

    # Checking the rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True

    # Checking the columns
    for column in range(3):
        if board[0][column] == board[1][column] == board[2][column] == player:
            return True

    return False


def check_diagonals(board, player):

    counter = 0

    # Principal Diagonal
    for row in range(3):
        for column in range(3):
            if (row == column) and (board[row][column] == player):
                counter += 1
    if counter == 3:
        return True

    counter = 0

    # Secondary Diagonal
    for row in range(3):
        for column in range(3):
            if (row + column == 2) and (board[row][column] == player):
                counter += 1

    if counter == 3:
        return True

    return False


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    if check_rows_columns(board, X) or check_diagonals(board, X):
        return X

    if check_rows_columns(board, O) or check_diagonals(board, O):
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True

    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    if player(board) == X:
        possible_actions = []

        for action in actions(board):
            possible_actions.append((min_value(result(board, action)), action))

        max_val = -1

        for i in range(len(possible_actions)):
            if possible_actions[i][0] >= max_val:
                max_val = possible_actions[i][0]
                optimal_action = possible_actions[i][1]

        return optimal_action

    if player(board) == O:
        possible_actions = []

        for action in actions(board):
            possible_actions.append((max_value(result(board, action)), action))

        min_val = 1

        for i in range(len(possible_actions)):
            if possible_actions[i][0] <= min_val:
                min_val = possible_actions[i][0]
                optimal_action = possible_actions[i][1]

        return optimal_action
