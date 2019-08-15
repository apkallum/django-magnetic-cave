from django.urls import path

from .views import GamePlayView
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('<str:id>', GamePlayView, name='GamePlayView'),
]