from enum import Enum


class GamePhase(Enum):

    DRAW_PHASE = 0  # player turn phase, drawing a card from the deck
    ACTION_PHASE = 1  # player turn phase, player executes an actions on the board
    END_TURN_PHASE = 2  # phase indicating end of current players turn
