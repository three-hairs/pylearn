# coding=utf-8
import arcpy
from arcpy import *
from arcpy.sa import *
import math

arcpy.env.workspace = "E:\\temp"
dem_input = "E:\\temp\\DEM.tif"  # 输入栅格数据
wshed = "E:\\temp\\Boundary.shp"  # 输入流域边界数据
demunits = "meters"
scf_lt5 = 0.7
scf_ge5 = 0.5


# 定义信息提示函数
def sendmsg(msg):
    print  msg
    arcpy.AddMessage(msg)


# 定义一个函数，输入字符型坐标、 cellsize 、倍数，返回平移后的字符型坐标值，目的为保留原始小数位数不变
def StoS(s, cellsize, mult):
    stri = s.split('.')
    inte = float(stri[0]) + mult * cellsize
    return str(int(inte)) + '.' + stri[1]


# 可覆盖文件
arcpy.env.overwriteOutput = 1
# 判断输入 DEM 数据的水平和垂直方向的单位是否一致
if demunits == None or demunits.strip() == "":
    demunits = "meters"
    sendmsg(" 使用默认单位： meters")
elif demunits != "meters" and demunits != "feet":
    demunits = "meters"
    sendmsg(" DEM 单位输入有误 , 使用默认单位 meters")
# 设置结束 / 开始坡长累计的中断因子；为小于或大于等于 5 度的坡设置不同的参数
# 输入坡度小于 5 度时，建议值为 0.7 ，大于等于 5 度时，建议值为 0.5
# scf_lt5,scf_ge5 值均需小于 1.1 ，否则赋予默认值
if scf_lt5 >= 1.1:
    scf_lt5 = 0.7
    if scf_ge5 >= 1.1:
        scf_ge5 = 0.5
else:
    if scf_ge5 >= 1.1:
        scf_ge5 = 0.5
sendmsg(str(scf_lt5) + "," + str(scf_ge5))
# 通过 Describe 方法获取输入 DEM 数据的范围和分辨率大小
dem_des = arcpy.Describe(dem_input)
cell_W = dem_des.MeanCellWidth
cell_H = dem_des.MeanCellHeight
cell_size = max(cell_W, cell_H)
cell_size = max(cell_W, cell_H)  # 如果格网高宽不一样，取最大值

extent = dem_des.extent
extent_buf = StoS(str(extent.XMin), cell_size, - 1) + " " + StoS(str(extent.YMin), cell_size, - 1) + " " + StoS(
    str(extent.XMax), cell_size, 1) + " " + StoS(str(extent.YMax)
                                                 , cell_size, 1)
sendmsg(" 做一个格网缓冲后的范围 " + extent_buf)
sendmsg(" 创建填充 DEM——dem_fill")
# 检查 Spatial 工具权限，很重要的一步

arcpy.CheckOutExtension("Spatial")
# arcpy.Fill_sa(dem_input,"dem_fill")
# 使用 Hickey 对 ArcGIS 自带 Fill 功能的修改构建填充 DEM; 本算法使用一个格网的圆环用于单个洼地格网，用八邻域格网的最小值应用于洼地格网
arcpy.Extent = "MAXOF"
arcpy.Extent = extent
arcpy.CellSize = cell_size
arcpy.CopyRaster_management(dem_input, "dem_fill2.tif")
dem_flow = FocalFlow("dem_fill2.tif")
dem_flow.save("dem_flow.tif")
dem_fill = Con("dem_flow" == 255, FocalStatistics("dem_fill2.tif", NbrAnnulus(1, 1, "CELL"), "MINORITY"),
               "dem_fill2.tif")
dem_fill.save("dem_fill.tif")  # 用八邻域格网的最小值应用于洼地格网
sendmsg(" 根据八邻域格网值创建每个格网的流入或流出方向 ")
flowdir_in = FocalFlow("dem_fill.tif")
flowdir_in.save("flowdir_in.tif")
flowdir_out = FlowDirection("dem_fill.tif")
flowdir_out.save("flowdir_out.tif")
# 重新设置 Environment 的 Extent 为扩充一个格网大小的范围
arcpy.Extent = "MAXOF"
arcpy.Extent = extent
sendmsg(" 为 dem_fill 创建一个格网大小的缓冲 ")

dem_fill_b = Con(IsNull("dem_fill.tif"), FocalStatistics("dem_fill.tif", NbrAnnulus(1, 1, "CELL"), "MINORITY"),
                 "dem_fill.tif")
