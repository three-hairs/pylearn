import pyautogui as gui
import os
from PyQt5.QtWidgets import QApplication
import time
import sys
import random
from aip import AipOcr
import win32gui
import cv2
import re
from paddleocr import PaddleOCR, draw_ocr
import re


def paddle_ocr(file: str) -> list:
    ret = []
    pos_list = []
    ocr = PaddleOCR(use_angle_cls=False, use_gpu=True)
    result = ocr.ocr(file, cls=False)
    return result
    # for line in result:
    #     line[0][0] +
    #     print(line)


hwnd_title = dict()
path = os.path.split(os.path.realpath(__file__))[0]
temppath = path + '/temp/'
respath = path + '/res/'


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


def get_window_pos() -> tuple or list:
    hwnd = win32gui.FindWindow(None, '坚持走中国特色国家安全道路 - Google Chrome')
    if hwnd == '':
        return -1, -1, '定位失败， 请打开窗口'
    rect = win32gui.GetWindowRect(hwnd)
    x0 = rect[0]
    y0 = rect[1]
    # w = rect[2] - x0
    # h = rect[3] - y0
    print("定位成功！！ Window %s :" % win32gui.GetWindowText(hwnd))
    print("\tLocation: (%d, %d)" % (x0, y0))
    # print("\t    Size: (%d, %d)" % (w, h))
    return rect


# 截屏
def screen_cut(pos: list, name) -> str:
    win32gui.EnumWindows(get_all_hwnd, 0)
    # hwnd = win32gui.FindWindow(None, '总体国家安全观 - Google Chrome')
    # app = QApplication(sys.argv)
    img1 = gui.screenshot(region=pos)  # x,y,w,h
    img1.save(path + '/temp/' + name + '.jpg')
    screen = QApplication.primaryScreen()
    # img = screen.grabWindow(hwnd).toImage()
    # img.save(path + '/temp/' + name + '.jpg')
    return temppath + name + '.jpg'


# 文字识别（精确）
def ocr_accurate(imgpath):
    APP_ID = '26893179'
    API_KEY = 'bBlTHVLNwNT1aFFmhLZCzA71'
    SECRET_KEY = 'enHiY18ozOfVAke1qBtettph0eG8LYBI'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    with open(imgpath, 'rb') as fp:
        image = fp.read()

    # options["language_type"] = "CHN_ENG"
    # options["detect_direction"] = "true"
    # options["detect_language"] = "true"
    # options["probability"] = "true"
    text = client.basicAccurate(image)
    res = ''
    for word in text['words_result']:
        res += word['words'].replace(' ', '')
    return text


# 读取文件 文字识别（tongyong）包含位置
def ocr_general(filePath):
    APP_ID = '26893179'
    API_KEY = 'bBlTHVLNwNT1aFFmhLZCzA71'
    SECRET_KEY = 'enHiY18ozOfVAke1qBtettph0eG8LYBI'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    with open(filePath, "rb") as fp:
        image = fp.read()

    # 调用通用文字识别（标准含位置信息版）
    res_image = client.general(image)

    # 如果有可选参数
    options = {}

    res_image = client.general(image, options)
    res = []
    for word in res_image['words_result']:
        pos_list = word['location']
        data = {'words': word['words'].replace(' ', ''), 'pos': [value[1] for value in pos_list.items()]}
        res.append(data)
    # print(res_image['words_result'])
    return res


# 点击函数(2)
def click(x_y: list) -> None:
    dt = random.uniform(0.2, 1)
    # dx = x_y[0] + x_y[3]/2
    # dy = x_y[1] + x_y[2]/2
    gui.click(x_y[0]-9, x_y[1]-9, interval=dt, button='left')
    time.sleep(5)

