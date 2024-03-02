from model.game import Game

game = Game()
# game.run()
from utils.saves import get_latest_save_file

game.load_history(filename=get_latest_save_file())
game.run_from_history()
