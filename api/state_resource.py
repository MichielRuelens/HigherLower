import json

from flask import request
from flask_restful import Resource

from base.game import Game
from run.game_runner import GameRunner


class StateResource(Resource):

    def get(self):
        """Get the state (as JSON) of the game identified by the gameId parameter"""
        args = request.args
        game_id = args["gameId"]
        game = GameRunner().get_game(game_id)
        if game:
            return self.game_to_json(game)
        return "Game not found", 204

    @staticmethod
    def game_to_json(game: Game) -> str:
        players = [{"playerId": player.identifier,
                    "isCurrentPlayer": idx == game.current_player_index,
                    "isHuman": player.is_human,
                    "numCards": player.num_cards(),
                    "score": player.score,
                    "cards": [{"rank": card.get_rank(),
                               "suit": card.get_suit(),
                               "shortRank": card.translate_rank_short() if not card.is_joker() else "J",
                               "shortSuit": card.get_suit()[0].upper(),
                               "isJoker": card.is_joker()
                              } for card in sorted(player.hand)],
                    } for idx, player in enumerate(game.players)]
        top_card = game.board.stack.look()
        stack_top_card_dict = {"rank": top_card.get_rank(),
                               "suit": top_card.get_suit(),
                               "shortRank": top_card.translate_rank_short() if not top_card.is_joker() else "J",
                               "shortSuit": top_card.get_suit()[0].upper()
                              } if top_card is not None else None
        return json.dumps(indent=2, obj={
            "isFinished": game.is_finished(),
            "phase": game.board.phase.name,
            "currentPlayerIndex": game.current_player_index,
            "players": players,
            "deck": {"numCards": game.board.deck.num_cards()},
            "stack": {"numCards": game.board.stack.num_cards(),
                      "topCard": stack_top_card_dict},
        })
