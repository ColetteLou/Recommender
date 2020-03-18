from Movies.models import Movie
from Movies.models import Ratings
from Movies.models import users
from Movies.models import MovieGenres
import pandas as pd
import numpy as np

def get_genre_data(userId):
    usermovies= (list(users.objects.filter(newuserID_id=userId, rating=3)))
    movieids = []

    for u in usermovies:
        movieids.append(u.movieId_id)

    genre_df= pd.DataFrame(MovieGenres.objects.filter(movieId_id__in=movieids).values('Action','Adventure','Animation'
    ,'Children','Comedy','Crime','Documentary','Drama','Fantasy','Film_Noir',
    'Horror','Musical','Mystery','Romance','Sci_Fi','Thriller','War','Western'))
    sums = genre_df[genre_df==True].count(axis=0)
    count_of_genres= sums.to_numpy()
    genre_names = ['Action','Adventure','Animation'
    ,'Children','Comedy','Crime','Documentary','Drama','Fantasy','Film_Noir',
    'Horror','Musical','Mystery','Romance','Sci_Fi','Thriller','War','Western']


    return(genre_names,sums)
