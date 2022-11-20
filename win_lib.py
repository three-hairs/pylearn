import pyautogui as gui
import win32gui
from PyQt5.QtWidgets import QApplication
from aip import AipOcr
import sys
from paddleocr import PaddleOCR, draw_ocr
import cv2
import time
import random
import numpy as np
import win32con
import win32com.client

hwnd_title = {}


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


def return_hwnd(name: str) -> tuple:
    """
    返回目标窗体名称 + 定位rect
    :param name: name window to search
    :return: list[0] rect of window ; list[1] tittle to search
    """
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t:
            # print(h, t)
            if name in t:
                # left, top, right, bottom = win32gui.GetWindowRect(h)
                return win32gui.GetWindowRect(h), t
                # print(left, top, right, bottom)

    return 0, 0


# region截屏
def r_screen_cut(pos: list, name: str, hwnd='') -> str:
    """
    region_screen_cut and save img
    :param hwnd:
    :param pos: rect of region
    :param name: path of img
    :return: path of img
    """
    if hwnd == '':
        img1 = gui.screenshot(region=pos)  # rect:[x,y,w,h]
        img1.save(name + '.jpg')
        return name + '.jpg'  # img path
    else:
        win32gui.EnumWindows(get_all_hwnd, 0)
        hwnd = win32gui.FindWindow(None, hwnd)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
        img1 = gui.screenshot(region=pos)  # rect:[x,y,w,h]
        img1.save(name + '.jpg')
        return name + '.jpg'  # img path


# handle截屏
def h_screen_cut(name: str, file: str) -> str:
    """
    handle_screen_cut and save img
    :param file: path of save
    :param name: name of handle
    :return: path of img
    """
    win32gui.EnumWindows(get_all_hwnd, 0)
    hwnd = win32gui.FindWindow(None, name)
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    # img = convertQImageToMat(img)  # 将获取的图像从QImage转换为RBG格式
    # cv2.imshow("asd", img)  # imshow
    # cv2.waitKey(0)
    img.save(file + '.jpg')
    return file + '.jpg'  # img path


# 文字识别（精确）
def ocr_accurate(imgpath):
    APP_ID = '26893179'
    API_KEY = 'bBlTHVLNwNT1aFFmhLZCzA71'
    SECRET_KEY = 'enHiY18ozOfVAke1qBtettph0eG8LYBI'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    with open(imgpath, 'rb') as fp:
        image = fp.read()

    text = client.basicAccurate(image)
    res = ''
    for word in text['words_result']:
        res += word['words'].replace(' ', '')
    return res


# paddle文字识别 + 定位
def paddle_ocr(file: str) -> list:
    """
    :param file: path of img to recog
    :return:list[0] :[four pnts coors]; list[1] [words and prob]
    """
    ret = []
    pos_list = []
    ocr = PaddleOCR(use_angle_cls=False, use_gpu=True)
    result = ocr.ocr(file, cls=False)
    return result
    # for line in result:
    #     line[0][0] +
    #     print(line)


# 图像识别定位
def image_locate(screenpath: str, templatepath: str) -> tuple:
    """
    !!! path no Chinese !!!
    :param screenpath: screen cut path
    :param templatepath: template img path
    :return: ret of match : pos[x,y] or -1,-1
    """
    screen = cv2.imread(screenpath)
    template = cv2.imread(templatepath)
    image_x, image_y = template.shape[:2]
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # print("prob:", max_val)
    if max_val > 0.9:
        center = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
        print(center)
        return center
    else:
        return -1, -1


# 点击函数
def click1(x: float, y: float, sleep: float = 0.5, delt_x=0, delt_y=0):
    """
    :param delt_y:
    :param delt_x:
    :param x: click x pos
    :param y: click y pos
    :param sleep: sleep time (second)
    :return: none
    """
    # random click
    dt = random.uniform(0.2, 1)
    dx = random.randint(-5, 5)
    dy = random.randint(-4, 4)
    gui.click(x + dx + delt_x, y + dy + delt_y, interval=dt, button='left')
    time.sleep(sleep)


# 点击函数(2)
def click2(x_y: list, sleep: float = 0.5):
    """
    :param sleep: sleep time(second)
    :param x_y: list of pos click
    :return: none
    """
    # random click
    dt = random.uniform(0.2, 1)
    dx = random.randint(-5, 5)
    dy = random.randint(-4, 4)
    gui.click(x_y[0] + dx, x_y[1] + dy, interval=dt, button='left')
    time.sleep(sleep)


# 拖动 !!! 暂定
def drag(x=770, y=650):
    ...
    dy = 380
    x = 770
    y = 650
    gui.moveTo(x, y)
    gui.dragTo(x, y - dy, duration=1)
    time.sleep(0.5)


def convertQImageToMat(incomingImage):
    '''  Converts a QImage into an opencv MAT format  '''
    # Format_RGB32 = 4,存入格式为B,G,R,A 对应 0,1,2,3
    # RGB32图像每个像素用32比特位表示，占4个字节，
    # R，G，B分量分别用8个bit表示，存储顺序为B，G，R，最后8个字节保留
    incomingImage = incomingImage.convertToFormat(4)
    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.bits()
    ptr.setsize(incomingImage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
    # arr为BGRA，4通道图片
    return arr


if __name__ == '__main__':

    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t:
            print(h, t)
            if True:
                left, top, right, bottom = win32gui.GetWindowRect(h)
                print(win32gui.GetWindowRect(h), t)
                # print(t)
                # print(left, top, right, bottom)
                # gui.click(right-206,bottom-31)
