# coding=utf-8
import math
import arcpy
from arcpy.sa import *
from arcpy import env

env.workspace = "E:\\workspace"

rainfall_month = "E:\\workspace\\rainfall month\\"
rainfall_year = "E:\\workspace\\rainfall year.tif"
san = "E:\\workspace\\san.tif"
sil = "E:\\workspace\\sil.tif"
cla = "E:\\workspace\\cla.tif"
c = "E:\\workspace\\C.tif"
dem_input = "E:\\workspace\\DEM.tif"  # input DEM raster
ndvi = "E:\\workspace\\ndvi.tif"
soil_con = "E:\\workspace\\soil condition.tif"
# input soil_erosion_area raster
m_a = arcpy.Raster("E:\\workspace\\soil erosion area.tif")
m_w = arcpy.Raster("E:\\workspace\\water soil loss.tif")
m_v = arcpy.Raster("E:\\workspace\\vegetation factors.tif")


# input str(coord ,cellsize ,mult)
# output Shifted str(coord) to keep decimal digits
def StoS(s, cellsize, mult):
    stri = s.split('.')
    inte = float(stri[0]) + mult * cellsize
    return str(int(inte)) + '.' + stri[1]


# calculate R factors
m_r = 0
rain_year = arcpy.Raster(rainfall_year)
for i in range(1, 13):
    curr_month = rainfall_month + str(i) + ".tif"
    rain_mon = arcpy.Raster(curr_month)
    m_r = m_r + 1.735 \
          * Power(10, 1.5 * Ln(rain_mon ** 2 / rain_year - 0.8188))

# calculate L factors
san = arcpy.Raster(san)
sil = arcpy.Raster(sil)
cla = arcpy.Raster(cla)
c = arcpy.Raster(c)
sn = 1 - san / 100
m_l = (0.2 + 0.3 * Exp(0.0253 * san * (1 - sil / 100))) \
      * Power((sil / (cla + sil)), 0.3) \
      * (1.0 - 0.25 * c / (c + Exp(3.72 - 2.95 * c))) \
      * (1.0 - 0.7 * sn / (sn + Exp(-5.51 + 22.9 * sn)))

# calculate LS factors
scf_lt5 = 0.7
scf_ge5 = 0.5
#  Describe get DEM boundary and resolution
dem_des = arcpy.Describe(dem_input)
cell_W = dem_des.MeanCellWidth
cell_H = dem_des.MeanCellHeight
# get the max grid value
cell_size = max(cell_W, cell_H)

extent = dem_des.extent
extent_buf = StoS(str(extent.XMin), cell_size, - 1) \
             + " " + StoS(str(extent.YMin), cell_size, - 1) \
             + " " + StoS(str(extent.XMax), cell_size, 1) \
             + " " + StoS(str(extent.YMax), cell_size, 1)

arcpy.CheckOutExtension("Spatial")
# build Fill DEM
arcpy.Extent = "MAXOF"
arcpy.Extent = extent
arcpy.CellSize = cell_size
arcpy.CopyRaster_management(dem_input, "dem_fill2.tif")
dem_flow = FocalFlow("dem_fill2.tif")
dem_flow.save("dem_flow.tif")
dem_fill = Con("dem_flow" == 255,
               FocalStatistics("dem_fill2.tif", NbrAnnulus(1, 1, "CELL"), "MINORITY"),
               "dem_fill2.tif")
dem_fill.save("dem_fill.tif")

# fill grid use min value of 8 neighborhood
# create flow direction by 8 neighbor grid
flowdir_in = FocalFlow("dem_fill.tif")
flowdir_in.save("flowdir_in.tif")
flowdir_out = FlowDirection("dem_fill.tif")
flowdir_out.save("flowdir_out.tif")

