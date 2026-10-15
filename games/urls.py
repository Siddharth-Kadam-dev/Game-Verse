from django.urls import path
from . import views

urlpatterns = [
    path('', views.games_view, name='games_list'),
]