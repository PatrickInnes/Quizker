from django.contrib import admin
from django.urls import path, include
from Quizker import views

urlpatterns = [
    path('', include('Quizker.urls')),
    path('accounts/', include('registration.backends.simple.urls')),
    path('admin/', admin.site.urls),
]