dem_fill_b.save("dem_fill_b.tif")
# 设置直角的和对角线的流向计算时的格网长度
cellorth = 1.00 * cell_size
celldiag = cell_size * (2 ** 0.5)
# 为每个格网计算坡降（ downslope ）角，修正了以前代码并重新设置平地格网（默认 0.0 度，即没有流出方向） >0.00 并 <0.57(inv. tan of 1% gradient) ；
# 建议值 0.1 ；新的假设是所有格网即使实际上是平的比如干湖，都有 >0.00 的坡度；这保证了所有格网都和流向网络有关，因而可以被赋坡度角和最终的 LS 因素值，
# 然而它需要非常小。
sendmsg(" 为每个格网计算坡降（ downslope ）角 ")
deg = 180.0 / math.pi
#  使用 shift 计算不同流向的偏移量
Shift_management("dem_fill_b.tif", "dem_fill_b64.tif", "0", "- " + str(cell_size))
Shift_management("dem_fill_b.tif", "dem_fill_b128.tif", "-" + str(cell_size), "-" + str(cell_size))
Shift_management("dem_fill_b.tif", "dem_fill_b1.tif", "-" + str(cell_size), "0")
Shift_management("dem_fill_b.tif", "dem_fill_b2.tif", "-" + str(cell_size), str(cell_size))
Shift_management("dem_fill_b.tif", "dem_fill_b4.tif", "0", str(cell_size))
Shift_management("dem_fill_b.tif", "dem_fill_b8.tif", str(cell_size), str(cell_size))
Shift_management("dem_fill_b.tif", "dem_fill_b16.tif", str(cell_size), "0")
Shift_management("dem_fill_b.tif", "dem_fill_b32.tif", str(cell_size), "-" + str(cell_size))
#  计算每个网格的坡降角
down_slp_ang2 = Con(flowdir_out == 64, deg * ATan((Raster("dem_fill_b.tif") - Raster("dem_fill_b64.tif")) / cellorth),
                    Con(flowdir_out == 128,
                        deg * ATan((Raster("dem_fill_b.tif") - Raster("dem_fill_b128.tif")) / cellorth),
                        Con(flowdir_out == 1,
                            deg * ATan((Raster("dem_fill_b.tif") - Raster("dem_fill_b1.tif")) / cellorth), \
                            Con(flowdir_out == 2,
                                deg * ATan((Raster("dem_fill_b.tif") - Raster("dem_fill_b2.tif")) / cellorth), \
                                Con(flowdir_out == 4,
                                    deg * ATan((Raster("dem_fill_b.tif") - Raster("dem_fill_b4.tif")) / cellorth), \
                                    Con(flowdir_out == 8,
                                        deg * ATan((Raster("dem_fill_b.tif") - Raster("dem_fill_b8.tif")) / cellorth), \
                                        Con(flowdir_out == 16, deg * ATan(
                                            (Raster("dem_fill_b.tif") - Raster("dem_fill_b16.tif")) / cellorth), \
                                            Con(flowdir_out == 32, deg * ATan((Raster("dem_fill_b.tif") - Raster(
                                                "dem_fill_b32.tif")) / cellorth)))))))))
down_slp_ang2.save("down_slp_ang2.tif")
# 将等于 0.0 的格网赋值为 0.1
down_slp_ang = Con(down_slp_ang2 <= 0, 0.1, down_slp_ang2)
down_slp_ang.save("down_slp_ang.tif")
# 重新设置环境中 Extent 为原始大小，并裁减 downslope 格网，重命名为原始名称
arcpy.Extent = "MAXOF"
arcpy.Extent = extent
sendmsg(" 计算每个格网的非累计格网坡长 slp_lgth_cell ，考虑到直角或对角线流出方向 （暂没考虑局部高程点） ")
slp_lgth_cell = Con(flowdir_out == 2, celldiag, Con(flowdir_out == 8, celldiag, Con(flowdir_out == 32, celldiag,
                                                                                    Con(flowdir_out == 128, celldiag,
                                                                                        cellorth))))
