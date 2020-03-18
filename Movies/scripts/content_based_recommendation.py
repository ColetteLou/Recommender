import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db import connection
from Movies.models import Movie
from Movies.models import Ratings
from Movies.models import users
import pickle

def run():
    content_recommendations(1)

def content_recommendations(userid):

    sim_matrix = np.load('Movies/static/Movies/sim_matrix.npy',allow_pickle = True)
    indices = pd.read_csv (r'Movies/static/Movies/index.csv')
    recommended_movies_id = []
    recommended_movies=[]
    movies_rated_high = list(Ratings.objects.filter(userID=userid,new_ratings=3))
    movies_rated_med = list(Ratings.objects.filter(userID=userid,new_ratings=2))

    liked_movies = []
    liked_movies_ids = []


    while movies_rated_high:
        for m in movies_rated_high[:]:
            liked_movies.append(m)
            movies_rated_high.remove(m)

    if len(liked_movies)<8:
        while movies_rated_med:
            for m in movies_rated_med[:]:
                    liked_movies.append(m)
                    movies_rated_med.remove(m)

    #if user hasn't given any feed back show 12 random movies and message advising user
    if len(liked_movies)==0 : return None

    for n in liked_movies:
        liked_movies_ids.append(n.movieId_id)

    top=[]
    indexes=[]
    already_recommended = list(users.objects.filter(newuserID_id=userid,recommended=1))

    for r in already_recommended:
        id=r.movieId_id
        indx_rec=(indices.loc[indices['movieId'] == id].index[0])
        indexes.append(indx_rec)

    for ids in liked_movies_ids:
        indx_liked = indices.loc[indices['movieId'] == ids].index[0]
        score = pd.Series(sim_matrix[indx_liked]).sort_values(ascending = False)
        score=score.drop(labels=indexes)

        if len(liked_movies_ids)==1:
            top.append(list(score.iloc[1:9].index))
        elif len(liked_movies_ids)==2:
            top.append(list(score.iloc[1:5].index))
        elif len(liked_movies_ids)==3:
            top.append(list(score.iloc[1:5].index))
        elif len(liked_movies_ids)>=4 and len(liked_movies_ids)<=7 :
            top.append(list(score.iloc[1:3].index))
        elif len(liked_movies_ids)>=8:
            top.append(list(score.iloc[1:2].index))

    for t in top:
        recommended_movies_id.append(list(indices.movieId)[t[0]])

    recommended_movies_id = list(dict.fromkeys(recommended_movies_id))

    for movies in recommended_movies_id:
        if len(recommended_movies)<8:
            recommended_movies.append(Movie.objects.get(movieId=movies))

    #send back full list of possiblilites, choose randomly for over 12 entries in view
    return recommended_movies
