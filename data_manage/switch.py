#coding:utf-8

# 提取出发生了基站转移的数据
def switch(file1, file2, file3, file4):
	f1 = open(file1, 'r')
	f2 = open(file2, 'r')
	f3 =  open(file3, 'a+')
	f4 =  open(file4, 'a+')
	ls1 = f1.readlines()
	ls2 = f2.readlines()
	targets = []
	preds = []
	for l1 in ls1:
		target = l1.strip('\n')
		targets.append(target)
	for l2 in ls2:
		pred = l2.strip('\n')
		preds.append(pred)
	for i in range(0,len(targets)):
		if i == 0:
			f3.write(targets[i] + '\n')
			f4.write(preds[i] + '\n')
		else:
			if (targets[i] == targets[i - 1]):
				continue
			else:
				f3.write(targets[i] + '\n')
				f4.write(preds[i] + '\n')
	f1.close()
	f2.close()
	f3.close()
	f4.close()

switch('/home/hexu/mobile-data/new_data/result/targets.txt','/home/hexu/mobile-data/new_data/result/preds.txt','/home/hexu/mobile-data/new_data/result/targets1.txt','/home/hexu/mobile-data/new_data/result/preds1.txt')