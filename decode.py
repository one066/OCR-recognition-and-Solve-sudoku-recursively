def initial():
    '''
    参考数据
    '''
    initial_list = [[-1, 0, -6, -2, 0, 0, 0, 0, 0],
                    [0, 0, 0, -4, 0, 0, -8, -2, 0],
                    [-2, 0, 0, 0, 0, -5, 0, 0, 0],
                    [0, -8, 0, 0, -4, 0, 0, 0, -7],
                    [0, 0, 0, -6, 0, -3, 0, 0, 0],
                    [-5, 0, 0, 0, -1, 0, 0, -4, 0],
                    [0, 0, 0, -9, 0, 0, 0, 0, 0],
                    [0, -3, -9, 0, 0, -4, 0, 0, 0],
                    [0, 0, 0, 0, 0, -2, -9, 0, -5]]
    return initial_list

def check_list(index, i):
    '''
    检测填入数据是否合格
    '''
    row = index // 9
    cow = index % 9
    try:
        if initial_list[row][cow] < 0: return False
    except Exception as e:
        print(initial_list)
        print(row)
        print(cow)
        print(e)
    for x in range(9):
        if abs(initial_list[x][cow]) == i: return False
        if abs(initial_list[row][x]) == i: return False
    for a in range(3):
        for b in range(3):
            if abs(initial_list[a+3*(row//3)][b+3*(cow//3)]) == i: return False
    return True

def solve(index):
    '''
    采用递归填入数据
    '''
    global flag
    if flag == True:
        return
    if index == 80:
        print(show(initial_list))
        flag = True
        return
    for i in range(1, 10):
        if check_list(index, i):
            initial_list[index//9][index%9] = i
            solve(index + 1)
            initial_list[index//9][index%9] = 0

    if initial_list[index//9][index%9] < 0:
        solve(index + 1)

def show(initial_list):
    '''
    数据显示
    '''
    for i in range(9):
        for j in range(9):
            print(abs(initial_list[i][j]), end=" ")
        print()

def start(list):
    '''
    调用接口
    '''
    global flag,initial_list
    flag = False
    initial_list = list
    solve(0)