# reset Environment Extent
arcpy.Extent = "MAXOF"
arcpy.Extent = extent
# create a grid buffer for dem_fill
dem_fill_b = Con(IsNull("dem_fill.tif"),
                 FocalStatistics("dem_fill.tif", NbrAnnulus(1, 1, "CELL"), "MINORITY"),
                 "dem_fill.tif")
dem_fill_b.save("dem_fill_b.tif")
# set flow direction for gird calculate
cellorth = 1.00 * cell_size
celldiag = cell_size * (2 ** 0.5)
# calculate offset of diff direction
deg = 180.0 / math.pi
arcpy.Shift_management("dem_fill_b.tif", "dem_fill_b64.tif", "0", "- " + str(cell_size))
arcpy.Shift_management("dem_fill_b.tif", "dem_fill_b128.tif", "-" + str(cell_size), "-" + str(cell_size))
arcpy.Shift_management("dem_fill_b.tif", "dem_fill_b1.tif", "-" + str(cell_size), "0")
arcpy.Shift_management("dem_fill_b.tif", "dem_fill_b2.tif", "-" + str(cell_size), str(cell_size))
arcpy.Shift_management("dem_fill_b.tif", "dem_fill_b4.tif", "0", str(cell_size))
arcpy.Shift_management("dem_fill_b.tif", "dem_fill_b8.tif", str(cell_size), str(cell_size))
arcpy.Shift_management("dem_fill_b.tif", "dem_fill_b16.tif", str(cell_size), "0")
arcpy.Shift_management("dem_fill_b.tif", "dem_fill_b32.tif", str(cell_size), "-" + str(cell_size))
# calculate downslope angle
down_slp_ang2 = Con(flowdir_out == 64,
                    deg * ATan((arcpy.Raster("dem_fill_b.tif") - arcpy.Raster("dem_fill_b64.tif")) / cellorth),
                    Con(flowdir_out == 128,
                        deg * ATan((arcpy.Raster("dem_fill_b.tif") - arcpy.Raster("dem_fill_b128.tif")) / cellorth),
                        Con(flowdir_out == 1,
                            deg * ATan((arcpy.Raster("dem_fill_b.tif") - arcpy.Raster("dem_fill_b1.tif")) / cellorth),
                            Con(flowdir_out == 2,
                                deg * ATan(
                                    (arcpy.Raster("dem_fill_b.tif") - arcpy.Raster("dem_fill_b2.tif")) / cellorth),
                                Con(flowdir_out == 4,
                                    deg * ATan(
                                        (arcpy.Raster("dem_fill_b.tif") - arcpy.Raster("dem_fill_b4.tif")) / cellorth),
                                    Con(flowdir_out == 8,
                                        deg * ATan((arcpy.Raster("dem_fill_b.tif") - arcpy.Raster(
                                            "dem_fill_b8.tif")) / cellorth),
                                        Con(flowdir_out == 16, deg * ATan(
                                            (arcpy.Raster("dem_fill_b.tif") - arcpy.Raster(
                                                "dem_fill_b16.tif")) / cellorth),
                                            Con(flowdir_out == 32,
                                                deg * ATan((arcpy.Raster("dem_fill_b.tif") - arcpy.Raster(
                                                    "dem_fill_b32.tif")) / cellorth)))))))))
down_slp_ang2.save("down_slp_ang2.tif")
# change grid value 0 to 0.1
down_slp_ang = Con(down_slp_ang2 <= 0, 0.1, down_slp_ang2)
down_slp_ang.save("down_slp_ang.tif")

# reset Extent calculate Non cumulative grid slope length
arcpy.Extent = "MAXOF"
arcpy.Extent = extent
slp_lgth_cell = Con(flowdir_out == 2, celldiag,
                    Con(flowdir_out == 8, celldiag,
                        Con(flowdir_out == 32, celldiag,
                            Con(flowdir_out == 128, celldiag, cellorth))))
