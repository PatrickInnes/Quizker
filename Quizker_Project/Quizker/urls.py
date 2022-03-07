from django.urls import path
from django.conf.urls import url
from Quizker import views

app_name = 'Quizker'

urlpatterns = [
    path('', views.index, name='index'),
]