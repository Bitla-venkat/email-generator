from django.urls import path
from .views import generate_text, home

urlpatterns = [
    path('', home, name='home'),
    path('generate_text/', generate_text, name='generate_text'),
]