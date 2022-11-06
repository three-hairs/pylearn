# coding=utf-8
import arcpy
from arcpy import env
a=1
env.workspace = "E:\QQVipDownload\创训\路网POI_MASK"
list=["科教_路mask", "企业_路mask", "商业_路mask"]
for i in list:
    arcpy.RasterToPoint_conversion(i, "E:\QQVipDownload\创训\道路核密度/"+i.replace("mask",""), "VALUE")
    j = a/4 * 100
    a = a+1


# arcpy.RasterToPoint_conversion("source.img", "E:/QQVipDownload/创训/核密度_点/", "VALUE")