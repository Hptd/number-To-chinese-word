import re  # 导入正则表达式模块
import tkinter as tk  # 导入tkinter模块
import tkinter.messagebox as msg  # 导入tkinter模块的messagebox子模块

# 不超过 1 0000 0000 0000 0000     &&     小数不超过2位
dict_ref = {'1': "壹", '2': "贰", '3': "叁", '4': "肆", '5': "伍", '6': "陆", '7': "柒", '8': "捌", '9': "玖", '0': "零"}  # 定义字典
list_ref = ['圆', '万', '亿', '兆']  # 定义一个列表


def input_to_txt_text(input_num):
    input_num = input_num.get()  # 获取输入框的值
    # 将结果打印在 text_result 中
    text_result.insert('insert', input_num + '\n')

def four_split(number):  # 拆分函数，将整数字符串拆分成[亿，万，仟]的list
    remainder = len(number) % 4  # 对4取余
    number_split = []  # 定义一个空列表存放拆分后的结果
    remaining_numbers_length = len(number) - 1  # 把数字的长度-1后赋给remaining_numbers_length
    if remainder > 0:  # 如果余数大于0
        number_split.append(number[0:remainder])  # 先把余数个数字拆分为一组
    k = remainder  # 把余数赋给k
    while k <= remaining_numbers_length:  # 遍历余下的数字
        number_split.append(number[k:k + 4])  # 在已拆分的余数个数字后面按4位拆分
        k += 4  # 每拆分一次，k值加上4
    return number_split  # 以列表形式返回拆分后的结果


def exchange(data):  # 在四位以下的数字切片中插入单位
    string = ['拾', '佰', '仟']  # 定义储存['拾', '佰', '仟']这些单位标识的列表
    words = ''  # 定义字符串
    length = len(data)  # 获取要转换的数字长度
    for e in range(length):  # 遍历数字
        words += dict_ref[data[e]]  # 全部转换为大写数字
    data_list = list(words)  # 把转换后的数字以列表形式返回给data_list
    for x in range(length - 1):  # 遍历数字
        data_list.insert(-(2 * x + 1), string[x])  # 把['拾', '佰', '仟']这些单位插入列表中
        data = ''.join(data_list)  # 转换为大写数字后连接到data字符串
    if length == 1:  # 如果数字长度为1
        data = ''.join(data_list)  # 转换为大写数字后连接到data字符串
    for y in ['零仟', '零佰', '零拾', '零零零', '零零']:  # 下面开始查找并处理含有['零仟', '零佰', '零拾', '零零零', '零零']的情况
        k = data.find(y)  # 如果data包含y字符串返回开始的索引值，否则返回-1。
        if k != -1:  # 如果data中含有y字符串
            data = re.sub(y, '零', data)  # data里面所有的y被零替换
    if data[-1] == '零':  # 如果data的末尾是“零”
        data = data[:-1]  # 把后面的零去掉
    else:  # 如果data的末尾不是“零”
        data = data  # 不变
    return data  # 返回处理后的值（字符串）

