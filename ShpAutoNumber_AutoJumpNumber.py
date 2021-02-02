# # coding:utf-8
import os
import arcpy
import sys
import os
import collections
from collections import defaultdict
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
def getgroupfield(shpName,ZLDWDM_Filid,AUTO_ZLDWDM_Filid):
    data = arcpy.SearchCursor(shpName)
    groupfield = []
    for row in data:
        #创建字典
        tempZLDWDM = row.getValue(ZLDWDM_Filid)
        keyValue = tempZLDWDM[0:12]
        groupfield.append(keyValue)
        #创建collections 字典  一个key对应多个value
        autoValue = row.getValue(AUTO_ZLDWDM_Filid)
        if len(autoValue) == 19:
            auto_Dict[keyValue].add(autoValue)
    groupfield = list(set(groupfield))
    #print  groupfield

    del data, row
    return groupfield

#2.创建按照村编号的字典
def addCunDict(shpName,ZLDWDM_Filid,AUTO_ZLDWDM_Filid):
    # 获取分组字段列表
    groupnum = getgroupfield(shpName,ZLDWDM_Filid,AUTO_ZLDWDM_Filid)
    for num in groupnum:
        ZLDWDM_Dict[num] = 0  # 根据列表构建初始分组字段对应字典

# 3.定义编号函数
def autoNumberFun(shpName,ZLDWDM_Filid,AUTO_ZLDWDM_Filid):
    print u'正在编号中，请等待........'

    rows = arcpy.UpdateCursor(shpName)
    for row in rows:  # 对要素进行遍历
        temp_ZLDWDM = row.getValue(ZLDWDM_Filid)
        currunt_key = temp_ZLDWDM[0:12]
        # 获取AUTO_ZLDWDM_Filid
        valueOrigin =  row.getValue(AUTO_ZLDWDM_Filid)
        #如果当前键值在ZLDWDM_Dict字典里面
        if currunt_key in ZLDWDM_Dict.keys():  # 对字段进行分组判断
            # 如果value在autoValue字典里面
            lsbh = ZLDWDM_Dict[currunt_key]  # 将临时编号赋予
            nextbh = ZLDWDM_Dict[currunt_key] + 1  # 分组增加
            ZLDWDM_Dict[currunt_key] = nextbh  # 更新字典值
            # print auto_Dict[currunt_key]
            # print type(auto_Dict[currunt_key])
            if valueOrigin in auto_Dict[currunt_key]:
                print u'编号已存在'
                print valueOrigin
            else:
                strbh = str(nextbh)  # 将字典值字符串化
                strbh2 = strbh.zfill(7)  # 填充满长度
                value = currunt_key + strbh2  # 构建赋值变量
                row.setValue(AUTO_ZLDWDM_Filid, value)  # 更新对应字段
                print u'重新编号'
                print value
                rows.updateRow(row)  # 更新游标
    del rows, row  # 释放游标

# 1.添加字段
shpName = 'DYBH.shp'
addnewfield(shpName)

#2.创建按照村编号的字典
ZLDWDM_Dict = {}
ZLDWDM_Filid = 'ZLDWDM'
AUTO_ZLDWDM_Filid = 'AUTO'
auto_Dict = defaultdict(set)
addCunDict(shpName,ZLDWDM_Filid,AUTO_ZLDWDM_Filid)

# 3.定义编号函数
autoNumberFun(shpName,ZLDWDM_Filid,AUTO_ZLDWDM_Filid)



