from dbconnect import connection
import pandas as pd
import numpy as np


a, config = connection()

movie = 'SELECT * FROM movies'
movies_df = pd.read_sql(movie, config)
movies_df.head()
movies_df = pd.concat([movies_df, movies_df.genre.str.get_dummies(sep='|')], axis=1)
movies_df.head()

movies_df.drop(['img'], axis=1, inplace=True)
movies_df.drop(['title'], axis=1, inplace=True)
movies_df.drop(['movie_id'], axis=1, inplace=True)
movies_df.drop(['genre'], axis=1, inplace=True)
movies_df.drop(['year'], axis=1, inplace=True)
# for genre in genres:
    # print(genre)

def get_genre():

    genres = list(movies_df)
    del genres[0]

    return genres

def gen_movies(x):
    # a.execute('SELECT title from movies where genre LIKE %s',("%" +"action" +"%"))
    # mov = a.fetchall()
    gen = str(x)
    movies = 'SELECT * FROM movies'
    mov = pd.read_sql(movies, config)
    mov.head()

    rate = 'SELECT * FROM ratings'
    rt_df = pd.read_sql(rate, config)
    rt_df.head()

    lens = pd.merge(mov, rt_df)

    lens.drop(['year'], axis=1, inplace=True)
    lens.drop(['img'], axis=1, inplace=True)
    # lens = lens[lens['genre'].str.contains("Crime")]

    if gen == "Action":
        lens = lens[lens['genre'].str.contains("Action")]

    elif gen == "Adventure":
        lens = lens[lens['genre'].str.contains("Adventure")]

    elif gen == "Animation":
        lens = lens[lens['genre'].str.contains("Animation")]

    elif gen == "Children":
        lens = lens[lens['genre'].str.contains("Children")]

    elif gen == "Comedy":
        lens = lens[lens['genre'].str.contains("Comedy")]

    elif gen == "Crime":
        lens = lens[lens['genre'].str.contains("Crime")]

    elif gen == "Documentary":
        lens = lens[lens['genre'].str.contains("Documentary")]

    elif gen == "Drama":
        lens = lens[lens['genre'].str.contains("Drama")]

    elif gen == "Fantasy":
        lens = lens[lens['genre'].str.contains("Fantasy")]

    elif gen == "Film-Noir":
        lens = lens[lens['genre'].str.contains("Film-Noir")]

    elif gen == "Horror":
        lens = lens[lens['genre'].str.contains("Horror")]

    elif gen == "IMAX":
        lens = lens[lens['genre'].str.contains("IMAX")]

    elif gen == "Musical":
        lens = lens[lens['genre'].str.contains("Musical")]

    elif gen == "Mystery":
        lens = lens[lens['genre'].str.contains("Mystery")]

    elif gen == "Romance":
        lens = lens[lens['genre'].str.contains("Romance")]

    elif gen == "Sci-Fi":
        lens = lens[lens['genre'].str.contains("Sci-Fi")]

    elif gen == "Thriller":
        lens = lens[lens['genre'].str.contains("Thriller")]

    elif gen == "War":
        lens = lens[lens['genre'].str.contains("War")]

    elif gen == "Western":
        lens = lens[lens['genre'].str.contains("Western")]
    else:
        return "notworking"



    movie_stats = lens.groupby('title').agg({'ratings': [np.size, np.mean]})
    movie_stats.head()
    atleast_100 = movie_stats['ratings']['size'] >= 30
    movie_stats = movie_stats[atleast_100].sort_values([('ratings', 'mean')], ascending=False)[:20]
    movie_stats.head()

    # print(movie_stats)

    # movie_stats.drop(['size'], axis=1, inplace=True)
    topgenmov = []
    for index, row in movie_stats.iterrows():
        a.execute('SELECT img from movies WHERE title =%s', (str(index)))
        img = a.fetchone()
        a.execute('SELECT movie_id from movies WHERE title =%s', (str(index)))
        mid = a.fetchone()
        a.execute('SELECT imdbid from links WHERE movie_id =%s', (int(mid[0])))
        imdb = a.fetchone()

        # print(imdb[0])
        topgenmov.append((index,img[0],imdb[0]))


        # print(topgenmov)
        # list(mov.movie_id)
        # print(name)
    return topgenmov

# print(gen_movies("Action"))