def change(input_number):
    # input_number = input("请输入不超过一万兆的金额，小数不超过3位：")  # 输入数字
    if input_number == '':  # 如果输入为空
        msg.showinfo(title='提示', message='输入不能为空！')  # 弹出提示框
    elif input_number == '0' or input_number == '0.0' or input_number == "0.00" or input_number == "0.000":  # 如果输入为0
        msg.showinfo(title='提示', message='输入不能为0！')  # 弹出提示框
    elif float(input_number) < 0:
        msg.showinfo(title='提示', message='输入不能为负数！')  # 弹出提示框

    if input_number.replace(".", '').isdigit() and input_number == input_number.strip(
            "."):  # 不能输入负数，小数点可以有0或1个，如果有小数点，小数点的前后要有数字
        if input_number.count(".") == 1:  # 如果输入的数字带有一个小数点（非整数），则执行下面语句
            input_number_split = input_number.split('.')  # 以.为分隔符对输入的字符串进行切片
            int_number = input_number_split[0]  # 整数部分
            dec_number = input_number_split[1]  # 小数部分
            int_number_split = four_split(int_number)  # 把整数部分按4位数字进行切分，返回值赋给int_number_split
            count = [len(x) for x in input_number_split]  # 计算以小数点为分隔符分割后的整数部分的数字个数和小数部分的数字个数
            # print(count, type(dec_number[0]), dec_number[1])  # 可输出查看结果
            if count[0] <= 16 and count[1] <= 3:  # 如果输入的数字不超过 1 0000 0000 0000 0000 并且小数不超过3位
                word = ''  # 定义字符串
                for i in range(len(int_number_split)):  # 处理整数部分
                    word += exchange(int_number_split[i]) + list_ref[
                        len(int_number_split) - i - 1]  # 遍历转化时把['圆', '万', '亿', '兆']的单位标识添加

                last_word = ''  # 定义字符串

                # if count[1] == 0:  # 处理小数部分，此处判断小数部分数字个数为0时
                #     last_word = '整'

                if count[1] == 1:  # 处理小数部分，此处判断小数部分数字个数刚好为1位时
                    if dec_number != "0":
                        last_word = dict_ref[dec_number[0]] + '角整'  # 转换小数部分数字，末尾添加“角整”
                    elif dec_number == "0":
                        last_word = '整'

                elif count[1] == 2:  # 处理小数部分，此处判断小数部分数字个数刚好为2位时
                    if dec_number[1] != "0" and dec_number[0] == "0":  # 如果角位为0，则不用读取角位
                        last_word = dict_ref[dec_number[1]] + '分'  # 转换小数部分数字，末尾添加“分整”
                    elif dec_number[0] != "0" and dec_number[1] == "0":  # 如果分位为0，则不用读取分位
                        last_word = dict_ref[dec_number[0]] + '角整'  # 转换小数部分数字，末尾添加“角整”
                    elif dec_number[0] != "0" and dec_number[1] != "0":  # 如果角位和分位都不为0
                        last_word = dict_ref[dec_number[0]] + '角' + dict_ref[dec_number[1]] + '分'
                    elif dec_number[0] == "0" and dec_number[1] == "0":
                        last_word = '整'

                elif count[1] == 3:  # 处理小数部分，此处判断小数部分数字个数刚好为3位时
                    if dec_number[2] != "0" and dec_number[1] == '0' and dec_number[0] == '0':  # 如果厘位，分位和角位都为0，则不用读取小数部分
                        last_word = dict_ref[dec_number[2]] + '厘'
                    elif dec_number[1] != "0" and dec_number[2] == "0" and dec_number[0] == '0':  # 如果厘位和角位为0，则不用读取厘位和角位
                        last_word = dict_ref[dec_number[1]] + '分'  # 转换小数部分数字，末尾添加“分整”
                    elif dec_number[0] != "0" and dec_number[2] == "0" and dec_number[1] == '0':  # 如果厘位和分位为0，则不用读取厘位和分位
                        last_word = dict_ref[dec_number[0]] + '角整'  # 转换小数部分数字，末尾添加“角整”
                    elif dec_number[2] == "0" and dec_number[1] != '0' and dec_number[0] != "0":  # 如果厘位为0，分位和角位不为0，需要读取分位和角位
                        last_word = dict_ref[dec_number[0]] + '角' + dict_ref[dec_number[1]] + '分'  # 转换小数部分数字，添加“角”，“分”，末尾添加“厘”
                    elif dec_number[1] == "0" and dec_number[2] != "0" and dec_number[0] != "0":  # 如果分位为0，厘位和角位不为0，需要读取厘位和角位
                        last_word = dict_ref[dec_number[0]] + '角' + dict_ref[dec_number[2]] + '厘'  # 转换小数部分数字，添加“角”，“分”，末尾添加“厘”
                    elif dec_number[0] == "0" and dec_number[1] != "0" and dec_number[2] != "0":  # 如果角位为0，厘位和分位不为0，需要读取厘位和分位
                        last_word = dict_ref[dec_number[1]] + '分' + dict_ref[dec_number[2]] + '厘'  # 转换小数部分数字，添加“角”，“分”，末尾添加“厘”
                    elif dec_number[2] != "0" and dec_number[1] != "0" and dec_number[0] != "0":  # 如果厘位，分位和角位都不为0，需要读取厘位，分位和角位
                        last_word = dict_ref[dec_number[0]] + '角' + dict_ref[dec_number[1]] + '分' + dict_ref[dec_number[2]] + '厘'  # 转换小数部分数字，添加“角”，“分”，末尾添加“厘”
                    elif dec_number[2] == dec_number[1] == dec_number[0] == "0":  # 如果厘位，分位和角位都为0，则不用读取小数部分
                        last_word = '整'

                word += last_word  # 把整数部分和小数部分处理后的结果拼接
                # print(word)  # 输出转换后的结果
                text_result.delete(0.0, 'end')  # 清空文本框
                text_result.insert('insert', word)  # 把转换后的结果显示在文本框中

            else:  # 如果用户输入不规范（超出提示输入范围）
                # continue  # 提示用户重新输入
                msg.showerror(title='错误', message='输入数字超出范围，请重新输入！')
        elif input_number.count(".") == 0:  # 如果输入的数字没有小数点（整数），则执行下面语句
            if int(input_number) <= 10000000000000000:  # 判断该整数是否符合输入规范
                word = ''  # 定义字符串
                int_number_split = four_split(input_number)  # 把输入的数字按4位数字进行切分，返回值赋给int_number_split
                for i in range(len(int_number_split)):  # 进入转换
                    word += exchange(int_number_split[i]) + list_ref[
                        len(int_number_split) - i - 1]  # 遍历转化时把['圆', '万', '亿', '兆']的单位标识添加
                    # word = re.sub('圆', '整', word)  # 方法一
                word = word + '整'  # 最后把“整”拼接进去
                if "亿万圆" in word:  # 如果转换后的结果含有“亿万圆”
                    word = word.replace('亿万圆', '')  # 方法二  删除“亿万圆”
                # print(word)  # 输出转换后的结果
                text_result.delete(0.0, 'end')  # 清空文本框
                text_result.insert('insert', word)  # 把转换后的结果显示在文本框中
            else:  # 如果用户输入不规范（超出提示输入范围）
                # continue  # 提示用户重新输入
                msg.showerror(title='错误', message='输入数字超出范围，请重新输入！')

root = tk.Tk()  # 创建一个Tkinter.Tk()实例
root.title("数字转换")  # 设置窗口标题
root.geometry("400x200")  # 设置窗口大小
root.resizable(width=False, height=False)  # 设置窗口大小不可变

lable = tk.Label(root, text="请输入不超过一万兆的金额，小数不超过3位：")  # 创建一个标签
lable.pack()

# 创建一个输入框,并设置尺寸
input_num = tk.Entry(root, width=30)
# 激活输入框
input_num.pack()


text_result = tk.Text(root, width=50, height=8)  # 创建一个文本框用于显示转换结果
text_result.pack()

# 创建一个按钮
# button = tk.Button(root, text="转换", command=lambda: change(input_num.get()))
button = tk.Button(root, text="转换", width=40, height=2, bg="gray", command=lambda: change(input_num.get()))

# 将按钮绑定回车键盘
root.bind('<Return>', lambda event: change(input_num.get()))
button.pack()


root.mainloop()
