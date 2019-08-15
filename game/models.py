import uuid
import json
from copy import copy
import re


from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel

# Eschew using constants for sake of simplicity
class Game(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=32)
    # Referring to User model directly since I have no plans to 
    player1 = models.ForeignKey(User, related_name='Player1', on_delete=models.CASCADE, blank=False)
    player2 = models.ForeignKey(User, related_name='Player2', on_delete=models.CASCADE, blank=True, null=True)
    game_over = models.BooleanField(default=False)
    winner = models.ForeignKey(User, related_name='Winner', on_delete=models.CASCADE, blank=True, null=True)
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

     
    def place_token(self, move):
        """
        Place token on board if it's a legal move, save to the database
        then check if a win has occured 
        """
        if self.game_over == True:
            print("Game over")
            return False
        if self.is_legal(move):
           serialized_state = json.loads(self.state) 
           if move.player == self.player1: 
               serialized_state[move.move_coordinates] = "J"
           elif move.player == self.player2: 
               serialized_state[move.move_coordinates] = "K"
           self.state = json.dumps(serialized_state)
           super().save()
           if self.is_winner(move):
               self.game_over = True
               winner = move.player
               print(winner, "is winner")
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

    def increment_coordinates(self, coordinates, x_amount, y_amount):
            coordinates = list(coordinates)[:]
            if x_amount:
                axis_value = 1
                original_value = int(coordinates[axis_value])
                coordinates[axis_value] = str(original_value + x_amount)
            if y_amount:
                axis_value = 3
                original_value = int(coordinates[axis_value])
                coordinates[axis_value] = str(original_value + y_amount)
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
        coordinates = self.increment_coordinates(coordinates, -1, 0)
        if self.who_is_there(coordinates):
            print("There is something to my left")
            return True
        # transform original move coordinates (x,y) to (x+1, y) to check rightwards
        coordinates = copy(move.move_coordinates)
        coordinates = self.increment_coordinates(coordinates, 1, 0)
        if self.who_is_there(coordinates):
            print("There is something to my right")
            return True
        print("far from the wall")       
        return False


        
    def count_five_tokens(self, coordinates, player_token_letter, x_amount, y_amount):
            """
            Counts five tokens from (x,y) by incrementally cheking (x+x_amount, y+y_amount) 
            """
            player_tokens = 0
            for i in range(5):
                print("At loop", i, "I'm at coordinates", coordinates)
                if coordinates[1] == '0' or coordinates[3] == '0' or coordinates[1] == '9' or coordinates[3] == '9':
                    break 
                if self.who_is_there(coordinates) == player_token_letter:
                    player_tokens += 1
                    print("at coordinates", coordinates, "I count", player_tokens)
                coordinates = self.increment_coordinates(coordinates, x_amount, y_amount)
            if player_tokens == 5:
                print("There are five tokens!")
                return True
            else:
                return False
                       

    def is_winner(self, move):
            if self.is_winner_vertically(move):
                print("Vertical win!")
                return True
            if self.is_winner_horizontally(move):
                print("Horizontal win!")
                return True
    
    def is_winner_vertically(self, move):
            if self.count_five_tokens(move.move_coordinates, "J", 0, 1):
                return True
            if self.count_five_tokens(move.move_coordinates, "J", 0, -1):
                return True
            if self.count_five_tokens(move.move_coordinates, "K", 0, 1):
                return True
            if self.count_five_tokens(move.move_coordinates, "K", 0, -1):
                return True
            return False
                                    

    def is_winner_horizontally(self, move):
            if self.count_five_tokens(move.move_coordinates, "J", 1, 0):
                return True
            if self.count_five_tokens(move.move_coordinates, "J", -1, 0):
                return True
            if self.count_five_tokens(move.move_coordinates, "K", 1, 0):
                return True
            if self.count_five_tokens(move.move_coordinates, "K", -1, 0):
                return True
            return False
        
    def is_winner_p_diagonal(self, move):
            pass

    def is_winner_n_diagonal(self, move):
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