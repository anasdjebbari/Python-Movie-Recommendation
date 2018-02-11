from flask import Flask, session,Response, render_template, request, redirect, url_for, g
import os
import requests
import time
import json

from topm import movie_info
from user_Rec import get_user_rec
from dbconnect import connection
from scrap import get_rec, M,M1
from search import srch_mov
from youtube import get_genre,gen_movies

a, config = connection()

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        a.execute('SELECT user_id FROM users WHERE name = %s', (request.form['username']))
        userid = a.fetchone()
        userid = int(userid[0])
        a.execute('SELECT password FROM users WHERE user_id = %s', (userid))
        password = a.fetchone()
        passw = str(password[0])

        if request.form['password'] == passw:
            session['user'] = userid
            session['password'] = request.form['password']

            return redirect(url_for('protected'))

    return render_template("index.html")

@app.route('/genre')
def genre():
    if g.user:
        gen = get_genre()
        return render_template('genre.html', genres = gen)

@app.route('/genremovies/<mgenre>')
def genremovies(mgenre):
    if g.user:
        x = str(mgenre)
        gen = gen_movies(x)
        print(gen)
        return render_template('genmov.html', movgen = gen)


@app.route('/search', methods=['GET', 'POST'])
def search():
    result = []
    if request.method == 'POST':
        search = request.form['title']
        result = (srch_mov(search))
    return render_template("search.html", res=result)


@app.route('/srch', methods=['GET', 'POST'])
def srch():
    select = request.form.get('search')
    return redirect(url_for('.movie', movie_id=str(select)))

@app.route('/logout')
def logout():
    dropsession()
    return redirect(url_for('index'))

@app.route('/protected')
def protected():
    search = list()
    sqlsearch = 'SELECT DISTINCT movies.title, links.imdbId from movies, links WHERE links.movie_id = movies.movie_id LIMIT 9300'
    a.execute(sqlsearch)
    srchdata = a.fetchall()
    search.append(srchdata)
    if g.user:

        imdbid = get_user_rec(int(g.user))
        noob_msg = "Your Recommendation:"



        return render_template('regout.html', nmsg = noob_msg,search=search, name=g.user, imdbid=imdbid)

    return redirect(url_for('index'), )

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        session['name'] = request.form['username']
        session['gender'] = request.form['gender']
        session['age'] = request.form['age']
        session['occupation'] = request.form['occupation']
        session['password'] = request.form['password']
        return redirect(url_for('register'))

    return render_template("register.html")

@app.route('/register')
def register():
    a.execute('select MAX(user_id) from users')
    maxid = a.fetchone()
    a.execute('insert into users VALUES (%s,%s,%s,%s,%s,%s)', (
    maxid[0] + 1, session['name'], session['gender'], session['age'], session['occupation'], session['password']))
    config.commit()
    # maxid = maxid[0] +1
    # movie = 1
    # rate = 5
    # tstamp = 1260759151
    # a.execute('insert into ratings VALUES (%s,%s,%s,%s)', (maxid, movie, rate,tstamp ))
    # config.commit()
    return redirect(url_for('index'), )

@app.route('/profile')
def profile():
    if g.user:
        uid = g.user

        search = list()
        sqlsearch = 'SELECT DISTINCT movies.title, links.imdbId from movies, links WHERE links.movie_id = movies.movie_id LIMIT 9300'
        a.execute(sqlsearch)
        srchdata = a.fetchall()
        search.append(srchdata)

        profileArray = list()
        a.execute('SELECT movies.title,links.imdbId from movies, ratings, links WHERE user_id = %s AND movies.movie_id = ratings.movie_id AND ratings.movie_id=links.movie_id',(uid))
        data = a.fetchall()
        profileArray.append(data)

    return render_template("profile.html",search=search, name=g.user, watched=profileArray)

@app.route('/movie/<movie_id>')
def movie(movie_id):
    movie_id = movie_id.replace("(", "").replace(",", "").replace(")", "")

    if g.user:
        a.execute('SELECT movie_id from links WHERE imdbId =%s', (movie_id))
        m_id = a.fetchone()

        id = m_id[0]

        sql2 = 'select ratings,FROM_UNIXTIME(ratings.timestamp) from ratings where user_id = %s AND movie_id = %s'
        a.execute(sql2, (g.user, id))
        sqlrating = a.fetchone()

        notification = list()
        sql3 = 'SELECT users.name, movies.title, ratings.ratings, FROM_UNIXTIME(ratings.timestamp), users.sex, users.age from ratings,movies, users WHERE ratings.movie_id=%s and movies.movie_id = ratings.movie_id and ratings.user_id = users.user_id LIMIT 10'
        a.execute(sql3, (id))
        notidata = a.fetchall()
        notification.append(notidata)



        a.execute('SELECT Round(AVG(ratings)) from ratings where movie_id=%s', (m_id[0]))
        avgrating = a.fetchone()

        a.execute('SELECT * from ratings where user_id = %s and movie_id = %s', (g.user, m_id[0]))
        rated = a.fetchone()

        message = " "
        mesage_time = " "
        recmesg = " "
        if rated == None:
            rec =[]

        else:
            message = "You rated this movie: "
            mesage_time = "At: "
            rec = get_rec(id, M, M1, 1)
            recmesg = ""

        info = movie_info(movie_id)



        return render_template("movie.html",
                               avg = avgrating[0],
                               m = message,
                               t = mesage_time,
                               # link="static/"+link,
                               rec = rec,
                               recmesg=recmesg,
                               minfo = info,
                               sqlrating=sqlrating,
                               movie=movie_id,
                               name=g.user,
                               notification=notification
        )

    return redirect(url_for('index'))

@app.route('/rate/<rating>/<movie_id>')
def rate(rating, movie_id):
    if g.user:
        rate = rating
        timestp = int(time.time())
        movie_id = movie_id.replace("(", "").replace(",", "").replace(")", "")
        a.execute('SELECT movie_id from links WHERE imdbId =%s', (movie_id))
        m_id = a.fetchone()

        a.execute('SELECT * from ratings where user_id = %s and movie_id = %s', (g.user, m_id[0]))
        works = a.fetchone()

        if works == None:
            a.execute('insert into ratings VALUES (%s,%s,%s,%s)', (g.user, m_id[0], rate, timestp))
            config.commit()
        else:
            a.execute('update ratings set ratings = %s,timestamp = %s where user_id = %s and movie_id = %s',
                      (rate, timestp, g.user, m_id[0]))
            config.commit()

        return redirect(url_for('.movie', movie_id=movie_id))

    return redirect(url_for("index"))

@app.route('/discover')
def discover():
    if g.user:
        return ""

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']

    return 'not logged in yet'

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run()
