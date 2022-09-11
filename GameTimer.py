from Character import Enemy

DEFAULT_TIME_STEP = 5


class GameTimer:
    def __init__(self):
        self.tick = 0
        self.game_time = 0
        self.last_tick_elapsed = 0

        self.player_has_control = True

        self.listeners = []

    def register_listener(self, listener: Enemy):
        self.listeners.append(listener)

    def advance_time(self, action_type):
        time_step = DEFAULT_TIME_STEP

        if action_type is not None:
            pass

        self.tick += 1
        self.game_time += time_step
        self.last_tick_elapsed = time_step

    def tick(self):
        if self.player_has_control:
            return

        self.advance_time(None)
