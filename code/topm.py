import requests
from dbconnect import connection

a, config = connection()

def plot(x):
        info = []
        if len(str((x))) == 7:
            url = 'https://www.omdbapi.com/?i=tt' + str(x) + '&plot=full&r=json'

        elif len(str((x))) == 6:
            url = 'https://www.omdbapi.com/?i=tt0' + str(x) + '&plot=full&r=json'


        elif len(str((x))) == 5:
            url = 'https://www.omdbapi.com/?i=tt00' + str(x) + '&plot=full&r=json'

        elif len(str((x))) == 4:
            url = 'https://www.omdbapi.com/?i=tt000' + str(x) + '&plot=full&r=json'


        elif len(str((x))) == 3:
            url = 'https://www.omdbapi.com/?i=tt000' + str(x) + '&plot=full&r=json'

        response = requests.get(url)
        if response.json()['Response'] == "True":
            results = response.json()['Plot']
            return results

        else:
            return "nothing is wokring"

        return info


def movie_info(x):
        info = []
        if len(str((x))) == 7:
            url = 'https://www.omdbapi.com/?i=tt'+str(x)+'&plot=full&r=json'

        elif len(str((x))) == 6:
            url = 'https://www.omdbapi.com/?i=tt0' + str(x) + '&plot=full&r=json'


        elif len(str((x))) == 5:
            url = 'https://www.omdbapi.com/?i=tt00' + str(x) + '&plot=full&r=json'

        elif len(str((x))) == 4:
            url = 'https://www.omdbapi.com/?i=tt000' + str(x) + '&plot=full&r=json'


        elif len(str((x))) == 3:
            url = 'https://www.omdbapi.com/?i=tt000' + str(x) + '&plot=full&r=json'

        response = requests.get(url)
        if response.json()['Response'] == "True":
            results = response.json()['Plot']
            genre = response.json()['Genre']
            poster = response.json()['Poster']
            runtime = response.json()['Runtime']
            title = response.json()['Title']


            info.append((results, genre, runtime, poster,title))

        else:
            return "nothing is wokring"

        return info


# print(movie_info(1375666))