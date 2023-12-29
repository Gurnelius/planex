from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('<str:id>', views.download, name='download_video'),
    path('downloads/', views.download, name='download'),
    path('scrape', views.home_scraper, name='scrape'),
]
