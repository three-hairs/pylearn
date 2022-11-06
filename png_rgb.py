from PIL import Image
import random



def RGB_to_Hex(rgb):
    # 将RGB格式划分开来
    color = '0x'
    for i in range(0, 3):
        num = int(rgb[i])
        # 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
        color += str(hex(num))[-2:].replace('x', '0').upper()
    # print(color)
    return color


table = ''
img = Image.open("MuMu20210806094112.png")
# print(img.mode)
# print(img.size)
# pos = [134, 262]
# print(RGB_to_Hex(img.getpixel((134, 262))))
# for i in range(0, 7):
#     x = random.randint(-50, 50)
#     y = random.randint(-40, 40)
#     print(x, y)
#     print(RGB_to_Hex(img.getpixel((pos[0]+x, pos[1]+y))))
#     print(img.getpixel((pos[0]+x, pos[1]+y)))
# print(RGB_to_Hex(img.getpixel((134, 262))))
# print(img.getpixel((134, 262)))

x1 = [4, 64, 98, 40, 138, 131, 138, 141]
y1 = [-20, -7, -19, 3, -10, 25, 15, -17]
pos1 = [137, 272]
table += RGB_to_Hex(img.getpixel((137, 272)))
print(RGB_to_Hex(img.getpixel((137, 272))))
for i in range(0, 8):
    table += ', '
    x = random.randint(-50, 50)
    y = random.randint(-30, 30)
    det = str(x) + ", " + str(y)
    table += det
    table += ', '
    table += RGB_to_Hex(img.getpixel((pos1[0]+x, pos1[1]+y)))

    #print(RGB_to_Hex(img.getpixel((pos1[0]+x, pos1[1]+y))))
    #print(img.getpixel((pos1[0]+x, pos1[1]+y)))
print(table)
