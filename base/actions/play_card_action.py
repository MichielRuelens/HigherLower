import logging
from numbers import Number
from typing import TYPE_CHECKING

from base.cards.card import Card

from base.actions.action import Action
from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.board import Board
    from base.players.player import Player


class PlayCardAction(Action):

    def __init__(self, card: Card):
        super().__init__()
        self.card = card
        self.score = None

    def _key(self):
        """Return a tuple of all fields that should be checked in equality and hashing operations."""
        return self.card

    def get_reward(self) -> Number:
        return self.score

    def validate(self, player: 'Player', board: 'Board', verbose: bool = False):
        # Check the board phase
        if board.phase != GamePhase.ACTION_PHASE:
            if verbose:
                logging.info("Invalid action {}. Reason: wrong phase - {}".format(self, board.phase))
            return False
        # Make sure the player discard a card it currently holds in its hand
        if self.card not in player.hand:
            return False
        return True

    def _execute(self, player: 'Player', board: 'Board'):
        card = player.hand.pop(self.card)
        top_card = board.stack.look()
        board.stack.put(card)
        # Only playing a higher card results in points
        card_difference = self.card.get_rank() - top_card.get_rank()
        self.score = card_difference if card_difference > 0 else 0

    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        return GamePhase.END_TURN_PHASE

    def __str__(self):
        execution_tag = "" if not self.is_executed else "(E) "
        return "{}Play card {}".format(execution_tag, self.card)
