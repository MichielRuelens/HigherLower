from typing import List, Optional

from ai.model_configs.mlp_config import MLPConfig
from base.board import Board
from base.cards.deck import Deck
from base.cards.hand import Hand
from base.constants import Constants
from base.enums.game_phase import GamePhase
from base.game_history import GameHistory
from base.game_state import GameState
from base.players.ai_player import AIPlayer
from base.players.human_player import HumanPlayer
from base.players.player import Player
from base.players.random_player import RandomPlayer


class Game:

    def __init__(self, keep_history: bool = False):
        self.players = None  # type: Optional[List[Player]]
        self.current_player_index = None
        self.board = None  # type: Optional[Board]
        self.keep_history = keep_history
        self.history = GameHistory()
        self.initialized = False

    def reset_game(self, initialize: bool = True, keep_players: bool = False, clear_history: bool = True) -> None:
        """
        Reset the current game.

        :param initialize: if True, re-initialize the game after the reset
        :param keep_players: if True, don't delete the player objects (can be useful for keeping AI models loaded)
                             Note that hands are cleared even when the players are kept.
        :param clear_history: if True, clear the history (if kept)
        """
        if not keep_players:
            self.players = None  # type: Optional[List[Player]]
        else:
            # We're not killing the players, but they have to be reset (e.g. score set to 0)
            for player in self.players:
                player.reset()
        self.current_player_index = None
        self.board = None  # type: Optional[Board]
        if clear_history:
            self.history.clear()
        self.initialized = False
        if initialize:
            self.initialize_game(initialize_players=not keep_players)

    def initialize_game(self, initialize_players: bool = True):
        if not self.initialized:
            self.current_player_index = 0
            # Initialize players
            if initialize_players:
                self._initialize_players()
            # Create new deck
            deck = self._create_deck()
            # Deal player hands
            self._deal_hands(deck)
            # Set up board (deck & stack)
            self._initialize_board(deck)
            # Set up game phase
            self.board.set_phase(GamePhase.DRAW_PHASE)
            self.initialized = True
            if self.keep_history:
                self.history.add(self, None)

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def play_single_step(self, verbose: bool = False):
        """Play a single action in the game."""
        if not self.initialized:
            raise Exception("Game not initialized")
        if not self.is_finished():
            if verbose:
                self.print()
                print("Current player: {}".format(self.current_player_index))
            action = self.players[self.current_player_index].play_single_step(self.get_state(), verbose=verbose)
            if self.keep_history:
                self.history.add(self, action)
            if self.board.phase == GamePhase.END_TURN_PHASE:
                self._next_player_turn()

    def get_state(self) -> GameState:
        """Return the current GameState of this Board."""
        return GameState(self.board, self.players, self.current_player_index)

    def is_finished(self) -> bool:
        """
        Return True if the game is finished.

        The game is finished when one of the players has no cards left and there are no more cards in the deck.
        """
        if self.board.deck.is_empty():
            if all([player.hand.is_empty() for player in self.players]):
                return True
        return False

    def _next_player_turn(self) -> None:
        """Increment the player and team counters to indicate it's now the next players turn."""
        self.current_player_index += 1
        self.current_player_index %= Constants.NUM_PLAYERS
        if self.board.deck.is_empty():
            self.board.set_phase(GamePhase.ACTION_PHASE)
        else:
            self.board.set_phase(GamePhase.DRAW_PHASE)

    def _initialize_players(self) -> None:
        self.players = []
        for i in range(Constants.NUM_PLAYERS):
            if i in Constants.HUMAN_PLAYER_INDEXES:
                self.players.append(HumanPlayer(i))
            elif i in Constants.RANDOM_PLAYER_INDEXES:
                self.players.append(RandomPlayer(i))
            elif i in Constants.AI_PLAYER_INDEXES:
                self.players.append(AIPlayer(i, MLPConfig()))

    @staticmethod
    def _create_deck() -> Deck:
        deck = Deck(with_jokers=False)
        deck.shuffle()
        return deck

    def _deal_hands(self, deck: Deck):
        """Deal cards from the deck to each player to create a their starting hands."""
        # Draw cards from the deck
        hands = [Hand(deck.deal_n(Constants.NUM_CARDS_IN_STARTING_HAND)) for _ in range(len(self.players))]
        # Hand the cards to each player
        for i, player in enumerate(self.players):
            player.deal(hands[i])

    def _initialize_board(self, deck):
        self.board = Board(deck=deck)
        # Deal 1 card onto the stack.
        card = self.board.deck.deal()
        self.board.stack.put(card)

    def print(self):
        if self.players is not None:
            for player in self.players:
                print(player)
        else:
            print("No players.")
        if self.board is not None:
            print(self.board)
        else:
            print("No board.")
