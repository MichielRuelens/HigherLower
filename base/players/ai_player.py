from typing import TYPE_CHECKING

import numpy as np
import tensorflow as tf

from ai.multi_layer_perceptron import MultiLayerPerceptron
from base.actions.action_service import ActionService
from base.players.player import Player

if TYPE_CHECKING:
    from base.game_state import GameState
    from base.actions.action import Action


class AIPlayer(Player):

    def __init__(self, identifier: int):
        super().__init__(identifier=identifier)
        self.action_service = ActionService()
        self.model = self._load_model()

    def _load_model(self):
        model = MultiLayerPerceptron(num_states=GameState.SIZE,
                                     num_hidden_units=[200, 200],
                                     num_actions=self.action_service.num_actions)
        model.load_weights("models/mlp_weights")
        return model

    def _predict(self, game_state: GameState):
        return self.model.predict({"state": np.atleast_2d(game_state.create_numeral_representation(self))})

    @property
    def is_human(self):
        return False

    def _choose_action(self, game_state: 'GameState', verbose: bool = False) -> 'Action':
        predictions = self._predict(game_state=game_state)
        mask = self.action_service.get_valid_actions_mask(self, game_state.board)
        proper_predictions = predictions * np.atleast_2d(mask)
        masked_predictions = np.atleast_2d(np.logical_not(mask) * (np.min(predictions) - 1))
        predictions = proper_predictions + masked_predictions
        action_idx = np.argmax(predictions[0])  # type: int
        return self.action_service.idx_to_action(action_idx)


if __name__ == '__main__':
    p = AIPlayer()
    print(p)
    print(p.model)
