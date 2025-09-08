from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('run/', views.run_scrape_view, name='run_scrape'),
    path('github/', views.scrape_github_view, name='scrape_github'),
]


