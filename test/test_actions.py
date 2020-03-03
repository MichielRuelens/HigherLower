from unittest import TestCase

from base.actions.action_service import ActionService
from base.actions.play_card_action import PlayCardAction
from base.actions.take_card_action import TakeCardAction
from base.cards.card import Card
from base.enums.game_phase import GamePhase
from base.game import Game
from base.utils.card_constants import HEARTS


class TestActions(TestCase):

    def setUp(self) -> None:
        self.game = Game()
        self.game.initialize_game()

    def test_take_card(self):
        # Execute a put action for the first player
        target_player = self.game.players[0]
        original_deck_num_cards = self.game.board.deck.num_cards()
        original_player_num_cards = target_player.hand.num_cards()
        self.game.board.set_phase(GamePhase.DRAW_PHASE)
        take_card_action = TakeCardAction()
        # Ensure the player can perform the play card action
        validated_actions = ActionService().get_valid_actions(target_player, self.game.board)
        self.assertIn(take_card_action, validated_actions)
        # Execute the action
        take_card_action.execute(target_player, self.game.board)
        # Ensure a card has been added to the players hand
        self.assertEqual(target_player.hand.num_cards(), original_player_num_cards + 1)
        # Ensure the deck has lost 1 card
        self.assertEqual(self.game.board.deck.num_cards(), original_deck_num_cards - 1)

    def test_play_card(self):
        # Execute a put action for the first player
        target_player = self.game.players[0]
        target_card = Card(12, HEARTS)
        self.game.board.set_phase(GamePhase.ACTION_PHASE)
        target_player.hand.clear()
        target_player.hand.add(Card(1, HEARTS))  # random card so hand isn't empty
        target_player.hand.add(target_card)
        play_card_action = PlayCardAction(target_card)
        # Ensure the player can perform the play card action
        validated_actions = ActionService().get_valid_actions(target_player, self.game.board)
        self.assertIn(play_card_action, validated_actions)
        # Execute the action
        play_card_action.execute(target_player, self.game.board)
        # Ensure the card has been played
        self.assertEqual(target_card, self.game.board.stack.look())
        # Ensure the card has been removed from the players hand
        self.assertNotIn(target_card, target_player.hand)
