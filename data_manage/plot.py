#coding:utf-8
from numpy import *
import matplotlib.pyplot as plt
import matplotlib
import os,sys
import shutil
import re

# 绘制折线图
def main():
	# 颜色列表
	colorList = ['b','g','r','c','m','y','k']
	# 共用的横坐标
	threadList = []
	# threadList[0] = 0
	for i in range(24):
		threadList.append(i)
	# 设置横坐标和纵坐标的名称
	plt.xlabel('num')
	plt.ylabel('cos')
	# 图的标题
	plt.title('test')
	# 要绘制的线的列表
	lines = []
	# 对应的线的名称
	titles = []
	# 第一根线的纵坐标
	dataList1 = []
	f1 = open('/home/hexu/return_home/data/FeatureMatrix/difference.txt','r')
	ls = f1.readlines()
	j = 1
	# dataList1.append(0)
	for l in ls:
		info = float(l.strip('\n'))
		# print(info)
		dataList1.append(info)
		j = j + 1
	# 根据横坐标和纵坐标画第一根线
	line1 = plt.plot(threadList, dataList1, '-')
	# 设置线的颜色宽度等
	plt.setp(line1, color=colorList[0], linewidth=2.0)
	# 线的名称
	# plt.legend(lines, titles)
	plt.savefig('/home/hexu/return_home/plot/different.png', dpi=120)
	#如果是pdf就,plt.savefig('/home/workspace/test.pdf')
	plt.show()

# 绘制散点图
def scatter():
	# 颜色列表
	colorList = ['b','g','r','c','m','y','k']
	# 共用的横坐标
	threadList = []
	# threadList[0] = 0
	for i in range(0,100):
		threadList.append(i)
	# 设置横坐标和纵坐标的名称
	plt.xlabel('num')
	plt.ylabel('rank')
	# 图的标题
	plt.title('test')
	# 要绘制的线的列表
	lines = []
	# 对应的线的名称
	titles = []
	# 第一根线的纵坐标
	dataList1 = []
	f1 = open('/home/hexu/mobile-data/new_data/result/targets66.txt','r')
	ls = f1.readlines()
	j = 1
	# dataList1.append(0)
	for l in ls:
		info = int(l.strip('\n'))
		# print(info)
		dataList1.append(info)
		j = j + 1
	# 根据横坐标和纵坐标画第一根线
	line1 = plt.plot(threadList, dataList1, 'o')
	# 设置线的颜色宽度等
	plt.setp(line1, color=colorList[0], linewidth=2.0)
	# 线的名称
	titles.append('target')
	lines.append(line1)
	# 同理画第二根线
	dataList2 = []
	f2 = open('/home/hexu/mobile-data/new_data/result/preds66.txt','r')
	ls2 = f2.readlines()
	k = 1
	# dataList2.append(0)
	for l2 in ls2:
		dataList2.append(int(l2.strip('\n')))
		k = k + 1
	line2 = plt.plot(threadList, dataList2,'o')
	plt.setp(line2, color=colorList[1], linewidth=2.0)
	titles.append('pred')
	lines.append(line2)
	# plt.legend(lines, titles)
	plt.savefig('/home/hexu/mobile-data/new_data/result/plot6.png', dpi=120)
	#如果是pdf就,plt.savefig('/home/workspace/test.pdf')
	plt.show()

# 去除重复项
def get_different(list):
	b_list = dict().fromkeys(list).keys()
	return b_list

def get_different2(list):
	resultList = []
	for item in list:
            		if not item in resultList:
                    		resultList.append(item)
   	return resultList

# 得到每个用户到过的基站数
def getstations(sourcedir):
	filelist = os.listdir(sourcedir)
	f2 = open('/home/hexu/mobile-data/statistical/stations.txt','a+')
	for filename in filelist:
		if filename:
			name_list = filename.strip().split('.')
			number = name_list[0]
			s_list = []
			f1 = open(sourcedir+'/'+filename,'r')
			lines = f1.readlines()
			for line in lines:
				data_list = line.strip().split(',')
				station_number = data_list[3] + data_list[4]
				s_list.append(station_number)
			b_list = get_different2(s_list)
			f2.write(number + ' ' + str(len(b_list)) + '\n')
			f1.close()
	f2.close()

# 统计用户基站数分布
def statistical():
	# 颜色列表
	colorList = ['b','g','r','c','m','y','k']
	# 共用的横坐标
	threadList = []
	# threadList[0] = 0
	for i in range(105):
		threadList.append(i)
	# 设置横坐标和纵坐标的名称
	plt.xlabel('region_num')
	plt.ylabel('people_num')
	# 图的标题
	plt.title('regions')
	# 第一根线的纵坐标
	dataList1 = []
	num_list = []
	for j in range(105):
		num_list.append(0)
	f1 = open('/home/hexu/mobile-data/region_num.txt','r')
	ls = f1.readlines()
	# dataList1.append(0)
	for l in ls:
		data_list = l.strip('\n').split(',')
		info = int(data_list[1])
		num_list[info] += 1
		# dataList1.append(info)
	# 根据横坐标和纵坐标画第一根线
	line1 = plt.plot(threadList, num_list, '-')
	# 设置线的颜色宽度等
	plt.setp(line1, color=colorList[0], linewidth=2.0)
	# plt.legend(lines, titles)
	plt.savefig('/home/hexu/mobile-data/plots/region_num.png', dpi=120)
	#如果是pdf就,plt.savefig('/home/workspace/test.pdf')
	plt.show()

def sort():
	f1 = open('/home/hexu/mobile-data/region_num.txt','r')
	ls = f1.readlines()
	x = []
	for l in ls:
		data_list = l.strip().split(',')
		regionID = data_list[1]
		x.append(regionID)
	x.sort()
	f2 = open('/home/hexu/mobile-data/sorted_region_num.txt', 'w')
	for i in range(0,len(x)):
		f2.write(x[i]+'\n')
	f2.close()
	f1.close()



if __name__ == '__main__':
	# main()
	# scatter()
	# statistical()
	main()
	# getstations('/home/hexu/mobile-data/rawData')