slp_lgth_cell.save("slp_lgth_cell.tif")
# 再设置环境的 Extent 为缓冲范围，创建缓冲格网为 0 的流出方向格网
arcpy.Extent = "MAXOF"
arcpy.Extent = extent
flowdir_out_b = Con(IsNull(flowdir_out), 0, flowdir_out)
flowdir_out_b.save("flowdir_out_b.tif")
# 创建初始每个格网单元的非累计坡长（ NCSL ），并对 flowdir_in 和 flowdir_out 做按位于运算，找到正常的流向格网，
# 并设为 Nodata ，然后计算高点（包括填充的洼地）为 1/2*slp_lgth_cell 长度。
sendmsg(" 创建初始累计坡长格网 slp_lgth_cum")
Shift_management("flowdir_out_b.tif", "flowdir_out_b64.tif", "0", "-" + str(cell_size))
Shift_management("flowdir_out_b.tif", "flowdir_out_b128.tif", "-" + str(cell_size), "-" + str(cell_size))
Shift_management("flowdir_out_b.tif", "flowdir_out_b1.tif", "-" + str(cell_size), "0")
Shift_management("flowdir_out_b.tif", "flowdir_out_b2.tif", "-" + str(cell_size), str(cell_size))
Shift_management("flowdir_out_b.tif", "flowdir_out_b4.tif", "0", str(cell_size))
Shift_management("flowdir_out_b.tif", "flowdir_out_b8.tif", str(cell_size), str(cell_size))
Shift_management("flowdir_out_b.tif", "flowdir_out_b16.tif", str(cell_size), "0")
Shift_management("flowdir_out_b.tif", "flowdir_out_b32.tif", str(cell_size), "-" + str(cell_size))
slp_lgth_cum = Con(BitwiseAnd(flowdir_in, 64) & (Raster("flowdir_out_b64.tif") == 4),
                   SetNull(BitwiseAnd(flowdir_in, 64) & (Raster("flowdir_out_b64.tif") == 4), 1),
                   Con(BitwiseAnd(flowdir_in, 128) & (Raster("flowdir_out_b128.tif") == 8),
                       SetNull(BitwiseAnd(flowdir_in, 128) & (Raster("flowdir_out_b128.tif") == 8), 1),
                       Con(BitwiseAnd(flowdir_in, 1) & (Raster("flowdir_out_b1.tif") == 16),
                           SetNull(BitwiseAnd(flowdir_in, 1) & (Raster("flowdir_out_b1.tif") == 16), 1),
                           Con(BitwiseAnd(flowdir_in, 2) & (Raster("flowdir_out_b2.tif") == 32),
                               SetNull(BitwiseAnd(flowdir_in, 2) & (Raster("flowdir_out_b2.tif") == 32), 1),
                               Con(BitwiseAnd(flowdir_in, 4) & (Raster("flowdir_out_b4.tif") == 64),
                                   SetNull(BitwiseAnd(flowdir_in, 4) & (Raster("flowdir_out_b4.tif") == 64), 1),
                                   Con(BitwiseAnd(flowdir_in, 8) & (Raster("flowdir_out_b8.tif") == 128),
                                       SetNull(BitwiseAnd(flowdir_in, 8) & (Raster("flowdir_out_b8.tif") == 128), 1),
                                       Con(BitwiseAnd(flowdir_in, 16) & (Raster("flowdir_out_b16.tif") == 1),
                                           SetNull(BitwiseAnd(flowdir_in, 16) & (Raster("flowdir_out_b16.tif") == 1),
                                                   1),
                                           Con(BitwiseAnd(flowdir_in, 32) & (Raster("flowdir_out_b32.tif") == 2),
                                               SetNull(
                                                   BitwiseAnd(flowdir_in, 32) & (Raster("flowdir_out_b32.tif") == 2),
                                                   1), 0.5 * slp_lgth_cell))))))))
slp_lgth_cum.save("slp_lgth_cum.tif")
# 设置起始坡长计算点（高点和填充的洼地）在所有其他格网坡长已经被决定进入每个迭代；
# 起始点将有一个等于 1/2 它们坡长的值；起始点 ( 局部高程点 ) 就是周围没有其他格网单元流入，或有其他单元流入，
# 但与入流单元之间坡角为零的格网单元，对应于 DEM 中的山顶、山脊线上的点及位于 DEM 边缘的点，这些点通过水流方向矩阵识别，
# 识别的条件是格网单元周边各相邻点的水流方向均不知向该单元；修正了以前的代码，改变了 “ 平地 ” 高点得到一个 0~1/2 格网坡长的值；
# 新的假设是，最小累计坡长是 1/2 格网坡长，即使是填充洼地和 “ 平地 ” 高点，从而确保每个格网 LS 因子的值 >0.00
sendmsg(" 设置起始坡长计算点 slp_lgth_beg")
slp_lgth_beg = Con(IsNull(slp_lgth_cum), cell_size, slp_lgth_cum)
slp_lgth_beg.save("slp_lgth_beg.tif")
# 指配坡度结束（ slope-end ）因素在累计坡长结束处；修正了以前的代码中利用 RUSLE 准则建议的坡度临界 5%(2.8624 弧度 ) 来区分两个不同的侵蚀 / 沉积对特别小
# 或特别陡的坡度；对 <5% 使用的参数比 >=5% 的大；这会使在浅滩处更容易结束侵蚀，开始沉积过程；比如，一个更高的临界值意味着需要更少的坡度降低就可以结束累计。
sendmsg(" 创建结束坡长累计阈值的格网 slp_lgth_fac")
slp_end_fac = Con(down_slp_ang < 2.8624, scf_lt5, scf_ge5)
slp_end_fac.save("slp_end_fac.tif")
# 移除所有任何剩余的方向格网数据（之前运行留下的）
if arcpy.Exists("fromcell_n"):
    arcpy.Delete_management("fromcell_n")
