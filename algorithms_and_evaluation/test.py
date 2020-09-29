#-*-coding:utf-8-*-
"""

@author: hjx

评测算法性能

"""

from algorithms import usercf
from algorithms import itemcf
from algorithms import useriif
from algorithms import itemiuf
from util import user_book_reader
from util import evaluation
import time


#usercf 将数据分成8份，选取不同的k值进行8次实验，避免过拟合

recall = 0
precision = 0
coverage = 0
popularity = 0

for k in range(0, 8):
	#生成训练集和测试集 [(uid, iid)]
	trainset,testset = user_book_reader.read_rating_data(k=k)
	print("训练集数量：" + str(len(trainset)))
	print("测试集数量：" + str(len(testset)))

	#training
	ucf = usercf.UserCF(trainset)
	ucf.train()


	#评测算法性能
	test = dict()
	for user, item in testset:
		test.setdefault(user, list())
		test[user].append(item)
	recommends = ucf.recommends(test.keys(), 20, 30)

	#1.计算召回率
	recall += evaluation.recall(recommends, test)
	#2.计算准确率
	precision += evaluation.precision(recommends, test)
	#3.计算覆盖率
	coverage += evaluation.coverage(recommends, trainset)
	#4.计算新颖度
	popularity += evaluation.popularity(recommends, trainset)


average_recall = recall / 8.0
average_precision = precision / 8.0
average_coverage = coverage / 8.0
average_popularity = popularity / 8.0
print("usercf性能：")
print(average_recall)
print(average_precision)
print(average_coverage)
print(average_popularity)


#useriif 将数据分成8份，选取不同的k值进行8次实验，避免过拟合
recall = 0
precision = 0
coverage = 0
popularity = 0

for k in range(0, 8):
	#生成训练集和测试集 [(uid, iid)]
	trainset,testset = user_book_reader.read_rating_data(k=0)
	print("训练集数量：" + str(len(trainset)))
	print("测试集数量：" + str(len(testset)))
	#training
	uiif = useriif.UserIIF(trainset)
	uiif.train()

	#评测算法性能
	test = dict()
	for user, item in testset:
		test.setdefault(user, list())
		test[user].append(item)
	recommends = uiif.recommends(test.keys(), 20, 30)

	#1.计算召回率
	recall += evaluation.recall(recommends, test)
	#2.计算准确率
	precision += evaluation.precision(recommends, test)
	#3.计算覆盖率
	coverage += evaluation.coverage(recommends, trainset)
	#4.计算新颖度
	popularity += evaluation.popularity(recommends, trainset)
	

#8次实验的平均值
average_recall = recall / 8.0
average_precision = precision / 8.0
average_coverage = coverage / 8.0
average_popularity = popularity / 8.0
print("useriif性能：")
print(average_recall)
print(average_precision)
print(average_coverage)
print(average_popularity)


#itemcf 将数据分成8份，选取不同的k值进行8次实验，避免过拟合
recall = 0
precision = 0
coverage = 0
popularity = 0

for k in range(0, 8):
	#生成训练集和测试集 [(uid, iid)]
	trainset,testset = user_book_reader.read_rating_data(k=0)
	print("训练集数量：" + str(len(trainset)))
	print("测试集数量：" + str(len(testset)))
	#training
	icf = itemcf.ItemCF(trainset)
	icf.train()

	#评测算法性能
	test = dict()
	for user, item in testset:
		test.setdefault(user, list())
		test[user].append(item)
	recommends = icf.recommends(test.keys(),20, 30)

	#1.计算召回率
	recall += evaluation.recall(recommends, test)
	#2.计算准确率
	precision += evaluation.precision(recommends, test)
	#3.计算覆盖率
	coverage += evaluation.coverage(recommends, trainset)
	#4.计算新颖度
	popularity += evaluation.popularity(recommends, trainset)

#8次实验的平均值
average_recall = recall / 8.0
average_precision = precision / 8.0
average_coverage = coverage / 8.0
average_popularity = popularity / 8.0
print("itemcf性能：")
print(average_recall)
print(average_precision)
print(average_coverage)
print(average_popularity)


#itemiuf 将数据分成8份，选取不同的k值进行8次实验，避免过拟合
recall = 0
precision = 0
coverage = 0
popularity = 0

for k in range(0, 8):
	#生成训练集和测试集 [(uid, iid)]
	trainset,testset = user_book_reader.read_rating_data(k=0)
	print("训练集数量：" + str(len(trainset)))
	print("测试集数量：" + str(len(testset)))
	#training
	iiuf = itemiuf.ItemIUF(trainset)
	iiuf.train()

	#评测算法性能
	test = dict()
	for user, item in testset:
		test.setdefault(user, list())
		test[user].append(item)
	recommends = iiuf.recommends(test.keys(), 20, 30)

	#1.计算召回率
	recall += evaluation.recall(recommends, test)
	print(" 召回率 " + str(recall))
	#2.计算准确率
	precision += evaluation.precision(recommends, test)
	print(" 准确率 " + str(precision))
	#3.计算覆盖率
	coverage += evaluation.coverage(recommends, trainset)
	print(" 覆盖率 " + str(coverage))
	#4.计算新颖度
	popularity += evaluation.popularity(recommends, trainset)
	print(" 新颖度 " + str(popularity))

#8次实验的平均值
average_recall = recall / 8.0
average_precision = precision / 8.0
average_coverage = coverage / 8.0
average_popularity = popularity / 8.0
print("itemiuf性能：")
print(average_recall)
print(average_precision)
print(average_coverage)
print(average_popularity)

































