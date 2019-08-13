import uuid
import json
from copy import copy
import re


from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel

def into_json(data):
    return json.dump

class Game(TimeStampedModel):
    id = models.CharField(primary_key=True, default=uuid.uuid4().hex, editable=False, max_length=32)
    # Referring to User model directly since I have no plans to 
    player1 = models.ForeignKey(User, related_name='Player1', on_delete=models.CASCADE, blank=False)
    player2 = models.ForeignKey(User, related_name='Player2', on_delete=models.CASCADE, blank=False)
    game_over = models.BooleanField(default=False)
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

        def who_is_there(self, coordinates: str):
            serialized_state_for_legality = json.loads(self.state)
            if serialized_state_for_legality[coordinates] == "J":
                return "J"
            elif serialized_state_for_legality[coordinates] == "K":
                return "K"
            else:
                return 0


    def increment_coordinates(self, coordinates: str, axis: str, amount: int) -> str:
        coordinates = list(coordinates)[:]
        if axis == "x-axis":
            axis_value = 1
        elif axis == "y-axis":
            axis_value = 3
        original_value = int(coordinates[axis_value])
        coordinates[axis_value] = str(original_value + amount)
        coordinates = "".join(coordinates)
        return coordinates

    def is_legal(self, move) -> bool:
        if not self.is_valid_magnetically(move):
            return False 
        if self.is_occupied(move):
            return False
        return True
        

       
        
    def is_occupied(self, move) -> bool:
        serialized_state_for_legality = json.loads(self.state)
        if serialized_state_for_legality[move.move_coordinates] == "J" or serialized_state_for_legality[move.move_coordinates] == "K":
            print("It's occupied")
            return True
        return False


 
            
    def is_valid_magnetically(self, move):
        """
        Check a token can be placed against the walls.
        """
        # Check if against the wall
        if move.move_coordinates[1] == '1' or move.move_coordinates[1] == '8':
            print("I'm against the wall")
            return True
        # transform original move coordinates (x,y) to (x-1,y), to check leftwards
        coordinates = copy(move.move_coordinates)
        coordinates = self.increment_coordinates(coordinates, "x-axis", 1)
        if self.who_is_there(coordinates):
            print("There is something to my left")
            return True
        # transform original move coordinates (x,y) to (x+1, y) to check rightwards
        coordinates = copy(move.move_coordinates)
        coordinates = self.increment_coordinates(coordinates, "x-axis", 1)
        if self.who_is_there(coordinates):
            print("There is something to my right")
            return True
        print("far from the wall")       
        return False

        def is_winner(self, move):
            pass
    
        




    


class Move(TimeStampedModel):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="move_player")
    # Sanitizing the input with e.g Regex would be necassary, but is skipped here for brevity
    move_coordinates = models.CharField(max_length=15, blank=False) 
    
    def save(self, *args, **kwargs):
        coordinates_for_test = self.move_coordinates
        if type(coordinates_for_test) is not str:
            print("Invalid Input not string")
        else:
            valid_coordinates = re.fullmatch(r'([(]{1}[1-8]{1}[,][1-8]{1}[)]{1})', coordinates_for_test)
            if valid_coordinates:
                current_game = Game.objects.get(id=self.game_id)
                if current_game.place_token(self):
                    super().save(*args, **kwargs)
                else:
                    print("Could not save move from move")
            else:
                print("Invalid coordinates")