if arcpy.Exists("fromcell_ne"):
    arcpy.Delete_management("fromcell_ne")
if arcpy.Exists("fromcell_e"):
    arcpy.Delete_management("fromcell_e")
if arcpy.Exists("fromcell_se"):
    arcpy.Delete_management("fromcell_se")
if arcpy.Exists("fromcell_s"):
    arcpy.Delete_management("fromcell_s")
if arcpy.Exists("fromcell_sw"):
    arcpy.Delete_management("fromcell_sw")
if arcpy.Exists("fromcell_w"):
    arcpy.Delete_management("fromcell_w")
if arcpy.Exists("fromcell_nw"):
    arcpy.Delete_management("fromcell_nw")
# 修正以前版本代码中创建一系列测试 nodata 数据来跟踪运行过程；重新设置环境 Extent 为正常，用 dem_fill 格网作为掩膜检验缓冲格网
arcpy.Extent = "MAXOF"
arcpy.Extent = extent
arcpy.Mask = dem_input
arcpy.CellSize = cell_size
ndcell = 1
# 修正了以前版本代码中设置迭代中 nodata 格网为 0
arcpy.CopyRaster_management("slp_end_fac.tif", "slp_lgth_nd3.tif")
slp_lgth_nd2 = Con(Raster("slp_lgth_nd3.tif") > 0, 0)
slp_lgth_nd2.save("slp_lgth_nd2.tif")
warn = 0
# 开始为每个格网计算累计坡长的迭代循环：依据格网单元流向，将流入当前格网单元的上游格网单元非累计坡长进行累加。
# 如果当前格网单元的上游单元不知一个，则取当前格网单元上游最大坡长值作为当前格网单元的上游累计坡长。
finished = 0
n = 1

slp_lgth_cum2 = Raster("slp_lgth_cum.tif")
slp_lgth_cum2.save("slp_lgth_cum2.tif")