slp_lgth_cell.save("slp_lgth_cell.tif")
flowdir_out_b = Con(IsNull(flowdir_out), 0, flowdir_out)
flowdir_out_b.save("flowdir_out_b.tif")
# create NCSL of every cell 'slp_lgth_cum'，
# use BitwiseAnd calculate flowdir_in,flowdir_out to find true direction grid
# and sta value Nodata ，then calculate high point length: 1/2*slp_lgth_cell
arcpy.Shift_management("flowdir_out_b.tif", "flowdir_out_b64.tif", "0", "-" + str(cell_size))
arcpy.Shift_management("flowdir_out_b.tif", "flowdir_out_b128.tif", "-" + str(cell_size), "-" + str(cell_size))
arcpy.Shift_management("flowdir_out_b.tif", "flowdir_out_b1.tif", "-" + str(cell_size), "0")
arcpy.Shift_management("flowdir_out_b.tif", "flowdir_out_b2.tif", "-" + str(cell_size), str(cell_size))
arcpy.Shift_management("flowdir_out_b.tif", "flowdir_out_b4.tif", "0", str(cell_size))
arcpy.Shift_management("flowdir_out_b.tif", "flowdir_out_b8.tif", str(cell_size), str(cell_size))
arcpy.Shift_management("flowdir_out_b.tif", "flowdir_out_b16.tif", str(cell_size), "0")
arcpy.Shift_management("flowdir_out_b.tif", "flowdir_out_b32.tif", str(cell_size), "-" + str(cell_size))

slp_lgth_cum = Con(BitwiseAnd(flowdir_in, 64) & (arcpy.Raster("flowdir_out_b64.tif") == 4),
                   SetNull(BitwiseAnd(flowdir_in, 64) & (arcpy.Raster("flowdir_out_b64.tif") == 4), 1),
                   Con(BitwiseAnd(flowdir_in, 128) & (arcpy.Raster("flowdir_out_b128.tif") == 8),
                       SetNull(BitwiseAnd(flowdir_in, 128) & (arcpy.Raster("flowdir_out_b128.tif") == 8), 1),
                       Con(BitwiseAnd(flowdir_in, 1) & (arcpy.Raster("flowdir_out_b1.tif") == 16),
                           SetNull(BitwiseAnd(flowdir_in, 1) & (arcpy.Raster("flowdir_out_b1.tif") == 16), 1),
                           Con(BitwiseAnd(flowdir_in, 2) & (arcpy.Raster("flowdir_out_b2.tif") == 32),
                               SetNull(BitwiseAnd(flowdir_in, 2) & (arcpy.Raster("flowdir_out_b2.tif") == 32), 1),
                               Con(BitwiseAnd(flowdir_in, 4) & (arcpy.Raster("flowdir_out_b4.tif") == 64),
                                   SetNull(BitwiseAnd(flowdir_in, 4) & (arcpy.Raster("flowdir_out_b4.tif") == 64), 1),
                                   Con(BitwiseAnd(flowdir_in, 8) & (arcpy.Raster("flowdir_out_b8.tif") == 128),
                                       SetNull(BitwiseAnd(flowdir_in, 8) & (
                                               arcpy.Rarcpy.aster("flowdir_out_b8.tif") == 128), 1),
                                       Con(BitwiseAnd(flowdir_in, 16) & (arcpy.Raster("flowdir_out_b16.tif") == 1),
                                           SetNull(
                                               BitwiseAnd(flowdir_in, 16) & (arcpy.Raster("flowdir_out_b16.tif") == 1),
                                               1),
                                           Con(BitwiseAnd(flowdir_in, 32) & (arcpy.Raster("flowdir_out_b32.tif") == 2),
                                               SetNull(BitwiseAnd(flowdir_in, 32)
                                                       & (arcpy.Raster("flowdir_out_b32.tif") == 2), 1),
                                               0.5 * slp_lgth_cell))))))))
slp_lgth_cum.save("slp_lgth_cum.tif")

