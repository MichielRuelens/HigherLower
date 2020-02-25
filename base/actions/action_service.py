from copy import copy
from typing import List

from base.actions.action import Action
from base.actions.play_card_action import PlayCardAction
from base.actions.take_card_action import TakeCardAction
from base.cards.card import Card
from base.players.player import Player

from base.board import Board
from base.utils.card_constants import POSSIBLE_SUIT, POSSIBLE_RANK
from base.utils.singleton import Singleton


class ActionService(metaclass=Singleton):

    def __init__(self):
        self._all_actions = (list(self._get_take_card_actions()) +
                             list(self._get_play_card_actions()))  # type: List['Action']
        self.num_actions = len(self._all_actions)
        self._action_to_idx = {action: i for i, action in enumerate(self._all_actions)}
        self._idx_to_action = {i: action for action, i in self._action_to_idx.items()}

    @staticmethod
    def _get_take_card_actions() -> List['Action']:
        yield TakeCardAction()

    @staticmethod
    def _get_play_card_actions() -> List['Action']:
        for suit in POSSIBLE_SUIT:
            for rank in POSSIBLE_RANK:
                yield PlayCardAction(card=Card(rank, suit))

    def action_to_idx(self, action: 'Action') -> int:
        """Return the unique index associated with the given action."""
        return self._action_to_idx[action]

    def idx_to_action(self, index: int) -> 'Action':
        """Return the action associated with the given unique index."""
        # Always return a copy so a unique action object is obtained
        return copy(self._idx_to_action[index])

    def get_valid_actions(self, player: 'Player', board: 'Board') -> List['Action']:
        """Return a list of all valid actions for the given player on the given board."""
        # Make sure to return copies of each action so they can be executed later on
        return [copy(a) for a in self._all_actions if a.validate(player=player, board=board)]

    def get_valid_actions_mask(self, player: 'Player', board: 'Board') -> List[bool]:
        """Return a boolean mask corresponding to the unique indexes representing the current valid actions."""
        return [a.validate(player=player, board=board) for a in self._all_actions]
