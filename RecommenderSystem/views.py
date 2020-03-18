from django.http import HttpResponse
from Movies.models import Movie

def hello(request):
    movies = Movie.objects.all()
    for m in movies:
     response = m.poster
    return HttpResponse(response)
