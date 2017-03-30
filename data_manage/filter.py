#coding:utf-8
import re

def  filter(input_filename,output_filename):
	f1 = open(input_filename, 'r')
	lines = f1.readlines()
	f2 = open(output_filename, 'w+')
	for line in lines:
		oline = result(line)
		f2.write(oline + '\n')
	f2.close()
	f1.close()

def result(s):
	result = re.findall(r"\d+\.?\d",s)
	return result

def filter1(s):
	result = re.sub("\D","",s)
	return result
#print(result('asdasd124234234'))
#filter('/home/hexu/mobile-data/datamanaging/train_dataset.txt','/home/hexu/mobile-data/datamanaging/train_dataset1.txt')
print(filter1("asdasdas1234124"))