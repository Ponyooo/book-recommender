#-*-coding:utf-8-*-
"""

@author: hjx

对BX三个数据文件的预处理并插入数据库

"""

import pandas as pd
import pymysql
from random import choice

from sqlalchemy import create_engine

#读取三个文件的数据 清除错误行以及未评价的用户
user = pd.read_csv('../data/BX-CSV-Dump/BX-Users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
user.columns = ['userID', 'Location', 'Age']
rating = pd.read_csv('../data/BX-CSV-Dump/BX-Book-Ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1")
rating.columns = ['userID', 'ISBN', 'bookRating']
book = pd.read_csv('../data/BX-CSV-Dump/BX-Books.csv', sep=';', error_bad_lines=False, encoding="latin-1")
book.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']

df = pd.merge(user, rating, on='userID', how='inner')
df.drop(['Location', 'Age'], axis=1, inplace=True)

test1 = df.groupby('userID', as_index = False)['bookRating'].count().reset_index().sort_values('bookRating', ascending=False)
print(test1.shape)
print(test1.tail(10))

#去掉 rarely rated books和 rarely rating users
min_book_ratings = 50
filter_books = df['ISBN'].value_counts() > min_book_ratings
filter_books = filter_books[filter_books].index.tolist()

min_user_ratings = 50
filter_users = df['userID'].value_counts() > min_user_ratings
filter_users = filter_users[filter_users].index.tolist()

df_new = df[(df['ISBN'].isin(filter_books)) & (df['userID'].isin(filter_users))]
"""
print('The original data frame shape:\t{}'.format(df.shape))
print('The new data frame shape:\t{}'.format(df_new.shape))
print('Number of unique books: ', df_new['ISBN'].nunique())
print('Number of unique users: ', df_new['userID'].nunique())
print(df_new.head(5))
"""
#df_new.to_csv('df_new.csv', index=False, encoding='latin-1')
test2 = df_new.groupby('userID', as_index = False)['bookRating'].count().reset_index().sort_values('bookRating', ascending=False)
print(test2.shape)
print(test2.head(20))


#book表仅保留用户行为数据中包含的书籍的信息
tmp = df_new.groupby('ISBN')['bookRating'].count().reset_index().sort_values('bookRating', ascending=False)

print(tmp.shape)
print(tmp.head(10))
"""
print(tmp2.shape)
print(tmp2.head(2))
"""
book_new = pd.merge(book, tmp, on="ISBN", how="inner")
cols = ['bookRating']
book_new.drop(cols, axis=1, inplace=True)
book_new['bid'] = book_new.index+1
"""
print(book_new.head(10))
print(book_new.shape)
"""



#把df_new中不存在于book表的书籍的记录去除
df_new = pd.merge(df_new, book_new, on="ISBN", how="inner")
cols = ['bookTitle', 'bookAuthor', 'yearOfPublication', 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL', 'ISBN']
df_new.drop(cols, axis=1, inplace=True)
"""
print('The new data frame shape:\t{}'.format(df_new.shape))
print('Number of unique books: ', df_new['bid'].nunique())
print('Number of unique users: ', df_new['userID'].nunique())
"""

#把userid重新排序替换
user_new = df_new.groupby('userID', as_index = False)['bookRating'].count().reset_index().sort_values('bookRating', ascending=False)
user_new = user_new.reset_index(drop=True)
user_new['uid'] = user_new.index+1
print(user_new.shape)
print(user_new.tail(10))

#把df_new中对应的userID替换为uid
df_new = pd.merge(df_new, user_new, on="userID", how="inner")
cols = ['userID', 'bookRating_x', 'bookRating_y']
df_new.drop(cols, axis=1, inplace=True)
"""
print(df_new.shape)
print(df_new.head(10))
"""


#插入数据库
conn = create_engine('mysql+pymysql://root:@localhost:3306/bookdb')
pd.io.sql.to_sql(book_new, "book", conn, if_exists='replace')
pd.io.sql.to_sql(df_new, "user_book", conn, if_exists='replace', index=False)
#pd.io.sql.to_sql(user_new, "user", conn, if_exists='replace', index=False) 改为由django迁移插入


