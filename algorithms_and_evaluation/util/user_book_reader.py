#-*-coding:utf-8-*-
"""

@author: hjx

从数据库中读取用户访问数据即user_book表
将读出的数据分为训练集和测试集

"""

import random
import pymysql


def read_rating_data(k=0, M=8, seed=1):
    """载入评分数据

    :param k: 第k份作为测试集
    :param M: 数据分为M份
    :param seed: 随机数种子
    :return: 训练集[[uid,iid]]，测试集[[uid,iid]]
    """
    trainset = list()
    testset = list()
    conn = pymysql.connect(user = "root", password = "", database = "bookdb")
    cur = conn.cursor()
    cur.execute('SELECT * FROM user_book')
    result = cur.fetchall()
    
    random.seed(seed)
    for (bid, uid,) in result:
        if random.randint(0,M) == k:
            testset.append([uid, bid])
        else:
            trainset.append([uid, bid])
    return trainset, testset



