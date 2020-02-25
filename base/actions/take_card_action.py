import logging
from numbers import Number
from typing import TYPE_CHECKING

from base.actions.action import Action
from base.enums.game_phase import GamePhase

if TYPE_CHECKING:
    from base.board import Board
    from base.players.player import Player


class TakeCardAction(Action):
    """ Take a card from the deck and add it to the players hand. """

    def _key(self):
        """Return a tuple of all fields that should be checked in equality and hashing operations."""
        return None

    def get_reward(self) -> Number:
        return 0

    def validate(self, player: 'Player', board: 'Board', verbose: bool = False):
        if board.phase != GamePhase.DRAW_PHASE:
            if verbose:
                logging.info("Invalid action {}. Reason: wrong phase - {}".format(self, board.phase))
            return False
        return True

    def _execute(self, player: 'Player', board: 'Board'):
        deck_card = board.deck.deal()
        player.hand.add(deck_card)

    def _target_phase(self, player: 'Player', board: 'Board') -> GamePhase:
        return GamePhase.ACTION_PHASE

    def __str__(self):
        execution_tag = "" if not self.is_executed else "(E) "
        return "{}TakeCard".format(execution_tag)
