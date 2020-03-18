from django import forms
from Movies.models import *

AGE= [
    ('0-18', '0-18'),
    ('18-25', '18-25'),
    ('25-30', '25-30'),
    ('30-40', '30-40'),
    ('40-50', '40-50'),
    ('50+', '50+')
    ]
WATCHES=[
    ('0-2','0-2'),
    ('3-6','3-6'),
    ('7-10','7-10'),
    ('10+','10+')
    ]
class user(forms.ModelForm):
    age =forms.CharField(label='What age are you :',
    widget=forms.RadioSelect(choices=AGE))
    movie_watching_freq = forms.CharField(label='How many times a week do you watch movies? :',
    widget=forms.RadioSelect(choices=WATCHES))
    class Meta:
        model=new_user_info
        fields =["age","movie_watching_freq"]
