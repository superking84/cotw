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
        """
        Add an Enemy to the list of Enemy objects currently receiving time
        updates from the GameTimer.
        :return: None
        """
        if listener not in self.listeners:
            self.listeners.append(listener)

    def unregister_listener(self, listener: Enemy):
        """
        Remove an Enemy from the list of Enemy objects currently receiving time
        updates from the GameTimer.
        :return: None
        """
        if listener in self.listeners:
            listener_index = self.listeners.index(listener)

            self.listeners.pop(listener_index)

    def advance_time(self, elapsed_time: int):
        """
        Increase the elapsed in-game time by the specified number of seconds.
        :param elapsed_time: An amount of time in seconds.
        :return: None
        """
        elapsed_time = elapsed_time or DEFAULT_TIME_STEP

        self.total_ticks += 1
        self.total_game_time += elapsed_time
        self.update_game_time(elapsed_time)
        self.last_tick_elapsed = elapsed_time

        for listener in self.listeners:
            listener.process_time(elapsed_time)

    def tick(self):
        """
        Advance the game by one tick. Ticks are distinct from game time, as
        :return:
        """
        if self.player_has_control:
            return

        self.advance_time(None)

    def update_game_time(self, elapsed_time: int):
        """
        Calculates the seconds, minutes, hours, and days of elapsed in-game time.
        :param elapsed_time: The total elapsed time, in seconds.
        :return:
        """
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
