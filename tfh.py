# _*_coding:utf-8_*_
import pyproj
from pyproj import Proj
from osgeo import ogr
import osgeo.osr as osr
import os
from osgeo import gdal
import numpy as np
from functools import partial
from pyproj import Proj, transform
from functools import partial
from pyproj import Proj, transform

zfmDic = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H',
          9: 'I', 10: 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O',
          16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V',
          23: 'W', 24: 'X', 25: 'Y', 26: 'Z'}
tzmDic = {'500000': 'B', '250000': 'C', '100000': 'D', '50000': 'E',
          '25000': 'F', '10000': 'G', '5000': 'H'}
longDic = {'10000': 0.0625,'50000':0.25}
latDic = {'10000': 0.0416666666666667,'50000':0.166666666666667}
numDic = {v: k for k, v in zfmDic.items()}


def lb_toyx(l, b, ty):
    daihao = ty
    zbx = "epsg" + ":" + daihao
    p1 = pyproj.Proj(init="epsg:4490")  # 定义数据地理坐标系
    p2 = pyproj.Proj(init=zbx)  # 定义转换投影坐标系
    x1, y1 = p1(l, b)
    x2, y2 = pyproj.transform(p1, p2, x1, y1, radians=True)
    return x2, y2

# def lonlat2geo(dataset, lon, lat):
#     '''
#     将经纬度坐标转为投影坐标（具体的投影坐标系由给定数据确定）
#     :param dataset: GDAL地理数据
#     :param lon: 地理坐标lon经度
#     :param lat: 地理坐标lat纬度
#     :return: 经纬度坐标(lon, lat)对应的投影坐标
#     '''
#     prosrs, geosrs = getSRSPair(dataset)
#     ct = osr.CoordinateTransformation(geosrs, prosrs)
#     coords = ct.TransformPoint(lon, lat)
#     return coords[:2]

def lb_toyx(l, b, ty):
    daihao = ty
    zbx = "epsg" + ":" + daihao
    proj_4490 = Proj(init="epsg:4490") # 定义数据地理坐标系
    proj_zbx = pyproj.Proj(init=zbx)# 定义转换投影坐标系
    transformer = partial(transform, proj_4490, proj_zbx)
    x2,y2 = transformer(l, b)
    return x2,y2

def yx_tolb(y, x, ty='4524'):
    daihao = ty
    zbx = "epsg" + ":" + daihao
    p1 = pyproj.Proj(init=zbx)  # 定义转换投影坐标系
    l, b = p1(y, x, inverse=True)
    return l, b


def dms_to_deg(num, sep):  # 定义60进制转换成十进制度函数
    dms = num.split(sep)
    deg = float(dms[0]) + float(dms[1])/60 + float(dms[2])/3600
    return deg


def deg_to_dms(num, sep):  # 定义十进制度转为60进制度函数
    num = num
    sep = sep
    try:
        af0, aft0 = int(num), num - int(num)
    except:
        num = float(num)
        af0, aft0 = int(num), num - int(num)
    aft01, aft02 = int(aft0 * 60), aft0 * 60 - int(aft0 * 60)
    aft03 = float(aft02 * 60)
    if aft03 < 10:
        aft03 = '0' + str(aft03)
    elif aft03 == 60:
        aft03 = '00'
        aft01 += 1
    if aft01 < 10:
        aft01 = '0' + str(aft01)

    dms = str(af0) + sep + str(aft01) + sep + str(aft03)

    return dms


def tfh(l, b, BL='10000'):

    longgitude = float(l)
    latitude = float(b)

    a = int(latitude / 4) + 1  # 计算纬度带字符对应数字 加字典后获取字符

    b = int(longgitude / 6) + 31  # 计算经度带数字码

    c = int(round((4 / latDic[BL]))) - int((latitude % 4) / latDic[BL])  # 获取行号
    d = int((longgitude % 6) / longDic[BL]) + 1  # 获取行号
    print(d)
    aStr = zfmDic[a]
    tfh = aStr + str(b) + tzmDic[BL] + str(c).zfill(3) + str(d).zfill(3)

    return tfh


def get_Swcood(tfh, BL):
    zb = []
    lblist = []
    a = numDic[tfh[0]]
    b = int(tfh[1:3])  # 获取经度带数字码
    c = int(tfh[4:7])  # 获取行号
    d = int(tfh[7:])  # 获取列号
    swL = (b - 31) * 6 + (d - 1) * longDic[BL]
    swB = (a - 1) * 4 + ((4/latDic[BL]) - c) * latDic[BL]
    zb.append(swL)
    zb.append(swB)
    lblist.append(zb)
    zb = []

    nwL = swL  # 获取西北角经度
    nwB = swB + latDic[BL]  # 获取西北角纬度
    zb.append(nwL)
    zb.append(nwB)
    lblist.append(zb)
    zb = []

    neL = swL + longDic[BL]  # 获取东北角经度
    neB = swB + latDic[BL]  # 获取东北角纬度
    zb.append(neL)
    zb.append(neB)
    lblist.append(zb)
    zb = []

    seL = swL + longDic[BL]  # 获取东南角经度
    seB = swB  # 获取东南角纬度
    zb.append(seL)
    zb.append(seB)
    lblist.append(zb)
    zb = []

    return lblist


# print(tfh(105.738963762, 30.222114086))


def draw_tukuang(file, tfh, daihao):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    if not os.path.exists(file):
        print("文件不存在")
        data_source = driver.CreateDataSource(file)
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(int(daihao))
        lyname = file.split('.')[0]
        layer = data_source.CreateLayer(lyname, srs, ogr.wkbPolygon)
        #tfhzd = layer.CreateField(ogr.FieldDefn('TFH', ogr.OFTString))
        tfhzd = ogr.FieldDefn("TFH", ogr.OFTString)
        tfhzd.SetWidth(30)
        layer.CreateField(tfhzd)
    else:
        data_source = driver.Open(file, 1)
        layer = data_source.GetLayer(0)
    tklb = get_Swcood(tfh,BL)
    xntkgs = lb_toyx(tklb[0][0], tklb[0][1], daihao)
    xbtkgs = lb_toyx(tklb[1][0], tklb[1][1], daihao)
    dbtkgs = lb_toyx(tklb[2][0], tklb[2][1], daihao)
    dntkgs = lb_toyx(tklb[3][0], tklb[3][1], daihao)
    feature = ogr.Feature(layer.GetLayerDefn())
    feature.SetField('TFH', tfh)
    layer.SetFeature(feature)
    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(xntkgs[0], xntkgs[1])
    ring.AddPoint(xbtkgs[0], xbtkgs[1])
    ring.AddPoint(dbtkgs[0], dbtkgs[1])
    ring.AddPoint(dntkgs[0], dntkgs[1])
    ring.AddPoint(xntkgs[0], xntkgs[1])
    print(xntkgs[0], xntkgs[1])
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(ring)
    feature.SetGeometry(polygon)
    layer.CreateFeature(feature)
    print('ok')

BL = input('请输入比例尺：')
for tu in ['H48E015020']:

#tu = input('请输入图幅号：')
    draw_tukuang('H48E015020.shp', tu, '4524')
#jwd = yx_tolb(35625051.568,3286949.875,ty='4523')
#ywtfh = tfh(jwd[0],jwd[1])
#print(ywtfh)
print('ok')