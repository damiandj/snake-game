# from model.game import Game
#
# game = Game()
# # game.run()
# from utils.saves import get_latest_save_file
#
# game.load_history(filename=get_latest_save_file())
# game.run_from_history()
# from model.game.game import SnakeGame
# from model.game.game_gui import GameGui
#
# #
# g = SnakeGame(arena_size=25)
# g.initialize_game()
# g.snake.direction = [0, 1]
# g.step()
# g.snake_eat_mouse()
# for _ in range(1000):
#     g.step()
#
# gui = GameGui(game=g)
# gui.draw_history()
from model.runer.user_gui_runner import UserGuiRunner

game = UserGuiRunner()
game.run()
