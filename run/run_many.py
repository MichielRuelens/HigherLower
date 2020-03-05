from collections import defaultdict

from numpy import mean

from run.game_runner import GameRunner


def get_winner(g):
    player_0 = g.players[0]
    player_1 = g.players[1]
    if player_0.score > player_1.score:
        return player_0, player_0.score - player_1.score
    return player_1, player_0.score - player_1.score


if __name__ == '__main__':
    game_runner = GameRunner()

    winners = defaultdict(int)
    score_deltas = []
    for i in range(1000):
        print("Playing game {}".format(i + 1))
        game_id, game = game_runner.start_game()
        while not game.is_finished():
            game.play_single_step()
        winner, delta = get_winner(game)
        winners[winner.identifier] += 1
        score_deltas.append(delta)
    print("Winners: {}".format(winners))
    print("With an average delta of {}".format(mean(score_deltas)))
