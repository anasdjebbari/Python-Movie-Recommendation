import pymysql

def connection():
    config = pymysql.connect (
            user = 'root',
           password = 'root',
           host = 'localhost',
           database =  'movie_rec',
            )
    a = config.cursor()
    return a, config


