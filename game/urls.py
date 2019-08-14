from django.urls import path

from .views import GamePlayView, GameCreateView
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('create/', GameCreateView.as_view(), name="create"),
    path('<str:id>', GamePlayView, name='GamePlayView'),
]