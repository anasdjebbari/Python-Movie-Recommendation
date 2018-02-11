from dbconnect import connection

a, config = connection()

def srch_mov(title):

    a.execute('SELECT DISTINCT links.imdbId, movies.title, movies.img from movies, links WHERE links.movie_id = movies.movie_id AND movies.title LIKE %s', ("%"+str(title)+"%"))
    name = a.fetchall()
    return name
#
# b = srch_mov("Bat")
#
# for item in b:
#     print(item[0])