import uuid
import json
from copy import copy

from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel

def into_json(data):
    return json.dump

class Game(TimeStampedModel):
    id = models.CharField(primary_key=True, default=uuid.uuid4().hex, editable=False, max_length=32)
    player1 = models.ForeignKey(User, related_name='Player1', on_delete=models.CASCADE, blank=False)
    player2 = models.ForeignKey(User, related_name='Player2', on_delete=models.CASCADE, blank=False)
    state = models.TextField(default="""{
            "(1,1)": 0,"(1,2)": 0,"(1,3)": 0,"(1,4)": 0,"(1,5)": 0,"(1,6)": 0,"(1,7)": 0,"(1,8)": 0,
            "(2,1)": 0,"(2,2)": 0,"(2,3)": 0,"(2,4)": 0,"(2,5)": 0,"(2,6)": 0,"(2,7)": 0,"(2,8)": 0,
            "(3,1)": 0,"(3,2)": 0,"(3,3)": 0,"(3,4)": 0,"(3,5)": 0,"(3,6)": 0,"(3,7)": 0,"(3,8)": 0,
            "(4,1)": 0,"(4,2)": 0,"(4,3)": 0,"(4,4)": 0,"(4,5)": 0,"(4,6)": 0,"(4,7)": 0,"(4,8)": 0,
            "(5,1)": 0,"(5,2)": 0,"(5,3)": 0,"(5,4)": 0,"(5,5)": 0,"(5,6)": 0,"(5,7)": 0,"(5,8)": 0,
            "(6,1)": 0,"(6,2)": 0,"(6,3)": 0,"(6,4)": 0,"(6,5)": 0,"(6,6)": 0,"(6,7)": 0,"(6,8)": 0,
            "(7,1)": 0,"(7,2)": 0,"(7,3)": 0,"(7,4)": 0,"(7,5)": 0,"(7,6)": 0,"(7,7)": 0,"(7,8)": 0,
            "(8,1)": 0,"(8,2)": 0,"(8,3)": 0,"(8,4)": 0,"(8,5)": 0,"(8,6)": 0,"(8,7)": 0,"(8,8)": 0
    }""")

    # Place token on board if it's a legal move 
    def place_token(self, move):
        if self.is_legal(move):
           serialized_state = json.loads(self.state) 
           if move.player == self.player1: 
               serialized_state[move.move_coordinates] = "J"
           elif move.player == self.player2: 
               serialized_state[move.move_coordinates] = "K"
           self.state = json.dumps(serialized_state)
           super().save()
           return True
        else:
           print("Illegal move")
           return False



    def is_legal(self, move):
        if self.is_occupied(move):
            return False 
        return True

        
    def is_occupied(self, move):
        serialized_state_for_legality = json.loads(self.state)
        # print(type(serialized_state_for_legality))
        # print(serialized_state_for_legality)
        # print(serialized_state_for_legality[move.move_coordinates])
        if serialized_state_for_legality[move.move_coordinates] == "J" or serialized_state_for_legality[move.move_coordinates] == "K":
             return True
        return False
    


    


class Move(TimeStampedModel):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="move_player")
    # Sanitizing the input with e.g Regex would be necassary, but is skipped here for brevity
    move_coordinates = models.CharField(max_length=15, blank=False) 
    
    def save(self, *args, **kwargs):
        current_game = Game.objects.get(id=self.game_id)
        if current_game.place_token(self):
            super().save(*args, **kwargs)
        else:
            print("Could not save move from move")
