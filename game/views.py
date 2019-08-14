from django.shortcuts import render,redirect, reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Game, Move
from .forms import MoveForm

@login_required
def index(request):
    player_id = request.user.id
    form = MoveForm(initial={'game': game.id, 'player_id': player_id})
    print(form)
    move_coordinates = request.POST.get('move_coordinates')
    Move.objects.create(game_id=game.id, player_id=player_id, move_coordinates=move_coordinates)
    context = {'game': game, 'form': form}
    return render(request, "game/game.html", context)

@login_required
def GamePlayView(request, id):
    game_id = id
    game = Game.objects.get(id=game_id)
    player_id = request.user.id
    form = MoveForm(request.POST)
    if request.method == "POST":
        move_coordinates = request.POST.get('move_coordinates')
        Move.objects.create(game_id = game.id, player_id = player_id, move_coordinates = move_coordinates)
        return redirect('./' + game.id)
    context = {
        'game': game,
        'form': form
    }
    return render(request, "game/game.html", context)

class GameCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Game
    fields = ['player2']

    def get_initial(self):
        initial = super().get_initial()
        initial['player1'] = self.request.user.username