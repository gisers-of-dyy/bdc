# 身份证验算规则链接  https://jingyan.baidu.com/article/72ee561abd962fe16038df48.html
import pandas as pd
import numpy as np
from docxtpl import DocxTemplate,InlineImage
from docx import shared
import os
file = pd.ExcelFile("IDCard_data.xlsx")
df = file.parse("Sheet1")

x_data = np.array(df)
x_list = x_data.tolist()
wi = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
checkCode = [1,0,'X',9,8,7,6,5,4,3,2]

for row in  x_list:
    IDCard_list = []
    lenth = len(row[0])
    if lenth < 18:
        print("身份证{row[0]}不满足18位长度！")
    else:
        a = 0
        while a < lenth-1:
            value = int(row[0][a])
            IDCard_list.append(value)
            a += 1

        # 身份证最后一位
        last_value = row[0][lenth-1]
        b = 0
        sum  = 0
        while b < len(IDCard_list):
            value = IDCard_list[b] *wi[b]
            sum += value
            b += 1
        Y = sum % 11
        cal_value = checkCode[Y]

        if last_value == 'X' and cal_value == 'X':
            pass
        elif int(last_value) == cal_value:
            pass
        else:
            print(f'身份证{row[0]}不满足编码规则！')
