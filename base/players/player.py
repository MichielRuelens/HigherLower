from abc import ABCMeta, abstractmethod
from typing import Optional, TYPE_CHECKING
from base.cards.hand import Hand

if TYPE_CHECKING:
    from base.game_state import GameState
    from base.actions.action import Action


class Player(metaclass=ABCMeta):

    def __init__(self, identifier: int):
        self.hand = None  # type: Optional[Hand]
        self.identifier = identifier
        self.score = 0

    @property
    @abstractmethod
    def is_human(self):
        raise NotImplementedError

    @abstractmethod
    def _choose_action(self, game_state: 'GameState', verbose: bool = False) -> 'Action':
        """
        Return an action to take given the current GameState.

        The chosen action must be an eligible one given the current state, invalid actions will result in an Exception.
        A valid series of actions will always result in a END_TURN_PHASE game phase which ends the players turn.
        """
        raise NotImplementedError

    def play_single_step(self, game_state: 'GameState', verbose: bool = False):
        """
        Play a single move based on the given GameState.

        :param game_state: the current state of the game
        :param verbose: if True, print extra information to the console
        :return: the action taken by the player
        """
        action = self._choose_action(game_state, verbose=verbose)
        if verbose:
            print("Executing {}".format(action))
        action.execute(self, game_state.board)
        self.score += action.get_reward()
        return action

    def deal(self, hand: Hand):
        self.hand = hand

    def num_cards(self) -> int:
        return self.hand.num_cards()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        print_str = str(self.identifier) + "\n"
        print_str += str(self.hand)
        return print_str
