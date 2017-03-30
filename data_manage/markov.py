#coding:utf-8

import numpy as np

#计算转移矩阵
def tranfer_matrix(filename):
	count = len(open(filename,'rU').readlines())
	data_list = []
	t_matrix = np.zeros((6,6))
	s_matrix = np.zeros(6)
	f1 = open(filename,'r')
	lines = f1.readlines()
	for line in lines:
		data_list.append(line.strip('\n').split(' ')[0])
	# print len(data_list)
	for i in range(0,count - 1):
		t_matrix[int(data_list[i]) - 1, int(data_list[i + 1]) - 1] = t_matrix[int(data_list[i]) -1 , int(data_list[i + 1]) - 1] + 1
	# print t_matrix
	for j in range(0,6):
		for k in range(0,6):
			s_matrix[j] = s_matrix[j] + t_matrix[j][k]
	# print s_matrix
	for l in range(0,6):
		for m in range(0,6):
			t_matrix[l][m] = t_matrix[l][m] / s_matrix[l]
	print t_matrix
	return t_matrix

def markov(filename):
	count = len(open(filename,'rU').readlines())
	data_list = []
	rights = 0.0
	f1 = open(filename,'r')
	lines = f1.readlines()
	for line in lines:
		data_list.append(line.strip('\n').split(' ')[0])
	for i in range(1,count):
		if(data_list[i] == data_list[i - 1]):
			rights = rights + 1
	print rights
	accurency = rights / count
	print accurency
	

if __name__ == '__main__':
	tranfer_matrix('/home/hexu/mobile-data/24time_finaldata/7_24testdata.txt')
	markov('/home/hexu/mobile-data/24time_finaldata/7_24testdata.txt')