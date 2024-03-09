from model.runer.runner import Runner, GUIRunner


class DummyRunner(Runner):

    def make_move(self):
        self.game.snake.turn_south()
        next_step_head_position = self.game.snake.get_new_head_position()
        if len(self.game.snake.tail) < self.game.arena_size:
            if next_step_head_position[1] == self.game.arena_size // 2:
                self.game.snake.turn_east()

        if next_step_head_position in self.game.get_deadly_positions():
            self.game.snake.turn_east()


class DummyRunnerGUI(GUIRunner, DummyRunner):
    pass
