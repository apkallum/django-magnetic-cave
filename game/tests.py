from django.test import TestCase

from django.contrib.auth.models import User
from .models import Game, Move

# Create your tests here.
class GameModelTest(TestCase):
    def setUp(self):
        u1 = User.objects.create(username='good_player')
        u2 = User.objects.create(username='bad_player')
        game = Game.objects.create(player1_id=2)
    

    # def test_legal_move_against_wall(self):
    #     game = Game.objects.latest('created')
    #     print(game.state)
    #     Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(1,3)")
    #     move = Move.objects.latest('created')
    #     self.assertEqual(move.move_coordinates, "(1,3)")
    
    # def test_legal_move_against_token(self):
    #     game = Game.objects.latest('created')
    #     print(game.state)
    #     Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(1,3)")
    #     move = Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(2,3)")
    #     self.assertEqual(move.move_coordinates, "(2,3)")

    # def test_illegal_move_far_from_wall(self):
    #     game = Game.objects.latest('created')
    #     print(game.state)
    #     Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(2,3)")
    #     self.assertRaises(Move.DoesNotExist, Move.objects.latest,'created')
    
    # def test_illegal_move_already_occupied(self):
    #     game = Game.objects.latest('created')
    #     Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(2,3)")
    #     Move.objects.create(game_id = game.id, player_id=1, move_coordinates = "(2,3)")
    #     self.assertRaises(Move.DoesNotExist, Move.objects.get, player_id=1)

    # def test_no_win(self):
    #     game = Game.objects.latest('created')
    #     Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(3,1)")
    #     Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(1,2)")       
    #     self.assertEqual(game.game_over, False)
    
    
    def test_vertical_win(self):
        game = Game.objects.latest('created')
        Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(8,1)")
        Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(8,2)")
        Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(8,3)")
        Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(8,4)")
        Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(8,5)")
        game = Game.objects.latest('created')
        print(game.state)
        self.assertEqual(game.game_over, True)

    def test_horizontal_win(self):
        game = Game.objects.latest('created')
        Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(1,1)")
        Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(2,1)")
        Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(3,1)")
        Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(4,1)")
        Move.objects.create(game_id = game.id, player_id=2, move_coordinates = "(5,1)")
        game = Game.objects.latest('created')
        print(game.state)
        self.assertEqual(game.game_over, True)

       