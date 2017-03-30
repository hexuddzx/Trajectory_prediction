#-*- coding: utf8 -*-
from pyExcelerator import *
import os
import csv
import re
import pdb

# 将基站的经纬度写入excel中

def location(source_dir):
    filelist = os.listdir(source_dir)
    for filename in filelist:
        if filename:
            w = Workbook()  # 创建一个工作簿
            ws = w.add_sheet('location')  # 创建一个工作表
            ws.write(0, 0, 'lat')  # 在1行1列写入lat(纬度)
            ws.write(0, 1, 'lon')  # 在1行2列写入lon(经度)
            f1 = open(source_dir + '/' + filename, 'r')
            lines = f1.readlines()
            i = 1
            for line in lines:
                data_list = line.strip().split(' ')
                reader = csv.reader(open('/home/hexu/mobile-data/WX_basestation_GPS.csv','rb'))
                for ID, LAC, CELL, lat, lon, fix_lat, fix_lon  in reader:
                    if(LAC == data_list[0] and CELL == data_list[1] and lat and lon):
                            ws.write(i, 0, lat)
                            ws.write(i, 1, lon)
                            i += 1

            w.save(filename + 'locations.xls')  # 保存
    



location('/home/hexu/mobile-data/analysis/99070819249650378')
