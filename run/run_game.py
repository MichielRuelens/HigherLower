from run.game_runner import GameRunner

if __name__ == '__main__':
    game_runner = GameRunner()
    game_id, game = game_runner.start_game()
    while input("play?") == "y":
        game.play_single_step(verbose=False)
