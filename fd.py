import math
import cv2
from PIL import Image
import numpy as np
from numpy.linalg import norm
from skimage.measure import compare_psnr
from skimage import io,transform
from  skimage.measure import shannon_entropy
from skimage.measure import compare_ssim
Image.MAX_IMAGE_PIXELS = None
import os


def ComEntropy(img1, img2):
    width = img1.shape[0]
    hegith = img1.shape[1]
    tmp = np.zeros((256, 256))
    res = 0
    for i in range(width):
        for j in range(hegith):
            val1 = img1[i][j]
            val2 = img2[i][j]
            tmp[val1][val2] = float(tmp[val1][val2] + 1)
    tmp = tmp / (width * hegith)
    for i in range(width):
        for j in range(hegith):
            if (tmp[i][j] == 0):
                res = res
            else:
                res = res - tmp[i][j] * (math.log(tmp[i][j] / math.log(2.0)))
    return res

def MI (path_A,path_B,path_C):
    A = Image.open(path_A).convert('L')
    B = Image.open(path_B).convert('L')
    C = Image.open(path_C).convert('L')
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    mi1 = shannon_entropy(A) + shannon_entropy(C) - ComEntropy(A, C)
    mi2 = shannon_entropy(B) + shannon_entropy(C) - ComEntropy(B, C)
    mi = (mi1+mi2)/2
    return round(mi,3)



def SSIM(path1,path2,path3):
    pic1 = Image.open(path1).convert('L')
    pic2 = Image.open(path2).convert('L')
    pic3 = Image.open(path3).convert('L')
    pic1 = np.array(pic1)
    pic2 = np.array(pic2)
    pic3 = np.array(pic3)
    ssim1 = compare_ssim(pic1,pic3)
    ssim2 = compare_ssim(pic2,pic3)
    return round((ssim1+ssim2)/2,3)



def mpsnr(x_true, x_pred):
    """
    :param x_true: 高光谱图像：格式：(H, W, C)
    :param x_pred: 高光谱图像：格式：(H, W, C)
    :return: 计算原始高光谱数据与重构高光谱数据的均方误差
    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio
    """
    n_bands = x_true.shape[2]
    p = [compare_psnr(x_true[:, :, k], x_pred[:, :, k], dynamic_range=np.max(x_true[:, :, k])) for k in range(n_bands)]
    return np.mean(p)


def avgGradient(path):
    image = Image.open(path).convert('L')
    image = np.array(image)
    width = image.shape[1]
    width = width - 1
    heigt = image.shape[0]
    heigt = heigt - 1
    tmp = 0.0

    for i in range(width):
        for j in range(heigt):
            dx = float(image[i, j + 1]) - float(image[i, j])
            dy = float(image[i + 1, j]) - float(image[i, j])
            ds = math.sqrt((dx * dx + dy * dy) / 2)
            tmp += ds

    imageAG = tmp / (width * heigt)
    return round(imageAG, 3)

def spatialF(path):
    image = Image.open(path).convert('L')
    image = np.array(image)
    M = image.shape[0]
    N = image.shape[1]

    cf = 0
    rf = 0
    for i in range(1, M - 1):
        for j in range(1, N - 1):
            dx = float(image[i, j - 1]) - float(image[i, j])
            rf += dx ** 2
            dy = float(image[i - 1, j]) - float(image[i, j])
            cf += dy ** 2

    RF = math.sqrt(rf / (M * N))
    CF = math.sqrt(cf / (M * N))
    SF = math.sqrt(RF ** 2 + CF ** 2)

    return round(SF,2)


def sam(x_true, x_pred):
    """
    :param x_true: 高光谱图像：格式：(H, W, C)
    :param x_pred: 高光谱图像：格式：(H, W, C)
    :return: 计算原始高光谱数据与重构高光谱数据的光谱角相似度
    """
    assert x_true.ndim ==3 and x_true.shape == x_pred.shape
    sam_rad = np.zeros(x_pred.shape[0, 1])
    for x in range(x_true.shape[0]):
        for y in range(x_true.shape[1]):
            tmp_pred = x_pred[x, y].ravel()
            tmp_true = x_true[x, y].ravel()
            sam_rad[x, y] = np.arccos(tmp_pred / (norm(tmp_pred) * tmp_true / norm(tmp_true)))
    sam_deg = sam_rad.mean() * 180 / np.pi
    return sam_deg


def mssim(src,dst):
    mean_src = np.mean(src)
    mean_dst = np.mean(dst)
    # 方差var
    var_src = np.var(src)
    var_dst = np.var(dst)
    cov = np.cov(src, dst)
    # 标准差std
    std_src = np.std(src)
    std_dst = np.std(dst)
    # 常数c1,c2,c3
    K1 = 0.01
    K2 = 0.03
    L = 255
    c1 = (K1 * L) ** 2
    c2 = (K2 * L) ** 2
    c3 = c2 / 2
    # 计算ssim
    l = (2 * mean_src * mean_dst + c1) / (mean_src ** 2 + mean_dst ** 2 + c1)
    c = (2 * var_src * var_dst + c2) / (var_src ** 2 + var_dst ** 2 + c2)
    s = (cov + c3) / (var_src * var_dst + c3)
    ssim = l * c * s
    return ssim


def STD(pic_path):
    image = Image.open(pic_path).convert('L')
    image = np.array(image)
    (mean,stddv) = cv2.meanStdDev(image)
    # mean为图像平均值  # 输出标准差
    return round(stddv[0][0],2)#84.7159


def entropy(img):
     out = 0
     count = np.shape(img)[0]*np.shape(img)[1]
     p = np.bincount(np.array(img).flatten())
     for i in range(0, len(p)):
         if p[i]!=0:
             out -= p[i]*math.log(p[i]/count,2)/count
     return out


docList = os.listdir('C:\\Users\\Lenovo\\Desktop\\1\\')
docList.sort()  #
print(docList)
p1 = io.imread("C:\\Users\\Lenovo\\Desktop\\2020_谷里high.jpg")
for dex, list1 in enumerate(docList):
    filename = 'C:\\Users\\Lenovo\\Desktop\\1\\'+list1
    p = io.imread(filename)
    print(entropy(p))

# l1="C:\\Users\\Lenovo\\Desktop\\1.jpg"
# l2="C:\\Users\\Lenovo\\Desktop\\2.jpg"
#
# p = io.imread("C:\\Users\\Lenovo\\Desktop\\1.jpg")
# p1 = io.imread("C:\\Users\\Lenovo\\Desktop\\2.jpg")
# p2 = io.imread("C:\\Users\\Lenovo\\Desktop\\3.jpg")

# print(spatialF(l1), spatialF(l2))

