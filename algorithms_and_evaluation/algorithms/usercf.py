#-*-coding:utf-8-*-
"""

@author: hjx

基于用户的协同过滤算法UserCF

"""

from collections import defaultdict
import math 
import pickle
import operator
import os


class UserCF(object):
	
	def __init__(self, ori_train):
		self.trainset = dict()
		for user, item in ori_train:
			self.trainset.setdefault(user, set())
			self.trainset[user].add(item)

			
	def user_similarity(self):
		"""计算用户兴趣相似度矩阵"""
		print("UserCF: ")
		#建立物品-用户倒排表
		item_users = dict()
		for user, items in self.trainset.items():
			for item in items:
				item_users.setdefault(item, set())
				item_users[item].add(user)

		#计算用户之间共同兴趣物品个数矩阵（分子）
		C = dict()
		N = defaultdict(int) #用户访问物品数
		for i,users in item_users.items():
			for u in users:
				C.setdefault(u, dict())
				N[u] += 1
				for v in users:
					if u == v:
						continue
					C[u].setdefault(v, 0)
					C[u][v] += 1
		
		#计算用户兴趣的余弦相似度矩阵（除以分母）
		for u, related_users in C.items():
			for v, cuv in related_users.items():
				C[u][v] = cuv / math.sqrt(N[u] * N[v])
		
		return C
		
	def train(self, user_matrix_path="data/user_matrix.pkl"):
		"""训练模型"""
		print("start training")
		try:
			print("loading...")
			fr = open(user_matrix_path, 'rb')
			self.user_matrix = pickle.load(fr)
			fr.close()
			print("Successfully loaded")
		except BaseException:
			print("Fail to load")
			print("Recalculate user_matrix...")
			self.user_matrix = self.user_similarity()
			print("Successfully calculated")
			"""
			为测试 因要多次实验计算不同的矩阵而先不保存
			parent_path = user_matrix_path[: user_matrix_path.rfind("/")]
			if not os.path.exists(parent_path):
				os.mkdir(parent_path)
			print("Start saving...")
			with open(user_matrix_path, "wb") as f:
				pickle.dump(self.user_matrix, f, 0)
			print("Successfully saved")
			"""

	def recommend(self, user, K, L):
		"""推荐 计算用户对物品的感兴趣程度

		:param user: 要做推荐的用户
		:param K: 相似用户数
		:param L: 推荐数量
		:return: {推荐书籍:喜欢度}
		"""
		
		rank = dict()
		interacted_items = self.trainset[user]
		for v, cuv in sorted(self.user_matrix[user].items(), 
			key = operator.itemgetter(1), reverse = True)[:K]:
				for i in self.trainset[v]:
					if i in interacted_items:
						continue
					rank.setdefault(i, 0.)
					rank[i] += cuv

		return dict(sorted(rank.items(), key = operator.itemgetter(1), 
			reverse = True)[:L])
	
	def recommends(self, users, K, L):
		"""推荐 用于测试

		:param users: 要做推荐的用户列表
		:param K: 相似用户数
		:param L: 推荐数量
		:return: {用户 : 该用户的推荐列表}
		"""

		recommends = dict()
		for user in users:
			
			if user not in self.user_matrix:
				continue
			
			recommends[user] = list(self.recommend(user, K, L).keys())
			#print(recommends[user])
		return recommends
