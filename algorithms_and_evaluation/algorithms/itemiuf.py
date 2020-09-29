#-*-coding:utf-8-*-
"""

@author: hjx

计算物品相似度时惩罚活跃用户的改进ItemCF算法item-IUF

"""

from algorithms.itemcf import ItemCF
from collections import defaultdict
import math 

class ItemIUF(ItemCF):
	
	#没写__init__函数
	def train(self, item_matrix_path="data/itemiuf_matrix.pkl"):
		ItemCF.train(self, item_matrix_path=item_matrix_path)

	def item_similarity(self):
		"""计算物品相似度矩阵 惩罚活跃用户"""
		
		#计算物品相似度矩阵（分子）
		print("ItemIUF:")
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
					C[i][j] += 1. / math.log(1. + len(items)) #惩罚活跃用户
		
		#余弦相似度矩阵（除以分母）
		for i, related_items in C.items():
			for j, cij in related_items.items():
				C[i][j] = cij / math.sqrt(N[i] * N[j])
		return C
