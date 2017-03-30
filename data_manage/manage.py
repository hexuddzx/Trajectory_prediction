#coding:utf-8
import os,sys
import shutil
import re

# 将数字从字符串中提取出来
def filter(s):
	result = re.sub("\D","",s)
	return result

# 去除重复项
def get_different(list):
	b_list = dict().fromkeys(list).keys()
	return b_list

# 对原数据进行过滤
def filtered(sourcedir):
	filelist = os.listdir(sourcedir)
	for filename in filelist:
		# print(filename)
		if filename:
			sourcefile = sourcedir+ '/' +filename
			if(len(open(sourcefile,'rU').readlines()) >= 648):		
				shutil.copy(sourcefile,'/home/hexu/mobile-data/new_data/648_filteredData')

# 将符合基站数条件的用户数据挑出来
def filtered1(sourcedir,standarddir):
	filelist1 = os.listdir(sourcedir)
	filelist2 = os.listdir(standarddir)
	for filename2 in filelist2:
		if filename2:
			name_list = filename2.strip().split('_')
			number = name_list[0]
			for filename1 in filelist1:
				if filename1 == number +'.txt' :
					sourcefile = sourcedir + '/' + filename1
					shutil.copy(sourcefile,'/home/hexu/mobile-data/new_data/2000_finalData')


		
# 得到所有的基站号
def getstations(sourcedir):
	filelist = os.listdir(sourcedir)
	for filename in filelist:
		if filename:
			name_list = filename.strip().split('.')
			number = name_list[0]
			f1 = open(sourcedir+'/'+filename,'r')
			lines = f1.readlines()
			f2 = open('/home/hexu/mobile-data/24time_filterstations/'+number+'_allstations.txt','w+')
			for line in lines:
				data_list = line.strip().split(',')
				station_number = data_list[3] + data_list[4]
				f2.write(station_number+'\n')
			f2.close()
			f1.close()

# 把基站号按出现的频率排序
def sort(sourcedir):
	filelist = os.listdir(sourcedir)
	for filename in filelist:
		if filename:
			name_list = filename.strip().split('_')
			number = name_list[0]
			f1 = open(sourcedir+'/'+filename,'r')
			lines = f1.readlines()			
			x = {}
			for line in lines:
				line = line.strip('\n')
				if (x.has_key(line)):
					x[line] = x[line] + 1
				else:
					x[line] = 1
			x = sorted(x.iteritems(), key = lambda asd:asd[1], reverse = True)
			# if(len(x) > 10):
			f2 = open('/home/hexu/mobile-data/24time_sortedstations/'+number+'_sortedstations.txt','w+')
			for i in range(0,len(x)):
				f2.write(x[i][0]+'\n')
			f2.close()
			f1.close()


# 将设备号，时间，与上次记录之间的时间差，基站出现频率排名写入文件
def manage(sourcedir):
	filelist = os.listdir(sourcedir)
	for filename in filelist:
		if filename:
			# name_list = filename.strip().split('_')
			# number = name_list[0]
			f1 = open(sourcedir+'/'+filename,'r')
			lines = f1.readlines()
			f2 = open('/home/hexu/mobile-data/datamanaging/final_data.txt','a+')
			a_list = []
			i = 0
			for line in lines:
				data_list = line.strip().split(',')
				device_number = data_list[0]
				time = filter(data_list[1])
				number_head = data_list[2]
				station_number = data_list[3] + data_list[4]
				f3 = open('/home/hexu/mobile-data/sortedstations/'+device_number+'_sortedstations.txt','r')
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