# set begine of slope length cal point
slp_lgth_beg = Con(IsNull(slp_lgth_cum), cell_size, slp_lgth_cum)
slp_lgth_beg.save("slp_lgth_beg.tif")
# create finished slp_lgth_fac
slp_end_fac = Con(down_slp_ang < 2.8624, scf_lt5, scf_ge5)
slp_end_fac.save("slp_end_fac.tif")
# remove all data create before
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
arcpy.Extent = "MAXOF"
arcpy.Extent = extent
arcpy.Mask = dem_input
arcpy.CellSize = cell_size
ndcell = 1
arcpy.CopyRaster_management("slp_end_fac.tif", "slp_lgth_nd3.tif")
slp_lgth_nd2 = Con(arcpy.Raster("slp_lgth_nd3.tif") > 0, 0)
slp_lgth_nd2.save("slp_lgth_nd2.tif")
warn = 0





# Start the iteration cycle of calculating the cumulative grade length for each grid:
# according to the grid cell flow direction,
# the non cumulative grade length of the upstream grid cell flowing into the current grid cell is accumulated.
# If there is not one upstream unit of the current grid unit,
# the maximum upstream grade length is taken as the upstream cumulative grade length of the current grid unit.
finished = 0
n = 1
slp_lgth_cum2 = arcpy.Raster("slp_lgth_cum.tif")
slp_lgth_cum2.save("slp_lgth_cum2.tif")
dirfrom_lis = [4, 8, 16, 32, 64, 128, 1, 2]
dirpossto_lis = [64, 128, 1, 2, 4, 8, 16, 32]
cellcol_lis = [0, 1, 1, 1, 0, -1, -1, -1]
cellrow_lis = [-1, -1, 0, 1, 1, 1, 0, -1]
while not finished:
    print " slope length calculate " + str(n+1) + "times"
    slp_lgth_prev = arcpy.Raster("slp_lgth_cum2.tif")
    slp_lgth_prev.save("slp_lgth_prev.tif")
    count = range(0, 8)
    for counter in count:
        # set diff value for diff direction
        dirfrom = dirfrom_lis[i]
        dirpossto = dirpossto_lis[i]
        cellcol = cellcol_lis[i]
        cellrow = cellrow_lis[i]
        arcpy.Shift_management("flowdir_out_b.tif", "flowdir_out_StoS.tif", - 1 * cellcol * cell_size,
                               cell_size * cellrow)
        arcpy.Shift_management("down_slp_ang.tif", "down_slp_ang_StoS.tif", - 1 * cellcol * cell_size,
                               cell_size * cellrow)
        arcpy.Shift_management("slp_lgth_prev.tif", "slp_lgth_prev_StoS.tif", - 1 * cellcol * cell_size,
                               cell_size * cellrow)
        arcpy.Shift_management("slp_lgth_cell.tif", "slp_lgth_cell_StoS.tif", - 1 * cellcol * cell_size,
                               cell_size * cellrow)
        fromcell_dir = Con(~ BitwiseAnd(flowdir_in, dirpossto), 0,
                           Con(arcpy.Raster("flowdir_out_StoS.tif") != dirfrom, 0,
                               Con(arcpy.Raster("down_slp_ang.tif") < arcpy.Raster(
                                   "down_slp_ang_StoS.tif") * arcpy.Raster("slp_end_fac.tif"), 0,
                                   Con(arcpy.Raster("down_slp_ang.tif") >= arcpy.Raster(
                                       "down_slp_ang_StoS.tif") * arcpy.Raster("slp_end_fac.tif"),
                                       arcpy.Raster("slp_lgth_prev_StoS.tif") + arcpy.Raster("slp_lgth_cell_StoS.tif"),
                                       Con(IsNull("slp_lgth_prev_StoS.tif"),
                                           SetNull(IsNull("slp_lgth_prev_StoS.tif"), 1), 0)))))
        fromcell_dir.save("fromcell_dir.tif")
        if counter == 7:
            fromcell_nw = arcpy.Raster("fromcell_dir.tif")
            fromcell_nw.save("fromcell_nw.tif")
        #  fromcell select max slope length
            slp_lgth_cum2 = CellStatistics(
                ["fromcell_n.tif", "fromcell_ne.tif", "fromcell_e.tif", "fromcell_se.tif", "fromcell_s.tif",
                 "fromcell_sw.tif",
                 "fromcell_w.tif", "fromcell_nw.tif", "slp_lgth_cum.tif"], "MAXIMUM")
            slp_lgth_cum2.save("slp_lgth_cum2.tif")
        # check all grid
        try:
            nd_chg2_max2 = arcpy.GetRasterProperties_management("nd_chg2.tif", "MINIMUM")
            ndcell = int(nd_chg2_max2.getOutput(0))

        except:
            nd2 = nd_chg2_max2
            if nd2 != 0:
                finished = 0
                warn = 1
        n = n + 1
