import uuid

from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    

class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    move_coordinates = models.CharField(max_length=7)
    date_created = models.DateTimeField(auto_now_add=True)

        


class Player(User):
    pass


