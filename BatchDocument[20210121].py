#_*_coding:utf-8_*_
import pandas as pd
import numpy as np
from docxtpl import DocxTemplate,InlineImage
from docx import shared
# have_content = False


file = pd.ExcelFile("D:\Python\word\小于400\小于400平米表.xlsx")
df = file.parse("Sheet1")

x_data = np.array(df)
x_list = x_data.tolist()

index = 0
while index<len(x_list):
    tpl = DocxTemplate("插图模板最终版本.docx")
    values = x_list[index]
    file_name = "D:\Python\word\小于400\\文档\\" + str(x_list[index][0]) + ".docx"
    img_name = "D:\Python\word\小于400\\截图\\" + x_list[index][3] + ".tif"
    print(img_name)

    context = \
        {
        "col_labels": ["序号", "ID", "行政区代码", "地块序号", "地块面积（平方米）", \
                       "地块面积（亩）", "核查结果"],
        "infos": [InlineImage(tpl, img_name, width=shared.Cm(9.52), height=shared.Cm(6.8))],
        "tbl_contents": [{"cols": values}]
         }
    tpl.render(context)

    tpl.save(file_name)
    # print(context)
    # print(index)

    index+=1
    print("ok")


