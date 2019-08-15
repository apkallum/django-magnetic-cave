from django.shortcuts import render,redirect, reverse, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import Game, Move
from .forms import MoveForm

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
    game = get_object_or_404(Game, id=game_id)
    player_id = request.user.id
    form = MoveForm(request.POST)
    if not game.player2_id:
        game.player2_id = request.user.id
    if request.method == "POST":
        move_coordinates = request.POST.get('move_coordinates')
        Move.objects.create(game_id = game.id, player_id = player_id, move_coordinates = move_coordinates)
        return redirect('GamePlayView', game.id)
    context = {
        'game': game,
        'form': form
    }
    return render(request, "game/game.html", context)

