# coding=utf-8
import arcpy
import codecs

import sys
reload(sys)
sys.setdefaultencoding('utf8')


def getCount( fc):

    r = arcpy.GetCount_management(fc)
    return int(r.getOutput(0))


def exportTableToCSV( fc, outCSV, userFieldList=[],
                     delimiter=",",
                     exportOID=True,
                     nullFormat=None,
                     exportGeom=False,
                     quoteStrings=True):

    arcpy.AddMessage("\nOptions selected: \nFields: %s \nDelimiter: '%s' Export OID: %s Export Geom: %s" % (
    userFieldList, delimiter, exportOID, exportGeom))
    try:
        f = open(outCSV, 'w')
        f.close()
    except:
        arcpy.AddMessage("Cannot open output file!\n%s" % outCSV)
        return False

    fieldList = arcpy.ListFields(fc)
    textFieldsIndex = []

    fieldList2 = []
    arcpy.AddMessage("\nFields found in feature class:")
    for field in fieldList:
        arcpy.AddMessage("%s (%s)" % (field.name, field.type))
        if field.type == 'OID':
            if exportOID:
                fieldList2.append(field)
            else:
                continue
        elif field.type == 'Geometry':
            if exportGeom:
                fieldList2.append(field)
            else:
                continue
        else:
            if len(userFieldList) > 0:

                if field.name in userFieldList:
                    fieldList2.append(field)
            elif len(userFieldList) == 0:

                fieldList2.append(field)
    arcpy.AddMessage("\n")

    index = 0
    for field in fieldList2:
        if field.type == 'String':
            textFieldsIndex.append(index)
        index += 1

    header = ""
    fieldList3 = []
    for field in fieldList2:
        fieldName = field.name
        fieldList3.append(fieldName)
        if quoteStrings:
            header += '"%s"%s' % (fieldName, delimiter)
        else:
            header += '%s%s' % (fieldName, delimiter)

    header = header[:-1]
    arcpy.AddMessage("Writing header: %s" % header)
    f = codecs.open(outCSV, encoding='utf-8', mode='a+')
    f.write(header)
    f.close()

    arcpy.AddMessage("CSV out: Checking contents of text fields for trouble:")
    arcpy.AddMessage("Text Fields: %s" % textFieldsIndex)
    numFields = len(fieldList3)
    rowCount = 0
    totalRows = getCount(fc)
    arcpy.AddMessage("Starting export...")
    import io
    f = io.open(outCSV, encoding='utf-8', mode='a+')
    with arcpy.da.SearchCursor(fc, fieldList3) as c:
        for row in c:
            rowCount += 1
            if rowCount > sys.maxsize:
                return True
            line = ""
            for i in range(numFields):
                contents = row[i]
                if i in textFieldsIndex:

                    if contents is not None:
                        contents = contents.replace(delimiter, "")
                        if quoteStrings:
                            line += '"%s"%s' % (contents, delimiter)
                        else:
                            line += '%s%s' % (contents, delimiter)
                    else:

                        line += '%s%s' % (contents, delimiter)
                else:

                    line += '%s%s' % (contents, delimiter)

            line = line[:-1]
            f.write(u'\n{}'.format(line))
            if rowCount % 1000 == 0:

                f.close()
                f = codecs.open(outCSV, encoding='utf-8', mode='a+')
                arcpy.AddMessage("\rExported row %s of %s..." % (rowCount, totalRows)),

    f.close()
    arcpy.AddMessage("\nAll done. %s rows exported." % rowCount)


path1 = "E:/QQVipDownload/创训/poi分块/poi_road.mdb/poi/"
path2 = "E:/"
arcpy.env.workspace = "E:/QQVipDownload/创训/道路核密度/科居公企商字段计算/科居公企商111.shp"
walk = arcpy.da.Walk()
print "read finish"
for dirpath, dirnames, filenames in walk:
    for filename in filenames:
       #print dirnames
        data = dirpath+"/"+filename
        outCSV = path2 + filename+".csv"
        userFieldList = ["number", "居住KR", "科教KR", "公服KR", "商业KR", "企业KR"]
        exportTableToCSV(data, outCSV, userFieldList)
