#_*_coding:utf-8_*_
import pandas as pd
import numpy as np
from docxtpl import DocxTemplate,InlineImage
from docx import shared
import os
# have_content = False


file = pd.ExcelFile("data\小于400三调精度.xlsx")
df = file.parse("小于400三调精度")

x_data = np.array(df)
x_list = x_data.tolist()

index = 0
while index<len(x_list):
    tpl = DocxTemplate("插图模板.docx")
    values= x_list[index]
    # values.pop()
    file_name = "data\\文档\\" + str(x_list[index][0]) + ".docx"
    gaoqing_name = "data\\高清\\" + x_list[index][3] + ".tif"
    update_name = "data\\更新\\" + x_list[index][3] + ".tif"

    if os.path.exists(gaoqing_name) == True:
        if os.path.exists(update_name):
            lableID = values[1]
            context = \
                {
                    "col_labels": ["序号", "ID", "行政区代码", "地块序号", "地块面积（平方米）", \
                                   "地块面积（亩）", "核查结果"],
                    "infos": [InlineImage(tpl, gaoqing_name, width=shared.Cm(7.75), height=shared.Cm(7)),
                              InlineImage(tpl, update_name, width=shared.Cm(9.52), height=shared.Cm(6.8))],
                    # "infos1": [InlineImage(tpl, gaoqing_name, width=shared.Cm(7.75), height=shared.Cm(7))],
                    # "infos2": [InlineImage(tpl, update_name, width=shared.Cm(9.52), height=shared.Cm(6.8))],
                    "tbl_contents": [{"cols": values}],

                }
            tpl.render(context)

            tpl.save(file_name)
            # print(context)
            # print(index)


        else:
            print(update_name)

    else:
        print(gaoqing_name)
    index += 1





    # print("ok")


