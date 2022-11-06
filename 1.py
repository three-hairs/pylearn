import time


class Test(object):
    def __init__(self,name):
        self.name = name
        self.age = 0
        self.tall = 180

    def __str__(self):
        return self.name+'age: '+str(self.age)



def show() -> None:
    """
    打印
    dskajd
    :return:
    """
    print('hei')


def time_compare() -> None:
    """
    dsadad
    :return:
    """
    N = 10000000

    t1 = time()

    arr = []
    for i in range(N):
        arr.append(i ** 2)

    t2 = time()

    arr1 = [i ** 2 for i in range(N)]

    t3 = time()
    print(t2 - t1, t3 - t2)


def func() -> ...:
    ...


def pro_count() -> None:
    """
    程序运行进图条
    :return: None
    """

    scale = 50

    print("执行开始".center(scale // 2, "-"))  # .center() 控制输出的样式，宽度为 25//2，即 22，汉字居中，两侧填充 -

    start = time.perf_counter()  # 调用一次 perf_counter()，从计算机系统里随机选一个时间点A，计算其距离当前时间点B1有多少秒。
    for i in range(scale + 1):
        a = '*' * i  # i 个长度的 * 符号
        b = '.' * (scale - i)  # scale-i） 个长度的 . 符号。符号 * 和 . 总长度为50
        c = (i / scale) * 100  # 显示当前进度，百分之多少
        dur = time.perf_counter() - start  # 计时，计算进度条走到某一百分比的用时
        print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, dur), end='')
        # \r用来在每次输出完成后，将光标移至行首，这样保证进度条始终在同一行输出，即在一行不断刷新的效果；{:^3.0f}，输出格式为居中，占3位，小数点后0位，浮点型数，对应输出的数为c；{}，对应输出的数为a；{
        # }，对应输出的数为b；{:.2f}，输出有两位小数的浮点数，对应输出的数为dur；end=''，用来保证不换行，不加这句默认换行。
        time.sleep(0.1)  # 在输出下一个百分之几的进度前，停止0.1秒  否则程序执行太快无法看清进度条变化
    print("\n" + "执行结果".center(scale // 2, '-'))


print('*'.join([str(i + 1) for i in range(10)]))


if __name__ == '__main__':
    # help(show)
    ai = Test('lll')
    print(ai)

