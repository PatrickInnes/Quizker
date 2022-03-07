from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

def index(request):
    return render(request, 'quizker/index.html')
