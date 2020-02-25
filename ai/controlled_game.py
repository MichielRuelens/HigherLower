from typing import List

from base.actions.action import Action
from base.actions.action_service import ActionService
from ai.controlled_player import ControlledPlayer
from base.constants import Constants
from base.game import Game


class ControlledGame(Game):

    def __init__(self):
        super().__init__()

    def play(self, verbose: bool = False):
        raise NotImplemented("The training game can only be played through the play_action() function.")

    def play_action(self, action: Action):
        if not self.initialized:
            raise Exception("Game not initialized")
        self.players[self.current_player_index].play_action(game_state=self.get_state(), action=action)

    def switch_player_turns(self):
        self._next_player_turn()

    def get_current_actions_mask(self) -> List[bool]:
        """Return a boolean mask representing the current valid actions."""
        return ActionService().get_valid_actions_mask(self.current_player, self.board)

    def _initialize_players(self) -> None:
        self.players = [ControlledPlayer(i) for i in range(Constants.NUM_PLAYERS)]
