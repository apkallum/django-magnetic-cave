from django.shortcuts import render

def index(request):
    return render(request, 'game/game_list.html')

