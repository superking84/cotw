from Enemy import Enemy

DEFAULT_TIME_STEP = 5


class GameTimer:
    def __init__(self):
        self.total_ticks = 0
        self.total_game_time = 0
        self.last_tick_elapsed = 0

        self.days_elapsed: int = 0
        self.hours_elapsed: int = 0
        self.minutes_elapsed: int = 0
        self.seconds_elapsed: int = 0

        self.player_has_control = True

        self.listeners = []

    def register_listener(self, listener: Enemy):
        self.listeners.append(listener)

    def advance_time(self, elapsed_time: int):
        elapsed_time = elapsed_time or DEFAULT_TIME_STEP

        # if action_type is not None:
        #     pass

        self.total_ticks += 1
        self.total_game_time += elapsed_time
        self.update_game_time(elapsed_time)
        self.last_tick_elapsed = elapsed_time

        for listener in self.listeners:
            listener.process_time(elapsed_time)

    def tick(self):
        if self.player_has_control:
            return

        self.advance_time(None)

    def update_game_time(self, elapsed_time: int):
        self.seconds_elapsed += elapsed_time
        if self.seconds_elapsed >= 60:
            self.seconds_elapsed %= 60
            self.minutes_elapsed += 1

        if self.minutes_elapsed >= 60:
            self.minutes_elapsed %= 60
            self.hours_elapsed += 1

        if self.hours_elapsed >= 24:
            self.hours_elapsed %= 24
            self.days_elapsed += 1

    def get_game_time(self):
        return f"{self.days_elapsed}d, {self.hours_elapsed:02}:{self.minutes_elapsed:02}:{int(self.seconds_elapsed):02}"