# 得到前几个时间点和本时间点所在的基站频率排名
def get_frequency(sourcedir):
	filelist = os.listdir(sourcedir)
	for filename in filelist:
		if filename:
			# name_list = filename.strip().split('_')
			# number = name_list[0]
			f1 = open(sourcedir+'/'+filename,'r')
			lines = f1.readlines()
			# f2 = open('/home/hexu/mobile-data/new_data/two_final_data.txt','a+')
			ranking_list = []  #频率排名数组
			time_list = []  #时间数组
			# tf_list = []   #时间差数组
			i = 0
			k = 0
			for line in lines:
				data_list = line.strip().split(',')
				device_number = data_list[0]
				time = filter(data_list[1])
				station_number = data_list[3] + data_list[4]
				f2 = open('/home/hexu/mobile-data/24time_finaldata/finaldata.txt','a+')
				f3 = open('/home/hexu/mobile-data/24time_sortedstations/'+device_number+'_sortedstations.txt','r')
				ls = f3.readlines()
				j = 1
				ranking = ''
				for l in ls:
					l = l.strip('\n')
					if(station_number == l):
						if(j > 10):                 #将频率排名在5之后的基站都归入第六类
							j = 11
						ranking = str(j)
						ranking_list.append(ranking)
						break
					else:
						j = j + 1
				f3.close()  
				if(k>0):
					time_list.append(time)
					# time_different = str(int(time_list[k]) - int(time_list[k-1]))
					# tf_list.append(time_different)
					k = k + 1
				else:
					time_list.append(time)
					# time_different = '0'
					# tf_list.append(time_different)
					k = k + 1
				if(i >= 7):
					for x in range(0,7):
						f2.write(ranking_list[i - 7 + x] + ' ')
					f2.write(ranking_list[i] + '\n')
					i = i + 1
				else:
					i = i + 1
				f2.close()
			# f2.close()
			f1.close()
					
# 得到RNN需要的数据集
def rnndata(sourcedir):
	filelist = os.listdir(sourcedir)
	for filename in filelist:
		if filename:
			# name_list = filename.strip().split('_')
			# number = name_list[0]
			f1 = open(sourcedir+'/'+filename,'r')
			lines = f1.readlines()
			f2 = open('/home/hexu/mobile-data/new_data/dataset/rnndata.txt','a+')
			a_list = []
			i = 0
			for line in lines:
				data_list = line.strip().split(',')
				device_number = data_list[0]
				time = filter(data_list[1])
				number_head = data_list[2]
				station_number = data_list[3] + data_list[4]
				f3 = open('/home/hexu/mobile-data/new_data/sortedstations/'+device_number+'_sortedstations.txt','r')
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
				f2.write(time+' '+ time_different+' '+ranking+'\n')
			f2.close()
			f1.close()

#得到马尔科夫模型所需的数据集
def markovData(sourcedir):
	filelist = os.listdir(sourcedir)
	for filename in filelist:
		if filename:
			# name_list = filename.strip().split('_')
			# number = name_list[0]
			f1 = open(sourcedir+'/'+filename,'r')
			lines = f1.readlines()
			# f2 = open('/home/hexu/mobile-data/new_data/two_final_data.txt','a+')
			ranking_list = []  #频率排名数组
			time_list = []  #时间数组
			tf_list = []   #时间差数组
			i = 0
			k = 0
			for line in lines:
				data_list = line.strip().split(',')
				device_number = data_list[0]
				time = filter(data_list[1])
				station_number = data_list[3] + data_list[4]
				f2 = open('/home/hexu/mobile-data/new_data/markovData/dataset.txt','a+')
				f3 = open('/home/hexu/mobile-data/new_data/sortedstations/'+device_number+'_sortedstations.txt','r')
				ls = f3.readlines()
				j = 1
				ranking = ''
				for l in ls:
					l = l.strip('\n')
					if(station_number == l):
						if(j > 5):                 #将频率排名在5之后的基站都归入第六类
							j = 6
						ranking = str(j)
						ranking_list.append(ranking)
						break
					else:
						j = j + 1
				f3.close()  
				if(k>0):
					time_list.append(time)
					time_different = str(int(time_list[k]) - int(time_list[k-1]))
					tf_list.append(time_different)
					k = k + 1
				else:
					time_list.append(time)
					# time_different = '0'
					# tf_list.append(time_different)
					k = k + 1
				f2.write(ranking_list[i] + '\n')
				i = i + 1
				f2.close()
			# f2.close()
			f1.close()

