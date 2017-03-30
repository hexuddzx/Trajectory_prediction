#coding:utf-8
import os
import csv
import re
import pdb

# 将数字从字符串中过滤出来
def filter(s):
	result = re.sub("\D","",s)
	return result

# 去除重复项
def get_different(list):
	b_list = dict().fromkeys(list).keys()
	return b_list

# 得到所有的基站号
def  get_stations(input_filename, output_filename):
	f1 = open(input_filename, 'r')
	lines = f1.readlines()
	f2 = open(output_filename, 'w+')
	a_list = []
	for line in lines:
		data_list = line.strip().split(',')
		# device_number = data_list[0]
		# time = filter(data_list[1])
		# number_head = data_list[2]
		station_number = data_list[3] + data_list[4]
		a_list.append(station_number)
		# flag = data_list[5]
		# f2.write(device_number+' '+time+' '+station_number+'\n')
		f2.write(station_number+'\n')
		# reader = csv.reader(open('/home/hexu/mobile-data/WX_basestation_GPS.csv','rb'))
		# for ID,LAC,CELL,lat,lon,fix_lat,fix_lon  in reader:
		# 	if(LAC == data_list[3] and CELL == data_list[4] and lat and lon):
		# 		f2.write(lat + ' ' + lon + '\n')
	f2.close()
	f1.close()
	return a_list


def time_different(input_filename, output_filename):
	f1 = open(input_filename, 'r')
	lines = f1.readlines()
	f2 = open(output_filename, 'w+')
	a_list = []
	i = 0
	
	for line in lines:
		data_list = line.strip().split(',')
		device_number = data_list[0]
		time = filter(data_list[1])
		number_head = data_list[2]
		station_number = data_list[3] + data_list[4]
		f3 = open('/home/hexu/mobile-data/datamanaging/99070810115182195/99070810115182195_sort.txt','r')
		ls = f3.readlines()
		j = 1
		ranking = ''
		for l in ls:
			l = l.strip('\n')
			if(station_number == l):
				ranking = str(j)
				break
			else:
				j = j + 1
		f3.close()  
		if(i>0):
			a_list.append(time)
			time_different = str(int(a_list[i]) - int(a_list[i-1]))
			# print(time_different)
			i = i + 1
		else:
			a_list.append(time)
			time_different = '0'
			i = i + 1
		flag = data_list[5]
		f2.write(device_number+' '+time+' '+ time_different+' '+ranking+'\n')
	f2.close()
	f1.close()

# c_list = get_different(manage_data("/home/hexu/mobile-data/rawData/99070810115182195.txt", "/home/hexu/mobile-data/datamanaging/managed_data.txt"))
# print(len(c_list))
# file = open('/home/hexu/mobile-data/datamanaging/99070810115182195_stations.txt','w')
# for s in c_list:
# 	file.write(s+'\n')
# file.close()

#get data including time_different:
# time_different('/home/hexu/mobile-data/rawData/99070810115182195.txt','/home/hexu/mobile-data/datamanaging/99070810115182195/99070810115182195_frequency.txt')
	
# manage_data('/home/hexu/mobile-data/rawData/99070810115182195.txt','/home/hexu/mobile-data/datamanaging/99070810115182195_allstations.txt')
# get_stations('/home/hexu/mobile-data/rawData/99249785829629798.txt','/home/hexu/mobile-data/test/99249785829629798_stations.txt')
filelist = os.listdir('/home/hexu/mobile-data/rawData')
print(len(filelist))