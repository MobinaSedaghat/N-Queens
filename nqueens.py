import sys
import random

MAXQ = 100


def in_conflict(column, row, other_column, other_row):
    """
    Checks if two locations are in conflict with each other.
    :param column: Column of queen 1.
    :param row: Row of queen 1.
    :param other_column: Column of queen 2.
    :param other_row: Row of queen 2.
    :return: True if the queens are in conflict, else False.
    """
    if column == other_column:
        return True  # Same column
    if row == other_row:
        return True  # Same row
    if abs(column - other_column) == abs(row - other_row):
        return True  # Diagonal

    return False


def in_conflict_with_another_queen(row, column, board):
    """
    Checks if the given row and column correspond to a queen that is in conflict with another queen.
    :param row: Row of the queen to be checked.
    :param column: Column of the queen to be checked.
    :param board: Board with all the queens.
    :return: True if the queen is in conflict, else False.
    """
    for other_column, other_row in enumerate(board):
        if in_conflict(column, row, other_column, other_row):
            if row != other_row or column != other_column:
                return True
    return False


def count_conflicts(board):
    """
    Counts the number of queens in conflict with each other.
    :param board: The board with all the queens on it.
    :return: The number of conflicts.
    """
    cnt = 0

    for queen in range(0, len(board)):
        for other_queen in range(queen + 1, len(board)):
            if in_conflict(queen, board[queen], other_queen, board[other_queen]):
                cnt += 1

    return cnt


def evaluate_state(board):
    """
    Evaluation function. The maximal number of queens in conflict can be 1 + 2 + 3 + 4 + .. +
    (nquees-1) = (nqueens-1)*nqueens/2. Since we want to do ascending local searches, the evaluation function returns
    (nqueens-1)*nqueens/2 - countConflicts().
    :param board: list/array representation of columns and the row of the queen on that column
    :return: evaluation score
    """
    return (len(board) - 1) * len(board) / 2 - count_conflicts(board)


def print_board(board):

    print("\n")

    for row in range(len(board)):
        line = ''
        for column in range(len(board)):
            if board[column] == row:
                line += 'Q' if in_conflict_with_another_queen(row, column, board) else 'q'
            else:
                line += '.'
        print(line)


def init_board(nqueens):

    board = []

    for column in range(nqueens):
        board.append(random.randint(0, nqueens - 1))

    return board



def random_search(board):
    i = 0
    optimum = (len(board) - 1) * len(board) / 2

    while evaluate_state(board) != optimum:
        i += 1
        print('iteration ' + str(i) + ': evaluation = ' + str(evaluate_state(board)))
        if i == 1000:  # Give up after 1000 tries.
            break

        for column, row in enumerate(board):  # For each column, place the queen in a random row
            board[column] = random.randint(0, len(board) - 1)

    if evaluate_state(board) == optimum:
        print('Solved puzzle!')

    print('Final state is:')
    print("board:", board)
    print_board(board)


def hill_climbing(board):
    print("board:", board)
    while count_conflicts(board) != 0:
        best_moves = [[]] * len(board)
        for col in range(len(board)):
            max_row = board[col]
            best_moves[col] = best_moves[col] + [board[col]]
            for row in range(len(board)):
                evaluate = evaluate_state(board)
                board[col] = row
                if evaluate > max_row:
                    try:
                        a = best_moves[col].index(row)
                    except ValueError:
                        best_moves[col][-1] = row
                        max_row = evaluate
                if evaluate == max_row:
                    try:
                        a = best_moves[col].index(row)
                    except ValueError:
                        best_moves[col] = best_moves[col] + [row]
                        max_row = evaluate
                    print(best_moves)
                rand = random.randint(0, len(best_moves[col]) - 1)
                board[col] = best_moves[col][rand]

    print_board(board)


def simulated_annealing(board):
    t = 10
    start_time = time.time()
    print(board)
    while t > 1 and count_conflicts(board) != 0:
        for col in range(len(board)):
            board_copy = board.copy()
            maax = evaluate_state(board_copy)
            row = random.randint(0, len(board) - 1)
            board_copy[col] = row
            evaluate = evaluate_state(board_copy)
            if evaluate >= maax:
                board[col] = row
            if evaluate < maax:
                pr = mp.exp((evaluate - maax) / t)
                if pr > 0.9:
                    board[col] = row
            t = t - 0.0001

    print_board(board)
    end_time = time.time()
    print(end_time - start_time)


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError

        n_queens = int(sys.argv[1])
        if n_queens < 1 or n_queens > MAXQ:
            raise ValueError

    except ValueError:
        print('Usage: python n_queens.py NUMBER')
        return False

    print('Which algorithm to use?')
    algorithm = input('1: random, 2: hill-climbing, 3: simulated annealing \n')

    try:
        algorithm = int(algorithm)

        if algorithm not in range(1, 4):
            raise ValueError

    except ValueError:
        print('Please input a number in the given range!')
        return False

    board = init_board(n_queens)
    print('Initial board: \n')
    print_board(board)

    if algorithm == 1:
        random_search(board)
    if algorithm == 2:
        hill_climbing(board)
    if algorithm == 3:
        simulated_annealing(board)


if __name__ == "__main__":
    print(len(sys.argv))
    sys.argv.append(4)
    main()