text = [{'words': '签pythons字共×图pythons中×|百度智能云×)文字识别oX)百度智能云×西ModuleNo×|图Python提元×',
         'location': {'top': 14, 'left': 29, 'width': 1107, 'height': 29}},
        {'words': 'Python:之c×CPython-×', 'location': {'top': 15, 'left': 1130, 'width': 317, 'height': 29}},
        {'words': '⑤总体国家安×', 'location': {'top': 18, 'left': 1446, 'width': 137, 'height': 22}}, {
            'words': '>eweiban.mycourse.cn/#/course/list?projectType=pre&subjectType=3&categoryCode=101001002&proje'
                     'ctld=563c75dd-49e8-4aab-baac-347d191f5295&categoryName=...',
            'location': {'top': 59, 'left': 24, 'width': 1852, 'height': 26}},
        {'words': '鱼首页白哔哩哔哩(·.)p.HDArea百度网盘全部文件目学习目工作目工具目电影目happy',
         'location': {'top': 99, 'left': 24, 'width': 950, 'height': 28}},
        {'words': '坚持走中国特色国家安全道路', 'location': {'top': 169, 'left': 811, 'width': 257, 'height': 19}},
        {'words': '凸52957', 'location': {'top': 208, 'left': 1124, 'width': 72, 'height': 30}},
        {'words': '《国家安全法》之你应该知道的', 'location': {'top': 275, 'left': 819, 'width': 271, 'height': 24}},
        {'words': '凸40857', 'location': {'top': 316, 'left': 1121, 'width': 77, 'height': 34}},
        {'words': '国家安全与总体国家安全观', 'location': {'top': 383, 'left': 811, 'width': 241, 'height': 24}},
        {'words': '院感', 'location': {'top': 362, 'left': 1169, 'width': 72, 'height': 49}},
        {'words': '凸94429', 'location': {'top': 425, 'left': 1122, 'width': 76, 'height': 31}},
        {'words': '可', 'location': {'top': 964, 'left': 769, 'width': 40, 'height': 42}},
        {'words': '②', 'location': {'top': 964, 'left': 942, 'width': 50, 'height': 45}},
        {'words': '首页', 'location': {'top': 1006, 'left': 771, 'width': 38, 'height': 24}},
        {'words': '在线课服', 'location': {'top': 1008, 'left': 932, 'width': 72, 'height': 24}},
        {'words': '我的', 'location': {'top': 1010, 'left': 1129, 'width': 34, 'height': 19}}]

# 获取所有句柄
win32gui.EnumWindows(get_all_hwnd, 0)

for h, t in hwnd_title.items():
    if t:
        print(h, t)
        if 'Edge' in t:
            a = win32gui.GetWindowRect(h)
            print(t)
            break
            # gui.click(right-206,bottom-31)


# b = screen_cut(a, 'ddd')
# c = paddle_ocr(b)
# print(c)
while True:
    # click([949, 1146, 87, 29])
    # click([949, 1046, 87, 29])
    img = screen_cut(a, 'ddd')
    res = paddle_ocr(img)
    print(res)
    word = ''
    judge = []
    for item in res:
        if '下一页' in item[1][0]:
            word = item[1][0]
            pos = [(item[0][0][0] + item[0][2][0]) / 2, (item[0][0][1] + item[0][2][1]) / 2]
            print(word, pos)
            click(pos)
        elif item[1][0] == '继续':
            pos = [(item[0][0][0] + item[0][2][0]) / 2, (item[0][0][1] + item[0][2][1]) / 2]
            print(word, pos)
            click(pos)
        elif item[1][0] == '确定':
            word = item[1][0]
            pos = [(item[0][0][0] + item[0][2][0]) / 2, (item[0][0][1] + item[0][2][1]) / 2]
            print(word, pos)
            click(pos)
        elif item[1][0] == '返回课程列表':
            word = item[1][0]
            pos = [(item[0][0][0] + item[0][2][0]) / 2, (item[0][0][1] + item[0][2][1]) / 2]
            print(word, pos)
            click(pos)
        elif '点击继续' in item[1][0]:
            word = item[1][0]
            pos = [(item[0][0][0] + item[0][2][0]) / 2, (item[0][0][1] + item[0][2][1]) / 2]
            print(word, pos)
            click(pos)
        elif '开始' in item[1][0] or '开始学习' in item[1][0] or '点击开始' in item[1][0] or '击学习' in item[1][0] or '进入' in item[1][0]:
            word = item[1][0]
            pos = [(item[0][0][0] + item[0][2][0]) / 2, (item[0][0][1] + item[0][2][1]) / 2]
            print(word, pos)
            click(pos)
        elif re.match(r'\d{5}', item[1][0]):
            te = item[1][0]
            if te in judge:
                continue
            else:
                judge.append(te)
                word = item[1][0]
                pos = [(item[0][0][0] + item[0][2][0]) / 2 - 50, (item[0][0][1] + item[0][2][1]) / 2]
                print(word, pos)
                click(pos)
                break
        else:
            continue
    if word == '':
        break