# clip last grid
arcpy.CopyRaster_management("slp_lgth_cum.tif", "slp_lgth_max.tif")

arcpy.Extent = "MAXOF"
arcpy.Extent = extent
if arcpy.Exists("slp_lgth_max2"):
    arcpy.Delete_management("slp_lgth_max2")
arcpy.CopyRaster_management("slp_lgth_max.tif", "slp_lgth_max2.tif")
if arcpy.Exists("m_slpexp"):
    arcpy.Delete_management("m_slpexp")
m_slpexp = Con(arcpy.Raster("down_slp_ang.tif") <= 0.1, 0.01,
               Con((arcpy.Raster("down_slp_ang.tif") > 0.1) & (arcpy.Raster("down_slp_ang.tif") < 0.2), 0.02,
                   Con((arcpy.Raster("down_slp_ang.tif") >= 0.2) & (arcpy.Raster("down_slp_ang.tif") < 0.4), 0.04)))
m_slpexp.save('m_slepexp.tif')
# calculate L factor
rusle_l = Power((arcpy.Raster("slp_lgth_max.tif")/72.6))
# rast_dem = arcpy.Raster(dem_input)
# slope = arcpy.sa.Slope(rast_dem)
# aspect = arcpy.sa.Aspect(rast_dem)
# slope_l = rast_dem / (Sin(slope * math.pi / 180))
rusle_s = Con(arcpy.Raster("down_slp_ang.tif") <= 5,
              10.8 * Sin(arcpy.Raster("down_slp_ang.tif") / deg) + 0.03,
              Con(arcpy.Raster("down_slp_ang.tif") > 5 & arcpy.Raster("down_slp_ang.tif") < 10,
                  16.8 * Sin(arcpy.Raster("down_slp_ang.tif") / deg) - 0.5,
                  Con(arcpy.Raster("down_slp_ang.tif") >= 10,
                      21.91 * Sin(arcpy.Raster("down_slp_ang.tif") / deg) - 0.96)))
m_ls = rusle_l * rusle_s

# calculate C factors
ndvi = arcpy.Raster(ndvi)
ndvi_veg = CellStatistics(ndvi, "MAXIMUM")
ndvi_soil = CellStatistics(ndvi, "MINIMUM")
fc = (ndvi - ndvi_soil) / (ndvi_veg - ndvi_soil)
m_c = Con(fc == 0, 1,
          Con(fc > 0 & fc < 78.3, 0.6508 - 0.3436 * Ln(fc),
              Con(fc >= 78.3, 0)))

# calculate P factors
s_c = arcpy.Raster(soil_con)
m_p = Con(s_c == 1, 0.25,
          Con(s_c == 2, 1,
              Con(s_c == 3, 1,
                  Con(s_c == 4, 0,
                      Con(s_c == 5, 0,
                          Con(s_c == 6, 0.5))))))

M = m_a * m_w * m_r * m_l * m_ls * m_p * m_v
M.save("E:\\workspace\\M.tif")
