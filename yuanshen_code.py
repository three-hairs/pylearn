import time

from win_lib import *
import re
import pyautogui as gui
import pyperclip
# run by administrator ！！

template = r'temp/'
enter = 'enter.png'
input = 'input.png'
click = 'exchange.png'
changed = 'ischanged.png'
success = 'changesuccess.png'
suc_conf = 'confirm.png'
clear = 'clear.png'
invalid = 'invalid.png'


def change(ex_code: list):
    win = return_hwnd('原神')
    print(win)
    for code in ex_code:
        scr = r_screen_cut(win[0], 'ccc', hwnd=win[1])
        print(template + enter)
        x0, y0 = image_locate(scr, template + enter)
        if x0 != -1 and y0 != -1:
            print(enter + 'locate success', x0, y0)
            click1(x0, y0, 0, delt_x=win[0][0])
            scr = r_screen_cut(win[0], 'ccc', hwnd=win[1])
        x1, y1 = image_locate(scr, template + input)
        if x1 != -1 and y1 != -1:
            print(input + 'locate success', x1, y1)
            click1(x1, y1, 0, delt_x=win[0][0])
            pyperclip.copy(code)
            gui.hotkey('Ctrl', 'v')
            scr = r_screen_cut(win[0], 'ccc', hwnd=win[1])
            # gui.write('7swvfftkbzx2', interval=0)
        x, y = image_locate(scr, template + click)
        if x != -1 and y != -1:
            print(click + 'locate success', x, y)
            click1(x, y, 0, delt_x=win[0][0])
            click1(x0, y0, 0, delt_x=win[0][0])
            gui.moveTo(x0 + 50, y0 + 50)

            # scr = r_screen_cut(win[0], 'ccc', hwnd=win[1])
        # x, y = image_locate(scr, template + changed)
        # x1, y1 = image_locate(scr, template + clear)
        x2, y2 = image_locate(scr, template + success)
        x3, y3 = image_locate(scr, template + suc_conf)
        if x2 != -1 and y2 != -1:
            print(success + '  locate success', x, y)
            print('兑换成功')
            click1(x3, y3, 0, delt_x=win[0][0])
            click1(x0, y0, 0, delt_x=win[0][0])
            gui.moveTo(x0 + 50, y0 + 50)
        else:
            click1(x0, y0, 0, delt_x=win[0][0])
            gui.moveTo(x0 + 50, y0 + 50)
        #     print(changed + 'locate success', x, y)
        #     click1(x1, y1, 0, delt_x=win[0][0])
        #     print('已被兑换')
        #     return x, y
        # elif x2 != -1 and y2 != -1:
        #     print(success + 'locate success', x, y)
        #     print('兑换成功')
        #     click1(x3, y3, 0.5, delt_x=win[0][0])
        #     scr = r_screen_cut(win[0], 'ccc', hwnd=win[1])


code = return_hwnd('深渊')
# print(code)
# c = r_screen_cut(code[0], '00', hwnd=code[1])


hd = '<斗鱼哇活动礼包其他礼包选择活动《原神》2.8版本直播季2.8萌新直播间观看时长10min_摩拉2022-07-2812:20:45《原神》2.8版本直播季2.8萌新直播间观看时….*1查看虚拟码2.8' \
    '萌新累计开播120min_精锻用魔…2022-07-2812:20:43《原神》2.8版jjjjjjjjjjjj本直播季2.8萌新累计开播120…*1查看虚拟码2.8萨F0:42《原查看虚拟码2.81虚拟码：7BLM2HHR6U5N拟码2.80' \
    ':18复制虚拟码《原2.8萌新累计收到1鱼…*1查看虚拟码2.8萌新弹幕条数满6条_冒险家的经…2022-07-2809:50:16《原神》2.8版本直播季2.8萌jjjjjjjjjjjj新弹幕条数满6…*1查看虚拟码2.8萌新直播间送出大气满2' \
    '人_摩拉*…2022-07-2809:50:15《原神》2.8版本直播季2.8萌新直播间送出大….*1查看虚拟码2.8萌新直播间观看时长10min_摩拉…2022-07-2714:03:15 '
# gui.write('hello world', interval=0)
#
# while True:
#     c = r_screen_cut(code[0], '00', hwnd=code[1])
#     d = ocr_accurate(c)
#     #cc = re.findall(r'([\u4E00-\u9FA5]{3}[:|：|\s][A-Za-z\d]{12})', d)
#     e = re.findall(r'[A-Za-z\d]{12}', d)
#     if len(e) == 0:
#         continue
#     change(e)
#

change(['GSWV2BNRAFX2'])



