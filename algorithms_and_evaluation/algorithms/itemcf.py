#-*-coding:utf-8-*-
"""

@author: hjx

基于物品的协同过滤算法ItemCF

"""

from algorithms.usercf import UserCF
from collections import defaultdict
import math 
import pickle
import operator
import os

class ItemCF(UserCF):
	
	def __init__(self, ori_train):
		UserCF.__init__(self, ori_train)
	
	def item_similarity(self):
		"""计算物品相似度矩阵"""

		#计算物品相似度矩阵（分子）
		print("ItemCF:")
		C = dict()
		N = defaultdict(int) #物品流行度(被多少用户访问过)
		for user, items in self.trainset.items():
			for i in items:
				C.setdefault(i, dict())
				N[i] += 1
				for j in items:
					if i == j:
						continue
					C[i].setdefault(j, 0)
					C[i][j] += 1
		
		#余弦相似度矩阵（除以分母）
		for i, related_items in C.items():
			for j, cij in related_items.items():
				C[i][j] = cij / math.sqrt(N[i] * N[j])
		return C
	
	def train(self, item_matrix_path="data/item_matrix.pkl"):
		"""训练模型"""

		print("start training")
		try:
			print("loading...")
			fr = open(item_matrix_path, 'rb')
			self.item_matrix = pickle.load(fr)
			fr.close()
			print("Successfully loaded")
		except BaseException:
			print("Fail to load")
			print("Recalculate item_matrix...")
			self.item_matrix = self.item_similarity()
			print("Successfully calculated")
			"""为测试 因要多次实验计算不同的矩阵而先不保存
			parent_path = item_matrix_path[: item_matrix_path.rfind("/")]
			if not os.path.exists(parent_path):
				os.mkdir(parent_path)
			print("Start saving...")
			with open(item_matrix_path, "wb") as f:
				pickle.dump(self.item_matrix, f, 0)
			print("Successfully saved")
			"""
	
	def recommend(self, user, K, L):
		"""推荐

		:param user: 要做推荐的用户
		:param K: 相似用户数
		:param L: 推荐数量
		:return: {推荐图书:喜欢度}
		"""
		
		rank = dict()
		interacted_items = self.trainset[user]
		for i in interacted_items:
			for j, cij in sorted(self.item_matrix[i].items(), 
				key = operator.itemgetter(1), reverse = True)[:K]:
				if j in interacted_items:
					continue
				rank.setdefault(j, 0)
				rank[j] += cij

		return dict(sorted(rank.items(), key = operator.itemgetter(1), 
			reverse = True)[:L])
	
	def recommends(self, users, K, L):
		"""推荐 用于测试

		:param users: 要做推荐的用户列表
		:param K: 相似用户数
		:param L: 推荐数量
		:return: {用户 : 该用户的推荐列表}
		"""
		not_in = 0
		recommends = dict()
		for user in users:
			if user not in self.trainset:
				not_in += 1
				continue
			recommends[user] = list(self.recommend(user, K, L).keys())
			#print(recommends[user])
		#print("not in:",not_in)
		return recommends

