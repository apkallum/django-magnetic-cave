from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Game, Move

class GameDetailView(generic.DetailView):
    model = Game

class GameCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Game
    fields = ['player2']

    def get_initial(self):
        initial = super().get_initial()
        initial['player1'] = self.request.user.username