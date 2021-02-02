# coding:utf-8
import os
import arcpy
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")

dqPath = os.getcwd()
# set arcgis workspace
arcpy.env.workspace = dqPath

# 1.添加字段
def addnewfield(shpName):
    try:
        # 添加自动坐落坐落单位代码编号字段  AUTO_ZLDWDM
        arcpy.AddField_management(shpName, "AUTO", "TEXT", field_length = 50)
    except:
        print u"字段已存在"

# 2.1获得分组字段列表
def getgroupfield(shpName, ZLDWDM_Filid):
    data = arcpy.SearchCursor(shpName)
    groupfield = []
    for row in data:
        temp = row.getValue(ZLDWDM_Filid)
        cunCode = temp[0:12]
        groupfield.append(cunCode)
    groupfield = list(set(groupfield))
    #print  groupfield

    del data, row
    return groupfield

#2.创建按照村编号的字典
def addCunDict(shpName):
    ZLDWDM_Filid = 'ZLDWDM'
    # 获取分组字段列表
    groupnum = getgroupfield(shpName, ZLDWDM_Filid)
    for num in groupnum:
        ZLDWDM_Dict[num] = 0  # 根据列表构建初始分组字段对应字典

# 3.定义编号函数
def autoNumberFun(shpName):
    print u'正在编号中，请等待........'
    ZLDWDM_Filid = 'ZLDWDM'
    AUTO_ZLDWDM_Filid = 'AUTO'

    rows = arcpy.UpdateCursor(shpName)
    for row in rows:  # 对要素进行遍历
        temp_ZLDWDM = row.getValue(ZLDWDM_Filid)
        currunt_ZLDWDM = temp_ZLDWDM[0:12]
        # AUTO_ZLDWDM_Value =  row.getValue(AUTO_ZLDWDM_Filid)# 获取AUTO_ZLDWDM_Filid
        # if AUTO_ZLDWDM_Value.strip() == '':
        if currunt_ZLDWDM in ZLDWDM_Dict.keys():  # 对字段进行分组判断
            lsbh = ZLDWDM_Dict[currunt_ZLDWDM]  # 将临时编号赋予
            nextbh = ZLDWDM_Dict[currunt_ZLDWDM] + 1  # 分组增加
            ZLDWDM_Dict[currunt_ZLDWDM] = nextbh  # 更新字典值

            strbh = str(nextbh)  # 将字典值字符串化
            strbh2 = strbh.zfill(7)  # 填充满长度
            value = currunt_ZLDWDM + strbh2  # 构建赋值变量
            row.setValue('AUTO', value)  # 更新对应字段
            print value
            rows.updateRow(row)  # 更新游标
    del rows, row  # 释放游标

# 1.添加字段
shpName = 'DYBH.shp'
addnewfield(shpName)

#2.创建按照村编号的字典
ZLDWDM_Dict = {}
addCunDict(shpName)

# 3.定义编号函数
autoNumberFun(shpName)



