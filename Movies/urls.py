from django.urls import path
from django.urls import re_path
from . import views

app_name ='Movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('starter_movies/', views.starter_movies),
    path('rec_movies_content/', views.recommendations_content),
    path('rec_movies_collab/', views.recommendations_collab),
    path('rec_movies_genre/', views.recommendations_genre),
    path('submit_starter/', views.submit_starter),
    path('submit_recommended_content/',views.submit_recommended_content),
    path('submit_recommended_collab/',views.submit_recommended_collab),
    path('submit_recommended_genre/',views.submit_recommended_genre),
    path('get_data/',views.get_data),
    path('end_page/',views.end_page),
    path('rate_more/',views.rate_more)
]
