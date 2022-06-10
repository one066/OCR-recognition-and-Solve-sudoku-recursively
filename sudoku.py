import sys


def show(sudoku_list):
    for line in sudoku_list:
        print(" ".join(map(str, line)))


def input_init_list(user_default_data=False):
    if user_default_data:
        return [
            [1, 0, 6, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 8, 2, 0],
            [2, 0, 0, 0, 0, 5, 0, 0, 0],
            [0, 8, 0, 0, 4, 0, 0, 0, 7],
            [0, 0, 0, 6, 0, 3, 0, 0, 0],
            [5, 0, 0, 0, 1, 0, 0, 4, 0],
            [0, 0, 0, 9, 0, 0, 0, 0, 0],
            [0, 3, 9, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 9, 0, 5],
        ]

    _init_list = []
    for i in range(9):
        _init_list.append(list(map(int, input().split())))
    return _init_list


def can_fill_in_the_num(sudoku_list, index, try_fill_num):
    """填充数字"""
    row = index // 9  # 行
    cow = index % 9  # 列

    # 这一行有相同数字不能填入
    if try_fill_num in sudoku_list[row]:
        return False

    # 这一列有相同数字不能填入
    if try_fill_num in [sudoku_list[i][cow] for i in range(9)]:
        return False

    # 这一个九宫格有相同数字不能填入
    if try_fill_num in [
        sudoku_list[row // 3 * 3 + i // 3][cow // 3 * 3 + i % 3]
        for i in range(9)
    ]:
        return False

    return True


def solve_sudoku(sudoku_list, index=0):
    """解题"""
    if index == 81:
        show(sudoku_list)
        sys.exit()
        return

    if sudoku_list[index // 9][index % 9] > 0:
        solve_sudoku(sudoku_list, index + 1)

    for i in range(1, 10):
        if can_fill_in_the_num(sudoku_list, index, i):
            sudoku_list[index // 9][index % 9] = i
            solve_sudoku(sudoku_list, index + 1)
            sudoku_list[index // 9][index % 9] = 0


if __name__ == "__main__":
    init_list = input_init_list(user_default_data=True)
    solve_sudoku(init_list)
