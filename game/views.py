from django.shortcuts import render
from django.views import generic
from .models import Game

class GameDetailView(generic.DetailView):
    model = Game

