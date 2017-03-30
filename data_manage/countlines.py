#coding:utf-8
import re

# 统计文件行数
def countlines(filepath):
	count = len(open(filepath,'rU').readlines())
	print(count)

# 
def result(s):
	result = re.findall(r"\d+\.?\d",s)
	return result

# 将输入文件的start到end行输入到输出文件中
def calssification(input_filename, output_filename, start, end):
	f1 = open(input_filename,'r')
	f2 = open(output_filename, 'w+')
	for line in f1.readlines()[start:end]:
		f2.write(line)
	f2.close()
	f1.close() 
	
# calssification('/home/hexu/mobile-data/new_data/result/preds6.txt','/home/hexu/mobile-data/new_data/result/preds66.txt',0,100)
# calssification('/home/hexu/mobile-data/new_data/LUdata/2000LU_dataset.txt','/home/hexu/mobile-data/new_data/LUdata/2000LU_testset.txt', 20000000, 30000000)
countlines('/home/hexu/mobile-data/statistical/stations.txt')
# calssification('/home/hexu/mobile-data/new_data/multiple/1_finaldata6.txt','/home/hexu/mobile-data/new_data/multiple/1_testset6.txt',3000000,3900000)
# calssification('/home/hexu/mobile-data/new_data/LUdata/LU_finaldata.txt','/home/hexu/mobile-data/new_data/LUdata/LU_testdata.txt', 40000, 51000)
# countlines('/home/hexu/mobile-data/new_data/LUdata/LU_testdata.txt')
# countlines('/home/hexu/mobile-data/new_data/markovData/dataset.txt')