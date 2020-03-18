import pandas as pd
import numpy as np
from surprise import Reader, Dataset
import scipy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db import connection
from Movies.models import Movie
from Movies.models import Ratings
from Movies.models import users
from scipy.linalg import sqrtm
from scipy.sparse.linalg import svds
def run():
    collabfilterRecommendations(1)

def collabfilterRecommendations(userId):

    ratings_df = pd.DataFrame(list(Ratings.objects.all().values('userID', 'movieId', 'new_ratings')))

    movie_df = pd.DataFrame(list(Movie.objects.all().values('movieId', 'title')))

    #create dataframe with movieid as columns and userid as the row index with ratings as values
    Rating = ratings_df.pivot_table(index='userID', columns='movieId', values='new_ratings').fillna(0)
    # convert to a numpy array
    R = Rating.to_numpy()

    U, sigma, Vt = svds(R, k = 50)
    # convert to a diagonal matrix
    sigma = np.diag(sigma)

    # calc predicted value for each movie and each user.
    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt)

    preds = pd.DataFrame(all_user_predicted_ratings, columns = Rating.columns)



    sorted_user_predictions = preds.iloc[userId-1].sort_values(ascending=False).index

    already_recommended = list(users.objects.filter(newuserID_id=userId,recommended=1))
    prev_recomended_id=[]
    for r in already_recommended:
        prev_recomended_id.append(r.movieId_id)

    predicted_less_prev_rec = [x for x in sorted_user_predictions if x not in prev_recomended_id]
    recommended_movies=[]
    for p in predicted_less_prev_rec:
        if len(recommended_movies)<8:
            recommended_movies.append(Movie.objects.get(movieId=p))

    return recommended_movies
