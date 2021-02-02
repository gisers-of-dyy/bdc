# coding:utf-8
import os
import arcpy
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# 实现根据分组最大值续编号功能
# get current dqPath
dqPath = os.getcwd()
djzq = {}
# set arcgis workspace
arcpy.env.workspace = dqPath

# 1.添加字段
def addnewfield(shpName, south_x,west_y):
    try:
        arcpy.AddField_management(shpName, south_x, "DOUBLE", 18, 10)
        arcpy.AddField_management(shpName, west_y, "DOUBLE", 18, 10)
        arcpy.AddField_management(
            shpName, "DJZQDM", "TEXT", field_length=50)  # 添加DJZQDM字段
        arcpy.AddField_management(shpName, 'PARCEL_NO', "TEXT", field_length=50)
        arcpy.AddField_management(shpName, 'BDCDM', "TEXT", field_length=50)
    except:
        print u"字段已存在"

# 2.获取西南角坐标
def setvalue(shpName):
    print '正在进行坐标赋值......'
    desc = arcpy.Describe(shpName)
    shapefieldname = desc.ShapeFieldName
    rows = arcpy.UpdateCursor(shpName)
    for row in rows:
        feat = row.getValue(shapefieldname)
        minX = feat.extent.XMin
        minY = feat.extent.YMin
        # print minX
        # print minY
        row.south_x = minY
        row.west_y = minX

        rows.updateRow(row)
    del row, rows
    print '已完成坐标赋值'

# 3.1获得分组字段列表
def getgroupfield(shpName, DJZQDMFilid):
    data = arcpy.SearchCursor(shpName)
    groupfield = []
    for row in data:
        groupfield.append(row.getValue(DJZQDMFilid))

    groupfield = list(set(groupfield))
    del data, row
    return groupfield

# 3.获取已有最大编号
def getmaxnum(shpName):
    DJZQDMFilid = 'DJZQDM'
    groupnum = getgroupfield(shpName, DJZQDMFilid)  # 获取分组字段列表
    for num in groupnum:
        djzq[num] = 0  # 根据列表构建初始分组字段对应字典

    BDCDMFild = 'BDCDM'
    rows = arcpy.da.UpdateCursor(shpName,(DJZQDMFilid,BDCDMFild))
    for row in rows:
        djzqdm = row[0]
        strnum = row[1]
        if strnum.strip() != '':
            intnum = int(strnum[-5:])
        else:
            intnum = 0
        if intnum > djzq[djzqdm]:
            djzq[djzqdm] = intnum
    for name in djzq.keys():
        print name,djzq[name]
    del rows, row  # 释放游标

# 4.定义编号函数
def bianhao(shpName):
    print u'正在编号中，请等待........'
    countnum = arcpy.GetCount_management(shpName).getOutput(0)
    print countnum
    rows = arcpy.UpdateCursor(
        shpName, "", "", "", "south_x D;west_y D")  # 通过X、Y值排序获取游标
    i = 0
    for row in rows:  # 对要素进行遍历
        currentdjzqdm = row.getValue('DJZQDM')  # 获取分组字段值
        bdcdmv =  row.getValue('BDCDM')# 获取不动产代码
        if bdcdmv.strip() == '':
            if currentdjzqdm in djzq.keys():  # 对字段进行分组判断
                lsbh = djzq[currentdjzqdm]  # 将临时编号赋予
                nextbh = djzq[currentdjzqdm] + 1  # 分组增加
                djzq[currentdjzqdm] = nextbh  # 更新字典值

                strbh = str(nextbh)  # 将字典值字符串化
                strbh2 = strbh.zfill(5)  # 填充满长度
                strbh3 = strbh.zfill(4)#填充四位长度地籍序号
                value = currentdjzqdm + "JC" + strbh2  # 构建赋值变量
                djhvalue = "SZ" + currentdjzqdm[6:] + strbh3 + "000" #构建地籍号

                row.setValue('BDCDM', value)  # 更新对应字段
                row.setValue('PARCEL_NO',djhvalue)#更新地籍号字段
                i += 1
                print value
            rows.updateRow(row)  # 更新游标

    del rows, row  # 释放游标
    return i

