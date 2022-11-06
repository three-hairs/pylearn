import csv
import os
import numpy as np
import re
import time
import scipy.io
import math
import pandas as pd

csv.field_size_limit(2 ** 31 - 1)


def progress_bar(finish_tasks_number, tasks_number, complete_time):
    """
    进度条
    :param finish_tasks_number: int, 已完成的任务数
    :param tasks_number: int, 总的任务数
    :param complete_time: float, 已完成的任务所消耗的总时间
    :return:
    """

    percentage = round(finish_tasks_number / tasks_number * 100)
    finished_label = "▓" * (percentage // 2)
    unfinished_label = "-" * (100 - percentage)
    arrow = "->"
    if not finished_label or not unfinished_label:
        arrow = ""
    print("\r{}% [{}{}{}] {:.2f}s".format(percentage, finished_label, arrow, unfinished_label, complete_time), end="")


def filecompare():
    fdir = r'C:\Users\Lenovo\Desktop\新建文件夹'
    flist = os.listdir(fdir)

    file2 = r'C:\Users\Lenovo\Desktop\PID2932.csv'
    print(flist)
    data = []
    data2 = []
    for file in flist:
        path = os.path.join(fdir, file)
        with open(path) as f:
            reader = csv.reader(f)
            data_row = next(reader)
            data_row = next(reader)
            data.append(data_row[4])

    with open(file2) as f2:
        reader = csv.reader(f2)
        data_row = next(reader)
        data_row = next(reader)
        data2.append(data_row[4])

    print(data)
    print(data2)


def find_miss(filename: str):
    """
    查找csv文件缺失的序号id
    :param filename:
    :return: none
    """
    with open(filename) as f:
        reader = csv.reader(f)
        data = next(reader)
        miss = []
        i = 1
        for row in reader:
            if i != int(row[2]):
                print(row[2])
                miss.append(i)
                i = int(row[2])
            i += 1
        print(miss)


def find_miss_fileid(fdir: str):
    """
    按照文件序号 查找缺失文件pid
    :param fdir:
    :return:
    """
    missid = []
    missfile = []
    flist = os.listdir(fdir)
    for i in range(1956, 2015):
        pid = 'PID' + str(i) + 'subPID'
        sublist = [subid for subid in flist if pid in subid]
        if 121 > len(sublist) > 0:
            missid.append(pid + ':' + str(121 - len(sublist)))
        elif len(sublist) == 0:
            missfile.append(i)

    print('lost subpid', missid)
    print('lost pid', missfile)


def file_del(fdir: str):
    flist = os.listdir(fdir)
    for file in flist:
        if '(1)' in file:
            try:
                path = os.path.join(fdir, file)
                os.remove(path)  # 这个可以删除单个文件，不能删除文件夹
                print(file, ' removed')
            except BaseException as e:
                print(e)


def file_merge():
    """
    拼接csv 时间序列数据; 拼接两个文件夹的csv
    :return:
    """
    header = []
    dirs = [r'C:\Users\dell\Desktop\cold\1', r'C:\Users\dell\Desktop\cold\2', r'C:\Users\dell\Desktop\cold\3',
            r'C:\Users\dell\Desktop\cold\4']

    dir_save = r'C:\Users\dell\Desktop\cold'

    flist = os.listdir(dirs[0])
    print(len(flist))
    for file in flist:
        print(file)
        data = []
        save_file = os.path.join(dir_save, file)
        if not os.path.isfile(save_file):
            for dir in dirs:
                path = os.path.join(dir, file)
                with open(path) as f1:
                    reader = csv.reader(f1)
                    data1 = next(reader)
                    header = data1
                    for da in reader:
                        data.append(da)

            with open(save_file, 'w+', newline='') as f2:
                writer = csv.writer(f2)
                writer.writerow(header)
                writer.writerows(data)


def find(fdir):
    lost = []
    flist = os.listdir(fdir)
    for i in range(1, 3908):
        pid = "{:04d}".format(i)
        name = 'PID' + pid + '.mat'
        if name in flist:
            continue
        else:
            lost.append(pid)
    print(lost, len(lost))


def split_csv():
    """
    fenge csv 时间序列数据;
    :return:
    """
    dir = r'C:\Users\dell\Desktop\cold\PID2.csv'
    save_file = r'C:\Users\Lenovo\Desktop\1.csv'
    save_dir = r'C:\Users\dell\Desktop'
    with open(dir) as f1:
        reader = csv.reader(f1)
        # data1 = next(reader)
        # header = data1
        print(reader)
        data = [da for da in reader]
    array = np.array(data)
    sp_array = np.split(array, 4, axis=1)
    for i, arr in enumerate(sp_array):
        with open(save_dir+str(i)+'.csv', 'w', newline='') as f2:
            writer = csv.writer(f2)
            # writer.writerow(header)
            writer.writerows(arr.tolist())

    # if not os.path.isfile(save_file):
    #     with open(dir) as f1:
    #         reader = csv.reader(f1)
    #
    #         data1 = next(reader)
    #         header = data1
    #         for index, da in enumerate(reader):
    #             # if index < 10:
    #             data.append(da)
    #         print(len(data))
    #         array1 = np.array(data)
    #         print(array1)
            # else:
            #     break


def csv_to_mat():
    """
    :return:
    """
    dir = r'D:\poly_r150_seg4\PID5.csv'
    save_file = r'C:\Users\Lenovo\Desktop\PID5-004.csv'

    pixels = int(math.pow(301, 2))  # radius
    pid = re.findall(r'(PID\d.csv)', dir)  # select pid
    pid = int(pid[0].replace('PID', '').replace('.csv', ''))
    print('PID :', pid)
    with open(dir) as f1:
        reader = csv.reader(f1)
        data1 = next(reader)
        header = data1
        print(header)
        if len(header) < 14:
            print('header columns miss')
            exit(1)
        columns = 13
        data = [da[1:14] for da in reader]

    rows = len(data)
    print(rows, 'rows data')
    ori_arr = np.zeros((rows * 90601, columns + 2))
    ori_arr[:, [0]] = pid
    start = time.perf_counter()
    for row, da in enumerate(data):
        duration = time.perf_counter() - start
        progress_bar(row, rows, duration)
        for col, item in enumerate(da):
            if 2 < col < 12:
                temp = re.findall(r'\-?\d+\.?\d*', item)  # split data
                len1 = len(temp)
                # print(len1)
                if len1 == pixels:
                    data_arr = np.matrix(temp).reshape((len1, 1))
                    ori_arr[row * len1: (row + 1) * len1, [col + 2]] = data_arr  # ref qa lonlat data
                    # subPID
                    ori_arr[row * len1: (row + 1) * len1, [1]] = np.matrix(range(1, len1 + 1)).reshape((len1, 1))
                elif len1 == 0:
                    ori_arr[row * len1: (row + 1) * len1, [col + 2]] = 0
                    ori_arr[row * len1: (row + 1) * len1, [1]] = np.matrix(range(1, len1 + 1)).reshape((len1, 1))
            else:
                try:
                    date = int(item)
                    ori_arr[row * pixels: (row + 1) * pixels, [col + 2]] = date  # yy-mm-dd  landsat
                except:
                    ori_arr[row * pixels: (row + 1) * pixels, [col + 2]] = 0
    # print(ori_arr)
    print('\nwriting')
    data2 = pd.DataFrame(ori_arr)
    data2.to_csv(save_file, index=False, header=False)
    print('success')


def test():
    A = np.arange(12).reshape((3, 4))

    print('打印矩阵A:')

    print(A)

    print('\n水平分割为两块:')

    print(np.split(A, 2, axis=1))  # 表示对A进行分割，分为两块，axis=1为水平分割

    print('\n垂直分割为3块:')

    print(np.vsplit(A, 3)[1])  # 不均等分割

    print('\n垂直不均等分割:')

    print(np.array_split(A, 2, axis=0))


if __name__ == '__main__':
    # dir = r'E:\refmat'
    csv_to_mat()
