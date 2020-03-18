from django.db import connection
from Movies.models import Movie
from Movies.models import Ratings
from Movies.models import users
from Movies.models import MovieGenres
import pandas as pd
import numpy as np
import random

def run():
    genre_based(611)

def genre_based(userId):

    users_liked = list(users.objects.filter(newuserID_id=userId,rating=3))

    liked_ids = []
    liked_movies = []
    for u in users_liked:
        liked_ids.append(u.movieId_id)
        liked_movies.append(Movie.objects.get(movieId=u.movieId_id))

    genre_df= pd.DataFrame(MovieGenres.objects.filter(movieId_id__in=liked_ids).values('Action','Adventure','Animation'
    ,'Children','Comedy','Crime','Documentary','Drama','Fantasy','Film_Noir',
    'Horror','Musical','Mystery','Romance','Sci_Fi','Thriller','War','Western'))
    sums = genre_df[genre_df==True].count(axis=0)

    movies_with_top_genre = list(Movie.objects.filter(genre__contains=sums.idxmax()))
    movies_with_top_genre_less_watched = [x for x in movies_with_top_genre if x not in liked_movies]

    recommended_movies= random.sample(movies_with_top_genre_less_watched,8)

    return(recommended_movies)