while not finished:
    sendmsg(" 现在开始每个格网坡长计算的第 " + str(n) + " 次循环！ ")
    slp_lgth_prev = Raster("slp_lgth_cum2.tif")
    slp_lgth_prev.save("slp_lgth_prev.tif")
    count = range(1, 9)
    for counter in count:
        # 为不同的条件设置不同的参数值
        if counter == 1:
            dirfrom = 4
            dirpossto = 64
            cellcol = 0
            cellrow = - 1
        elif counter == 2:
            fromcell_n = Raster("fromcell_dir.tif")
            fromcell_n.save("fromcell_n.tif")
            dirfrom = 8
            dirpossto = 128
            cellcol = 1
            cellrow = - 1
        elif counter == 3:
            fromcell_ne = Raster("fromcell_dir.tif")
            fromcell_ne.save("fromcell_ne.tif")
            dirfrom = 16
            dirpossto = 1
            cellcol = 1
            cellrow = 0
        elif counter == 4:
            fromcell_e = Raster("fromcell_dir.tif")
            fromcell_e.save("fromcell_e.tif")
            dirfrom = 32
            dirpossto = 2
            cellcol = 1
            cellrow = 1
        elif counter == 5:
            fromcell_se = Raster("fromcell_dir.tif")
            fromcell_se.save("fromcell_se.tif")
            dirfrom = 64
            dirpossto = 4
            cellcol = 0
            cellrow = 1
        elif counter == 6:
            fromcell_s = Raster("fromcell_dir.tif")
            fromcell_s.save("fromcell_s.tif")
            dirfrom = 128
            dirpossto = 8
            cellcol = - 1
            cellrow = 1
        elif counter == 7:
            fromcell_sw = Raster("fromcell_dir.tif")
            fromcell_sw.save("fromcell_sw.tif")
            dirfrom = 1
            dirpossto = 16
            cellcol = - 1
            cellrow = 0
        else:
            fromcell_w = Raster("fromcell_dir.tif")
            fromcell_w.save("fromcell_w.tif")
            dirfrom = 2
            dirpossto = 32
            cellcol = - 1
            cellrow = - 1
    Shift_management("flowdir_out_b.tif", "flowdir_out_StoS.tif", - 1 * cellcol * cell_size, cell_size * cellrow)
    Shift_management("down_slp_ang.tif", "down_slp_ang_StoS.tif", - 1 * cellcol * cell_size, cell_size * cellrow)
    Shift_management("slp_lgth_prev.tif", "slp_lgth_prev_StoS.tif", - 1 * cellcol * cell_size, cell_size * cellrow)
    Shift_management("slp_lgth_cell.tif", "slp_lgth_cell_StoS.tif", - 1 * cellcol * cell_size, cell_size * cellrow)
    fromcell_dir = Con(~ BitwiseAnd(flowdir_in, dirpossto), 0, \
                       Con(Raster("flowdir_out_StoS.tif") != dirfrom, 0, \
                           Con(Raster("down_slp_ang.tif") < Raster("down_slp_ang_StoS.tif") * Raster("slp_end_fac.tif"),
                               0, \
                               Con(Raster("down_slp_ang.tif") >= Raster("down_slp_ang_StoS.tif") * Raster(
                                   "slp_end_fac.tif"),
                                   Raster("slp_lgth_prev_StoS.tif") + Raster("slp_lgth_cell_StoS.tif"), \
                                   Con(IsNull("slp_lgth_prev_StoS.tif"), SetNull(IsNull("slp_lgth_prev_StoS.tif"), 1),
                                       0)))))
    fromcell_dir.save("fromcell_dir.tif")
    if counter == 8:
        fromcell_nw = Raster("fromcell_dir.tif")
    fromcell_nw.save("fromcell_nw.tif")
    # 在 fromcell 各方向中选择最大的累计坡长
    slp_lgth_cum2 = CellStatistics(
        ["fromcell_n.tif", "fromcell_ne.tif", "fromcell_e.tif", "fromcell_se.tif", "fromcell_s.tif", "fromcell_sw.tif",
         "fromcell_w.tif", "fromcell_nw.tif", "slp_lgth_cum.tif"], "MAXIMUM")
    slp_lgth_cum2.save("slp_lgth_cum2.tif")
    # 检查最后一次循环所有格网都有
    try:
        nd_chg2_max2 = arcpy.GetRasterProperties_management("nd_chg2.tif", "MINIMUM")
        ndcell = int(nd_chg2_max2.getOutput(0))
        sendmsg(str(nd_chg2_max2))
    except:
        sendmsg(arcpy.GetMessages(2))
    nd2 = nd_chg2_max2
    if nd2 != 0:
        finished = 0
        warn = 1
    n = n + 1

# 将最后一次循环产生的累计格网重命名为 max ，裁剪后再重命名回去
arcpy.CopyRaster_management("slp_lgth_cum.tif", "slp_lgth_max.tif")
arcpy.Extent = "MAXOF"
arcpy.Extent = extent
if arcpy.Exists("slp_lgth_max2"):
    arcpy.Delete_management("slp_lgth_max2")
arcpy.CopyRaster_management("slp_lgth_max.tif", "slp_lgth_max2.tif")
# 如果有必要的话将坡长单位从 meters 转换为 feet
if arcpy.Exists("slp_lgth_ft"):
    arcpy.Delete_management("slp_lgth_ft")
if demunits == "meters":
    slp_lgth_ft = Raster("slp_lgth_max.tif") / 0.3048
else:
    arcpy.CopyRaster_management("slp_lgth_ft,tif", "slp_lgth_max.tif")

# 修正了以前版本中根据细沟 / 细沟侵蚀率为 RUSLE 中坡长分配指数；要明确的是草地 / 森林有低的敏感度；根据 McCool 等人准则中表格 4-5 （ 1997 ）。
sendmsg(" 计算坡度幂指数 m_slpexp")
if arcpy.Exists("m_slpexp"):
    arcpy.Delete_management("m_slpexp")
m_slpexp = Con(Raster("down_slp_ang.tif") <= 0.1, 0.01, \
               Con((Raster("down_slp_ang.tif") > 0.1) & (Raster("down_slp_ang.tif") < 0.2), 0.02,
                   Con((Raster("down_slp_ang.tif") >= 0.2) & (Raster("down_slp_ang.tif") < 0.4), 0.04,