# 选出状态是LU-PERIODIC的记录，以减少冗余信息的干扰
def get_LUdata(sourcedir):
	filelist = os.listdir(sourcedir)
	for filename in filelist:
		if filename:
			# name_list = filename.strip().split('_')
			# number = name_list[0]
			f1 = open(sourcedir+'/'+filename,'r')
			lines = f1.readlines()
			# f2 = open('/home/hexu/mobile-data/new_data/two_final_data.txt','a+')
			ranking_list = []  #频率排名数组
			time_list = []  #时间数组
			tf_list = []   #时间差数组
			i = 0
			k = 0
			for line in lines:
				data_list = line.strip().split(',')
				device_number = data_list[0]
				time = filter(data_list[1])
				station_number = data_list[3] + data_list[4]
				state = data_list[5]
				f2 = open('/home/hexu/mobile-data/new_data/LUdata/2000LU_dataset.txt','a+')
				f3 = open('/home/hexu/mobile-data/new_data/2000_sortedstations/'+device_number+'_sortedstations.txt','r')
				ls = f3.readlines()
				j = 1
				ranking = ''
				for l in ls:
					l = l.strip('\n')
					if(station_number == l):
						if(j > 5):                 #将频率排名在5之后的基站都归入第六类
							j = 6
						ranking = str(j)
						# ranking_list.append(ranking)
						break
					else:
						j = j + 1
				f3.close()
				if state == 'LU-PERIODIC':
					ranking_list.append(ranking)
					if(i >= 7):
						for x in range(0,7):
							f2.write(ranking_list[i - 7 + x] + ' ')
						f2.write(ranking_list[i] + '\n')
					i = i + 1
				
				f2.close()
			f1.close()

# 把活跃基站数满足条件的设备号筛选出来
def station_num():
	f1 = open('/home/hexu/mobile-data/statistical/stations.txt', 'r')
	f2 = open('/home/hexu/mobile-data/statistical/lessthan50.txt', 'a+')
	ls = f1.readlines()
	for l in ls:
		data_list = l.strip('\n').split(' ')
		info = int(data_list[1])
		if info <= 50:
			f2.write(l)
	f1.close()
	f2.close()

# 将指定设备的记录按天分割

def data_day(device_number):
	f1 = open('/home/hexu/mobile-data/rawData/' + device_number + '.txt', 'r')
	lines = f1.readlines()
	for line in lines:
		data_list = line.strip().split(',')
		time = filter(data_list[1])
		station_number = data_list[3] + data_list[4]
		date = time[4] + time[5] + time[6] + time[7]
		f2 = open('/home/hexu/mobile-data/analysis/' + device_number + '/' + device_number + '_' + date + '.txt', 'a+')
		f2.write(data_list[3] + ' ' + data_list[4] + '\n')
		f2.close()
	f1.close()

# filtered('/home/hexu/mobile-data/rawData')
# getstations('/home/hexu/mobile-data/24time_data')
# sort('/home/hexu/mobile-data/24time_filterstations')
# filtered1('/home/hexu/mobile-data/new_data/2000_filteredData','/home/hexu/mobile-data/new_data/2000_sortedstations')
# manage('/home/hexu/mobile-data/test')
get_frequency('/home/hexu/mobile-data/24time_data')
# rnndata('/home/hexu/mobile-data/new_data/finalData')
# markovData('/home/hexu/mobile-data/new_data/finalData')
# get_LUdata('/home/hexu/mobile-data/new_data/2000_finalData')

#对数据进行统计分析

# getstations('/home/hexu/mobile-data/rawData')

# 筛选基站数满足条件的设备号
# station_num()

# data_day('99885120581854226')