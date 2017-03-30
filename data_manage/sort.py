#coding:utf-8
# 将基站按出现频率排序
def sortbyfrequency(input_filename,output_filename):
	f1 = open(input_filename,'r')
	f2 = open(output_filename, 'w+')
	x = {}
	for line in f1.readlines():
		line = line.strip('\n')
		if (x.has_key(line)):
			x[line] = x[line] + 1
		else:
			x[line] = 1
	x = sorted(x.iteritems(), key = lambda asd:asd[1], reverse = True)
	for i in range(0,len(x)):
		f2.write(x[i][0]+'\n')
	f2.close()
	f1.close()
	# return (x)

# x = {'a':1,'b':2}
# if(x.has_key('c')):
# 	print(x['c'])
# else:
# 	x['c']=3
# 	print(x['c'])
sortbyfrequency('/home/hexu/mobile-data/datamanaging/99070810115182195_allstations.txt','/home/hexu/mobile-data/datamanaging/99070810115182195_sort.txt')
