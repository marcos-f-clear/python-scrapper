from django.urls import path
from .views import scrape_json

urlpatterns = [
    path('scrape_json/', scrape_json, name='scrape_json'),
]