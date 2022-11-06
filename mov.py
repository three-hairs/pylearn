import os
highs = []
for i in range(1, 1117):
    if i < 10:
        filename = 'C:\\Users\\Lenovo\\Desktop\\54\\ldiosteotb_00' + str(i) + '.ts'
    elif i >= 10 and i < 100:
        filename = 'C:\\Users\\Lenovo\\Desktop\\54\\ldiosteotb_0' + str(i) + '.ts'
    elif i >= 100:
        filename = 'C:\\Users\\Lenovo\\Desktop\\54\\ldiosteotb_' + str(i) + '.ts'
    #os.remove(filename)
    with open(filename, "rb") as f1:
        highs.append(f1.read())
filename = 'C:\\Users\\Lenovo\\Desktop\\54\\ldiosteotb.mp4'
with open(filename, "wb") as f2:
    for a in highs:
        f2.write(a)


