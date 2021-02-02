# 房屋编码验算规则  参考《房屋代码编码标准》（JGJT 246-2012）
import pandas as pd
import numpy as np
from docxtpl import DocxTemplate,InlineImage
from docx import shared
import os
file = pd.ExcelFile("Building_data.xlsx")
df = file.parse("Sheet1")

x_data = np.array(df)
x_list = x_data.tolist()

for row in  x_list:
    build_list = []
    lenth = len(row[0])
    a = 0
    while a < lenth-1:
        value = int(row[0][a])
        build_list.append(value)
        a += 1

    if (build_list[0] + 10) % 10 == 0:
        sj = 10
    else:
        sj = (build_list[0] + 10) % 10

    index = 0
    while index < len(build_list):
       # print(f'sj = {sj}',end='    ')
       if (sj % 10) == 0:
           pj_1 = 10 * 2
       else:
           pj_1 = (sj % 10) * 2
       # print(f'pj_1 = {pj_1}', end='    ')

       if  pj_1 % 11 == 0:
           pj = 11
       else:
           pj = pj_1 % 11
       # print(f'余数 = {pj}')
       index += 1
       if (index) == len(build_list):
           continue
       else:
           sj = pj + build_list[index]

    a1 = pj - 1
    # list 转换为字符串
    value25 = "".join([str(x) for x in build_list])

    print(value25, end='\t')
    print(a1, end='\n')
    # print(f'a1 = {a1}')
# 4403030070020300006000002
# 4403030070020300020000017