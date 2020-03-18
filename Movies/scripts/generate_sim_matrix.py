import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from django.db import connection
from Movies.models import Movie
import pickle

def run():
    df = pd.DataFrame(list(Movie.objects.all().values()))
    # extract data for comparison and movie id for identification
    df = df[['movieId','genre','yearReleased','director_s','country','actors']]

    # clean up data, top 2 directors, split genres, top 3 countries,top 4 actors
    df['genre'] = df['genre'].map(lambda x: x.lower().split('|'))
    df['director_s'] = df['director_s'].map(lambda x: x.split(',')[:2])
    df['country'] = df['country'].map(lambda x: x.split(',')[:3])
    df['actors'] = df['actors'].map(lambda x: x.split(',')[:4])

    #remove spaces between actors and director names so for e.g danny devito
    # and danny trejo don't show similarity due to danny being present
    for index, row in df.iterrows():
        row['actors'] = [x.lower().replace(' ','') for x in row['actors']]
        row['director_s'] = [x.lower().replace(' ','') for x in row['director_s']]

    #add more weight to director and genre
    df['director2'] = df['director_s']
    df['genre2'] = df['genre']

    #use movieid as index
    df.set_index('movieId', inplace = True)

    #combines all the features into a series of words
    df['combined_features'] = ''
    columns = df.columns
    for index, row in df.iterrows():
        words = ''

        for col in columns:
            if col == 'yearReleased':
                words = words + row[col]+ ' '
            else:
                words = words + ' '.join(row[col])+ ' '

        row['combined_features'] = words

    #drop all colunms except index(movieId) and combined features column
    df.drop(columns = [col for col in df.columns if col!= 'combined_features'], inplace = True)

    count = CountVectorizer()
    count_matrix = count.fit_transform(df['combined_features'])

    indices = pd.Series(df.index)
    indices.to_csv(r'Movies/static/Movies/index.csv', index = False)
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    cos =cosine_sim.round(4)
    #np.save('Movies/static/Movies/sim_matrix.npy',cos,allow_pickle=True)
    print(cos)
