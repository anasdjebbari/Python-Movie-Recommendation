from dbconnect import connection
import pandas as pd
import numpy as np
from topm import plot

a, config = connection()

rating = 'SELECT * FROM ratings'
ratings = pd.read_sql(rating, config)
ratings.head()

del ratings['timestamp']


movie = 'SELECT * FROM movies'
movies = pd.read_sql(movie, config)
movies.head()

user = 'SELECT * FROM users'
users = pd.read_sql(user, config)
users.head()

ratings_df = pd.merge(ratings, movies, on='movie_id')[['user_id', 'title', 'movie_id','ratings']]

ratings_mrtx_df = ratings_df.pivot_table(values='ratings', index='user_id', columns='title')
ratings_mrtx_df.fillna(0, inplace=True)

movie_index = ratings_mrtx_df.columns


ratings_mrtx_df.head()

corr_matrix = np.corrcoef(ratings_mrtx_df.T)
corr_matrix.shape


def get_similar_movies(movie_title):
    '''Returns correlation vector for a movie'''
    movie_idx = list(movie_index).index(movie_title)
    return corr_matrix[movie_idx]

def get_movie_recommendations(user_movies):
    '''given a set of movies, it returns all the movies sorted by their correlation with the user'''
    movie_similarities = np.zeros(corr_matrix.shape[0])
    for movie_id in user_movies:
        movie_similarities = movie_similarities + get_similar_movies(movie_id)


        similar_movies_df = pd.DataFrame({
            'title': movie_index,
            'sum_similarity': movie_similarities
        })
        # similar_movies_df = similar_movies_df.drop.loc[similar_movies_df['title'].str.contains('Gladiator')]
        # similar_movies_df.drop(similar_movies_df['title'].str.contains('Star Wars: Episode IV - A New Hope'), inplace=True)

    # for index, row in similar_movies_df.iterrows():
    #     if index == 4963:
    #         # print(index)
    #         similar_movies_df.drop(index, inplace=True)

    # similar_movies_df = similar_movies_df.loc[similar_movies_df['title'].str.contains('Gladiator')
    similar_movies_df = similar_movies_df.sort_values(by=['sum_similarity'], ascending=False)
    # print(similar_movies_df)
    return similar_movies_df

#
# smpl_user = 685
# ss = ratings_df[ratings_df.user_id==smpl_user].sort_values(by=['ratings'], ascending=False)
# print(ss)
#
# smpl_user_movies = ratings_df[ratings_df.user_id == smpl_user].title.tolist()
# recommendations = get_movie_recommendations(smpl_user_movies)
# l= len(smpl_user_movies)
# #We get the top 20 recommended movies
# innerl = l+20
# s = recommendations.title.head(20)
#
# print(s)

# # #

def get_user_rec(smpl_user):
    ratings_df[ratings_df.user_id==smpl_user].sort_values(by=['ratings'], ascending=False)

    smpl_user_movies = ratings_df[ratings_df.user_id==smpl_user].title.tolist()
    recommendations = get_movie_recommendations(smpl_user_movies)
    l= 20

    #We get the top 20 recommended movies
    innerl = l+24
    rec = recommendations.title.head(innerl)[l:]
#
    reviews = []

    for item in rec:
        a.execute('SELECT img from movies WHERE title =%s', (str(item)))
        img = a.fetchone()
        a.execute('SELECT movie_id from movies WHERE title =%s', (str(item)))
        mid = a.fetchone()
        a.execute('SELECT imdbid from links WHERE movie_id =%s', (int(mid[0])))
        imdb = a.fetchone()

        x = plot(int(imdb[0]))

        reviews.append((int(imdb[0]), item, img[0], str(x)))


    return reviews

# # print(get_user_rec(9))
#
#
#



