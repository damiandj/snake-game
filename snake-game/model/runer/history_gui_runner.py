from pathlib import Path

import pygame

from model.game import SnakeGame
from model.gui import GameGui
from model.history import GameHistory


class HistoryGuiRunner(GameGui):
    def __init__(self, history_file_path: Path):
        history = GameHistory()
        history.load(filename=history_file_path)
        arena_size = history[0].arena.size
        game = SnakeGame(arena_size=arena_size)
        super().__init__(game)
        self.game.history = history

    def run(self):
        """Draw the game history."""
        self.initialize()
        clock = pygame.time.Clock()
        for game_stage in self.game.history:
            if self.check_if_quit():
                break
            self.draw_step(game_stage)
            clock.tick(60)
            pygame.display.update()
