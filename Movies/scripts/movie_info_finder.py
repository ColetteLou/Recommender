# scripts/movie_info_finder.py

from django.db import connection
from Movies.models import Movie
from Movies.models import MovieGenres

import omdb

omdb.set_default('apikey', 'd322bb8e')
omdb.set_default('timeout', 5)


all_entries = Movie.objects.all()
all_entries_genre =MovieGenres.objects.all()
def run():
    for m in all_entries:
        Imdbid = m.imdbId
        id = m.movieId
        try:
            movie_info= omdb.imdbid(Imdbid)
            poster_link = movie_info.get("poster", "none")
            m.poster = poster_link
            str_dir = movie_info.get("director","none")
            if len(str_dir)>200 : str_dir = str_dir[0:200]
            m.director_s = str_dir
            m.actors = movie_info.get("actors","none")
            m.country = movie_info.get("country","none")
            m.yearReleased = movie_info.get("year","none")

        except:
            pass



        m.save()



for m in all_entries:
    for g in all_entries_genre:
        if(m.movieId==g.movieId_id):
            if "Action" in m.genre: g.Action=1
            else:g.Action=0
            if "Adventure" in m.genre: g.Adventure=1
            else:g.Adventure=0
            if "Animation" in m.genre: g.Animation=1
            else:g.Animation=0
            if "Children" in m.genre: g.Children=1
            else:g.Children=0
            if "Comedy" in m.genre: g.Comedy=1
            else:g.Comedy=0
            if "Crime" in m.genre: g.Crime=1
            else:g.Crime=0
            if "Documentary" in m.genre: g.Documentary=1
            else:g.Documentary=0
            if "Drama" in m.genre: g.Drama=1
            else:g.Drama=0
            if "Fantasy" in m.genre: g.Fantasy=1
            else:g.Fantasy=0
            if "Film-Noir" in m.genre: g.Film_Noir=1
            else:g.Film_Noir=0
            if "Horror" in m.genre: g.Horror=1
            else:g.Horror=0
            if "Musical" in m.genre: g.Musical=1
            else:g.Musical=0
            if "Mystery" in m.genre: g.Mystery=1
            else:g.Mystery=0
            if "Romance" in m.genre: g.Romance=1
            else:g.Romance=0
            if "Sci-Fi" in m.genre: g.Sci_Fi=1
            else:g.Sci_Fi=0
            if "Thriller" in m.genre: g.Thriller=1
            else:g.Thriller=0
            if "War" in m.genre: g.War=1
            else:g.War=0
            if "Westerm" in m.genre: g.Western=1
            else:g.Western=0
            if "no genres listed" in m.genre: g.no_genres_listed=1
            else:g.no_genres_listed=0
            g.save()
