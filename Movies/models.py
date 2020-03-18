from django.db import models
from graphos.sources.model import ModelDataSource

class Movie(models.Model):
    movieId = models.BigIntegerField(primary_key=True)
    imdbId = models.CharField(max_length=10,default=None, blank=True, null=True)
    title = models.CharField(max_length=200,default=None, blank=True, null=True)
    yearReleased = models.CharField(max_length=15,default=None, blank=True, null=True)
    genre = models.CharField(max_length=400,default=None, blank=True, null=True)
    poster = models.CharField(max_length=500,default=None, blank=True, null=True)
    director_s = models.CharField(max_length=201,default=None, blank=True, null=True)
    country = models.CharField(max_length=500,default=None, blank=True, null=True)
    actors = models.CharField(max_length=300,default=None, blank=True, null=True)

class MovieGenres(models.Model):
    id = models.AutoField(primary_key=True)
    movieId = models.ForeignKey('Movie', to_field='movieId',on_delete=models.CASCADE)
    Action = models.BooleanField(default=None, blank=True, null=True)
    Adventure =models.BooleanField(default=None,blank=True, null=True)
    Animation= models.BooleanField(default=None, blank=True, null=True)
    Children = models.BooleanField(default=None, blank=True, null=True)
    Comedy= models.BooleanField(default=None, blank=True, null=True)
    Crime= models.BooleanField(default=None, blank=True, null=True)
    Documentary= models.BooleanField(default=None, blank=True, null=True)
    Drama= models.BooleanField(default=None, blank=True, null=True)
    Fantasy= models.BooleanField(default=None, blank=True, null=True)
    Film_Noir= models.BooleanField(default=None, blank=True, null=True)
    Horror= models.BooleanField(default=None, blank=True, null=True)
    Musical= models.BooleanField(default=None, blank=True, null=True)
    Mystery= models.BooleanField(default=None, blank=True, null=True)
    Romance= models.BooleanField(default=None, blank=True, null=True)
    Sci_Fi= models.BooleanField(default=None, blank=True, null=True)
    Thriller= models.BooleanField(default=None, blank=True, null=True)
    War= models.BooleanField(default=None, blank=True, null=True)
    Western= models.BooleanField(default=None, blank=True, null=True)
    no_genres_listed= models.BooleanField(default=None, blank=True, null=True)


class Ratings(models.Model):
    id = models.AutoField(primary_key=True)
    userID = models.BigIntegerField()
    movieId = models.ForeignKey('Movie', to_field='movieId',on_delete=models.CASCADE)
    ratings = models.FloatField(default=None, blank=True, null=True)
    new_ratings = models.SmallIntegerField(default=None, blank=True, null=True)
    timestamp = models.BigIntegerField(default=None, blank=True, null=True)


class users(models.Model):
    id = models.AutoField(primary_key=True)
    newuserID = models.ForeignKey('new_user_info',on_delete=models.CASCADE)
    movieId = models.ForeignKey('Movie', to_field='movieId',on_delete=models.CASCADE)
    # rating given for recommendation
    recommended = models.BooleanField(default=None, blank=True, null=True)
    #user rated as a preference
    user_preference = models.BooleanField(default=None, blank=True, null=True)
    # yes, no, maybe
    rating= models.CharField(max_length=5,default=None, blank=True, null=True)
    watched = models.BooleanField(default=None, blank=True, null=True)
    #1,2,3
    alg = models.SmallIntegerField(default=None, blank=True, null=True)
    #first round second etc
    alg_count = models.SmallIntegerField(default=None, blank=True, null=True)


class new_user_info(models.Model):
        newuserID = models.BigIntegerField(primary_key=True)
        age = models.CharField(max_length=10)
        # 1 = a few 1-2  a week 2 = moderate 3-6 amount 3 = alot 6+ per week
        movie_watching_freq = models.CharField(max_length=5)
