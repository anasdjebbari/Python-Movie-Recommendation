from dbconnect import connection
import pandas as pd
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt



a, config = connection()

rating = 'SELECT * FROM ratings'
ratings = pd.read_sql(rating, config)
ratings.head()
ratings.drop(['timestamp'],axis=1, inplace=True)

M = ratings.pivot_table(index=['user_id'],columns=['movie_id'],values='ratings')
M.shape

rating2 = 'SELECT r.*, r1.size, r1.mean from ratings r INNER JOIN (SELECT movie_id, COUNT(1) size, AVG(ratings) mean FROM ratings GROUP BY movie_id HAVING COUNT(1) >= 20 ORDER BY 3 DESC) AS r1 ON r.movie_id = r1.movie_id'
ratings2 = pd.read_sql(rating2, config)
ratings2.head()
ratings2.drop(['timestamp'],axis=1, inplace=True)
ratings2.drop(['size'],axis=1, inplace=True)
ratings2.drop(['mean'],axis=1, inplace=True)


M1 = ratings2.pivot_table(index=['user_id'],columns=['movie_id'],values='ratings')
M1.shape

# print(M1)
# mov = homerec()


def pearson(m1, m2):
    m1_c = m1 - m1.mean()
    m2_c = m2 - m2.mean()
    cor = np.sum(m1_c*m2_c)/np.sqrt(np.sum(m1_c ** 2) * np.sum(m2_c **2))
    return cor

def get_rec(mid, M, M1,like):
    reviews = []
    for title in M1.columns:
        if title == mid:
            continue
        cor = pearson(M[mid],M1[title])

        if np.isnan(cor):
            continue
        else:
            a.execute('SELECT title from movies WHERE movie_id =%s', (int(title)))
            name = a.fetchone()
            a.execute('SELECT img from movies WHERE movie_id =%s', (int(title)))
            img = a.fetchone()
            a.execute('SELECT imdbid from links WHERE movie_id =%s', (int(title)))
            imdb = a.fetchone()

            reviews.append((title,cor,name[0],img[0],imdb[0]))

    if like == 1:
        reviews.sort(key=lambda tup: tup[1], reverse=True)
        return (reviews[:10])

    if like == 2:
        reviews.sort(key=lambda tup: tup[1], reverse=False)
        return (reviews[10:])




def recmov(mov,set,rate):
    p = mp.Process(target=get_rec, args=(mov, set, rate))
    p.start()
    p.join()

# #
# get = get_rec(1,M,M1,2)
# #
# print(get)
# # get = recmov(1,M,1)
# print(get)