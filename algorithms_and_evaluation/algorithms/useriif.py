#-*-coding:utf-8-*-
"""

@author: hjx

计算用户兴趣相似度时惩罚热门物品的改进UserCF算法User-IIF

"""

from algorithms.usercf import UserCF
from collections import defaultdict
import math 

class UserIIF(UserCF):

	def train(self, user_matrix_path="data/useriif_matrix.pkl"):
		UserCF.train(self, user_matrix_path=user_matrix_path)
	
	def user_similarity(self):
		"""计算用户兴趣相似度矩阵 对热门物品惩罚"""
		print("UserIIF")
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
					C[u][v] += 1.0 / math.log(1. + len(item_users[i]))
		
		#计算用户兴趣的余弦相似度矩阵（除以分母）
		for u, related_users in C.items():
			for v, cuv in related_users.items():
				C[u][v] = cuv / math.sqrt(N[u] * N[v])
		
		return C

