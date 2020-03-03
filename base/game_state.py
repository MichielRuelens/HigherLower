from typing import List, TYPE_CHECKING

from base.board import Board
from base.cards.card_encoder import CardEncoder


if TYPE_CHECKING:
    from base.players.player import Player


class GameState:
    """
    The full current state of the game.
    The game state contains all necessary information for a player to determine the next action.
    """

    SIZE = 115  # Total number of integers required to represent the game state

    def __init__(self, board: Board, players: List['Player'], current_player_index: int):
        self.board = board
        self.players = players
        self.current_player_index = current_player_index

    def create_numeral_representation(self, player: 'Player') -> List[int]:
        """
        Create a numerical representation of (a subset of) the game state for the specified player.

        This representation only contains information that is accessible to the specified player.
        """
        representation = []
        representation.extend(self._own_player_index_representation(player=player))
        representation.extend(self._current_player_representation())
        representation.extend(self._player_hand_representation(player=player))
        representation.extend(self._top_stack_card_representation())
        representation.extend(self._players_num_cards_representation())
        representation.extend(self._deck_num_cards_representation())
        representation.extend(self._get_own_score_representation(player=player))
        representation.extend(self._get_other_players_score_representation(player=player))
        return representation

    @staticmethod
    def _own_player_index_representation(player: 'Player'):
        return [player.identifier]

    def _current_player_representation(self):
        return [self.current_player_index]

    @staticmethod
    def _player_hand_representation(player: 'Player'):
        return list(CardEncoder().encode(player.hand.get_raw_cards()))

    def _top_stack_card_representation(self):
        return list(CardEncoder().encode(self.board.stack.look()))

    def _players_num_cards_representation(self):
        return [player.num_cards() for player in self.players]

    def _deck_num_cards_representation(self):
        return [self.board.deck.num_cards()]

    @staticmethod
    def _get_own_score_representation(player: 'Player'):
        return [player.score]

    def _get_other_players_score_representation(self, player: 'Player'):
        other_player_scores = []
        for other_player in self.players:
            if player.identifier != other_player.identifier:
                other_player_scores.append(other_player.score)
        return other_player_scores
