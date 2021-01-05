import tesserocr
import locale
locale.setlocale(locale.LC_ALL, 'C')
from PIL import Image
import decode

def seach_line_data(size, flag = False):
    '''
    寻找边界
    '''
    size_temp = size
    if flag is True:
        size_temp = (size_temp[1], size_temp[0])
    message = {}
    src_strlist = img.load()
    for i in range(size_temp[0]):
        for j in range(size_temp[1]):
            num = src_strlist[i, j] if flag == False else src_strlist[j, i]
            try:
                num_1 = src_strlist[i-1, j] if flag == False else src_strlist[j, i-1]
            except:
                num_1 = src_strlist[i + 1, j] if flag == False else src_strlist[j, i+1]
            if abs((num[0]+num[1]+num[2])-(num_1[0]+num_1[1]+num_1[2])) > 300:
                if i not in message:
                    message[i] = 1
                else:
                    message[i] += 1
    return [k for k, v in message.items() if v>=size[0]*0.7]

def cut_img():
    '''
    通过寻找到的边界裁剪图片
    '''
    size = img.size
    col_line = seach_line_data(size)
    row_line = seach_line_data(size, True)
    # print(col_line)
    # print(row_line)
    region = img.crop((col_line[0], row_line[0], col_line[-1], row_line[-1]))
    #region.show()
    return region

def img_paste(block):
    '''
    将每个数字复制五份合起来，
    因为单独数字识别不了，需要多个结合在一起
    '''
    gd = Image.open('background.png')
    for xx in range(5):
        gd.paste(block, (xx * 25, 0))
    return gd

def img_block(img):
    '''
    将图片切割为81份单独识别
    '''
    nums = [[],[],[],[],[],[],[],[],[]]
    size = img.size
    step = size[0] // 9
    for i in range(9):
        for j in range(9):
            block = img.crop((12+i*step, 8+j*step, (i + 1)*step - 10, (j + 1)*step - 2))
            block = block.convert('L')
            threshold = 125
            table = [0 if i < threshold else 1 for i in range(256)]
            block = block.point(table, '1')
            gd = img_paste(block)
            result = tesserocr.image_to_text(gd,lang="eng")
            if len(result) != 0:
                try:
                    num = int(result[0])
                    nums[j].append(-num)
                except:
                    print(f'{i}排{j}列数字识别失败，填充为0')
                    nums[j].append(0)
            else:
                nums[j].append(0)
    return nums

def data_update(initial_list):
    '''
    修改识别出来的数据
    '''
    while True:
        message = input('输入几排几列更新后的数据，空格隔开:\n如修改第一排第二列数字为5  输入：1 2 5)')
        # try:
        message_ls = message.split(' ')
        print(message_ls)
        initial_list[int(message_ls[0]) - 1][int(message_ls[1] )- 1] = -int(message_ls[2])
        print('更新成功')
        # except:
        #     print('输入错误')
        flag = input('是否继续修改，Y/N')
        if flag in ['N', 'n']:
            return initial_list

if __name__ == '__main__':
    img = Image.open("demo.png")
    # img = cut_img()
    # initial_list = img_block(img)
    initial_list = [[-4, 0, 0, 0, 0, -9, 0, 0, -6], [-5, 0, 0, 0, 0, 0, -4, 0, 0], [0, 0, 0, -7, -1, 0, 0, 0, 0], [0, -7, 0, -8, 0, -3, 0, 0, -9], [-6, 0, -8, 0, -4, 0, 0, -3, 0], [0, -4, 0, -9, 0, -6, 0, 0, -5], [0, 0, 0, -2, -6, 0, 0, 0, 0], [-7, 0, 0, 0, 0, 0, -3, 0, 0], [-2, 0, 0, 0, 0, -8, 0, 0, -1]]
    print(initial_list)
    print('识别结果为：')
    decode.show(initial_list)
    pass_update = input('是否需要修改数据Y/N')
    if pass_update in ['Y', 'y']:
        initial_list = data_update(initial_list)
        print('修改后结果为：')
        decode.show(initial_list)
    print('参考结果为：')
    decode.start(initial_list)





