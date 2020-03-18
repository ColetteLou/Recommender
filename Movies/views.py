from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.db.models import Max
from django import template
from django.template.loader import get_template
from Movies.models import *
import random
import time
from Movies.scripts.content_based_recommendation import *
from Movies.scripts.genre_based import *
from Movies.scripts.collabrative_filtering import *
from Movies.scripts.graph import *
from .forms import user

def index(request):
    if request.method=='POST':
        d=new_user_info.objects.aggregate(Max('newuserID'))
        i=d.get("newuserID__max")
        request.session['username']=i+1
        request.session['alg1_count']=0
        request.session['alg2_count']=0
        request.session['alg3_count']=0
        request.session['starterRated']=0
        ra= Ratings(userID=i+1,movieId_id=1,new_ratings=None)
        ra.save()
        form= user(request.POST)
        if form.is_valid():
            f=form.save(False)
            f.newuserID = request.session['username']
            f.save()
            return HttpResponseRedirect('starter_movies/')
    else :
        form =user()
        context= { 'form': form }
        template= get_template('Movies/start_page.html')
    return HttpResponse(template.render(context,request))

def starter_movies(request):

    all_movies = (list(Movie.objects.all().values()))
    movies = random.sample(all_movies,12)
    template= get_template('Movies/starter_movies.html')
    context = {
        'movies': movies,
    }
    return HttpResponse(template.render(context,request))

def recommendations_content(request):
    userid=request.session['username']
    request.session['alg1_count']+=1
    movies = content_recommendations(userid)
    template= get_template('Movies/recommended_content.html')
    while movies is None:
        time.sleep(1)
    if len(movies)>8:
        movies= random.sample(movies,8)

    context = {
        'movies': movies,
    }
    return HttpResponse(template.render(context,request))

def recommendations_collab(request):
    userid=request.session['username']
    request.session['alg2_count']+=1
    movies = collabfilterRecommendations(userid)
    template= get_template('Movies/recommended_collab.html')
    while movies is None:
        time.sleep(1)
    if len(movies)>8:
            movies= random.sample(movies,8)

    context = {
        'movies': movies,
    }
    return HttpResponse(template.render(context,request))

def recommendations_genre(request):
    userid=request.session['username']
    request.session['alg3_count']+=1
    movies = genre_based(userid)
    template= get_template('Movies/recommended_genre.html')
    while movies is None:
        time.sleep(1)
    if len(movies)>8:
        movies= random.sample(movies,8)

    context = {
        'movies': movies,
    }
    return HttpResponse(template.render(context,request))

def get_data(request):
    userid=request.session['username']
    names,counts = get_genre_data(userid)
    while names is None:
        time.sleep(1)
    while counts is None :
        time.sleep(1)
    data= {
            "labels" : list(names),
            "count" : list(counts)
    }

    return JsonResponse(data)

def end_page(request):

    return render(request,'Movies/graph_page.html',{})


def algorithm_info(request):
    return HttpResponse('alg info')

def submit_starter(request):
    if request.method == 'POST':
        id=request.POST.get('userID')
        for i in range(1,13):
            rating= request.POST.get(str(i))
            if rating is not None:
                mId, r = rating[:-1], rating[-1]
                if(int(r)==4):
                    rec=users(newuserID_id=int(id),recommended=1,user_preference=1,movieId_id=int(mId))
                    rec.save()
                else:
                    ra= Ratings(userID=int(id),movieId_id=int(mId),new_ratings=int(r))
                    ra.save()
                    rec=users(newuserID_id=int(id),recommended=1,user_preference=1,rating=int(r),movieId_id=int(mId))
                    rec.save()
                    request.session['starterRated']+=1
    if request.session['starterRated']==0 : return HttpResponseRedirect('/Movies/starter_movies/')

    return HttpResponseRedirect('/Movies/rec_movies_content/')

def submit_recommended_content(request):
        if request.method == 'POST':
            id=request.POST.get('userID')
            for i in range(1,13):
                rating= request.POST.get(str(i))
                watched = request.POST.get(str(i)+"1")
                if rating is not None and watched is not None:
                    watched = watched[-1]
                    if watched == 'w':
                        seen=True
                    elif watched=='n':
                        seen=False
                    else:
                        seen=None
                    mId, r = rating[:-1], rating[-1]
                    ra= Ratings(userID=int(id),movieId_id=int(mId),new_ratings=int(r))
                    ra.save()
                    rec=users(newuserID_id=int(id),recommended=1,user_preference=0,rating=int(r),watched=seen,movieId_id=int(mId),alg=1,alg_count=request.session['alg1_count'])
                    rec.save()
        return HttpResponseRedirect('/Movies/rec_movies_collab/')

def submit_recommended_collab(request):
        if request.method == 'POST':
            id=request.POST.get('userID')
            for i in range(1,13):
                rating= request.POST.get(str(i))
                watched = request.POST.get(str(i)+"1")
                if rating is not None and watched is not None:
                    watched = watched[-1]
                    if watched == 'w':
                        seen=True
                    elif watched=='n':
                        seen=False
                    else:
                        seen=None
                    mId, r = rating[:-1], rating[-1]
                    ra= Ratings(userID=int(id),movieId_id=int(mId),new_ratings=int(r))
                    ra.save()
                    rec=users(newuserID_id=int(id),recommended=1,user_preference=0,rating=int(r),watched=seen,movieId_id=int(mId),alg=2,alg_count=request.session['alg2_count'])
                    rec.save()
        return HttpResponseRedirect('/Movies/rec_movies_genre/')

def submit_recommended_genre(request):
        if request.method == 'POST':
            id=request.POST.get('userID')
            for i in range(1,13):
                rating= request.POST.get(str(i))
                watched = request.POST.get(str(i)+"1")
                if rating is not None and watched is not None:
                    watched = watched[-1]
                    if watched == 'w':
                        seen=True
                    elif watched=='n':
                        seen=False
                    else:
                        seen=None
                    mId, r = rating[:-1], rating[-1]
                    ra= Ratings(userID=int(id),movieId_id=int(mId),new_ratings=int(r))
                    ra.save()
                    rec=users(newuserID_id=int(id),recommended=1,user_preference=0,rating=int(r),watched=seen,movieId_id=int(mId),alg=3,alg_count=request.session['alg3_count'])
                    rec.save()
        if request.session['alg3_count']>=2:
            return HttpResponseRedirect('/Movies/end_page/')
        else:
            return HttpResponseRedirect('/Movies/rec_movies_content/')


def rate_more(request):
    if request.method == 'POST':
        id=request.POST.get('userID')
        for i in range(1,13):
            rating= request.POST.get(str(i))
            if rating is not None:
                mId, r = rating[:-1], rating[-1]
                if(int(r)==4):
                    rec=users(newuserID_id=int(id),recommended=1,user_preference=1,movieId_id=int(mId))
                    rec.save()
                else:
                    ra= Ratings(userID=int(id),movieId_id=int(mId),new_ratings=int(r))
                    ra.save()
                    rec=users(newuserID_id=int(id),recommended=1,user_preference=1,rating=int(r),movieId_id=int(mId))
                    rec.save()
                    request.session['starterRated']+=1
    return HttpResponseRedirect('/Movies/starter_movies/')