# 定义相交预处理函数
# def interSect(file1, file2, outfile):
#     infc1 = file1
#     infc2 = file2
#     outfc = outfile
#     #arcpy.AddField_management(infc2, "CSMJ", "FLOAT", 10, 2)  # 为宗地图层添加CSMJ字段
#     arcpy.CalculateField_management(
#         infc2, "CSMJ", "!shape.area@squaremeter!", "PYTHON")  # 计算面积
#     #arcpy.AddField_management(infc2, "NBSM", "LONG")  # 添加新的标识码字段
#     #arcpy.AddField_management(infc2, "BDCDM", "TEXT",
#                               #field_length=50)  # 添加BDCDM字段
#     cursor = arcpy.UpdateCursor(infc2)  # 获取游标
#     i = 0
#     for row in cursor:
#         row.NBSM = i  # 新标识码字段赋值
#         i += 1
#         cursor.updateRow(row)  # 更新游标
#
#     del cursor, row  # 释放游标
#
#     newfile = arcpy.Intersect_analysis(
#         [infc1, infc2], outfc, "ALL", "", "INPUT")  # 相交
#     arcpy.AddField_management(newfile, "MJ", "FLOAT", 10, 2)  # 添加相交结果mj字段
#     arcpy.CalculateField_management(
#         newfile, "MJ", "!shape.area@squaremeter!", "PYTHON")  # 计算相交片块面积
#     arcpy.AddField_management(newfile, "BL", "FLOAT", 10, 4)  # 添加比例字段
#     arcpy.CalculateField_management(
#         newfile, "BL", "!MJ!/!CSMJ!", "PYTHON")  # 计算所占比例
#     with open('jilu.txt', 'w') as f:
#         cur = arcpy.UpdateCursor(newfile)
#         for row in cur:
#             if row.BL < 0.5:
#                 f.write(str(row.NBSM) + '\n')
#                 cur.deleteRow(row)
#
#             cur.updateRow(row)#更新游标
#
#         del cur, row
#
#     return newfile
#def join(tarfile, srcfile):
#     tarfc = tarfile
#     srcfc = srcfile
#     arcpy.JoinField_management(tarfc, 'NBSM', srcfc, 'NBSM', ['DJZQDM'])
# def newjoinfield(shpName):
#     newjoindic = joindic('xj.shp')
#     rows = arcpy.UpdateCursor(shpName)
#     for row in rows:
#         NBSM = row.getValue('NBSM')
#         if NBSM in newjoindic.keys():
#             row.DJZQDM = newjoindic[NBSM]
#             rows.updateRow(row)  # 更新游标
#         else:
#             print u'请核实{}号宗地位置'.format(NBSM)
#
#     del rows, row  # 释放游标
# def joindic(shpName):
#     joindic = {}
#     rows = arcpy.UpdateCursor(shpName)
#     for row in rows:
#         joinkey = row.getValue('NBSM')
#         joinvalue = row.getValue('DJZQDM')
#         joindic[joinkey] = joinvalue
#     del rows, row  # 释放游标
#
#     return joindic

#interSect('DJZQ.shp',shpName,'xj.shp')
# 1.添加字段
shpName = 'part_DYBH.shp'
south_x = 'south_x'
west_y = 'west_y'
addnewfield(shpName,south_x,west_y)

#newjoinfield(shpName)
#2.获取西南角坐标
setvalue(shpName)
#3.获取已有最大编号
getmaxnum(shpName)
#4.定义编号函数
bhnum = bianhao(shpName)
#5.
getmaxnum(shpName)
print '完成{}个宗地图形编号'.format(bhnum)
print 'ok'
