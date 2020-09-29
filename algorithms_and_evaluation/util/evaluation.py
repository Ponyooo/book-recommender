#-*-coding:utf-8-*-
"""

@author: hjx

各种评测指标实现

"""

import math

def recall(recommends, test):
	"""计算召回率

	:param recommends: 给用户的推荐结果{用户 : 该用户的推荐列表}
	:param test: 测试集{用户 : 该用户感兴趣的物品列表}
	:return: 召回率
	"""

	hit = 0 #预测对的物品数
	total = 0 #用户在测试集上喜欢的物品数
	#temp = 0
	for user, items in recommends.items():
		"""
		if user not in test.keys():
			temp += 1
			continue
		"""
		rec = set(items)
		tes = set(test[user])
		hit += len(rec & tes) #交集
		total += len(rec)
	#print("有多少用户不在test:" + str(temp))
	return hit / (total * 1.0)

def precision(recommends, test):
	"""计算准确率

	:param recommends: 给用户的推荐结果{用户 : 该用户的推荐列表}
	:param test: 测试集{用户 : 该用户感兴趣的物品列表}
	:return: 准确率
	"""

	hit = 0
	total = 0
	for user, items in recommends.items():
		rec = set(items)
		tes = set(test[user])
		hit += len(rec & tes)
		total += len(tes)
	
	return hit / (total * 1.0)

def coverage(recommends, train):
	"""计算覆盖率

	:param recommends: 给用户的推荐结果{用户 : 该用户的推荐列表}
	:param train: 训练集[(uid, iid)]
	:return: 覆盖率
	"""

	rec_items = set() #被推荐的物品集合
	total_items = set() #物品总集合

	for user, items in recommends.items():
		for item in items:
			rec_items.add(item)
	for user, item in train:
		total_items.add(item)

	return len(rec_items) / (len(total_items) * 1.0)

def popularity(recommends, train):
	"""计算平均流行度代表新颖度

	:param recommends: 给用户的推荐结果{用户 : 该用户的推荐列表}
	:param train: 训练集[(uid, iid)]
	:return: 平均流行度
	"""
	
	#先计算训练集中每个物品的流行度
	item_popularity = dict()
	for user, item in train:
		item_popularity.setdefault(item, 0)
		item_popularity[item] += 1
	
	#计算推荐列表中物品的流行度之和
	n = 0 #推荐列表总物品数
	total = 0 #推荐列表物品总流行度
	for user, items in recommends.items():
		for item in items:
			n += 1
			total += math.log(1 + item_popularity[item])
	
	#平均
	return total / (n * 1.0)
