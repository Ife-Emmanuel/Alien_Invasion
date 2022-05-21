import rocket_game_functions as rgf
class GameStats():
    """Track statistics for Alien Invasion."""

    def __init__(self, a1_settings):
        """Initialize statistics."""
        self.a1_settings = a1_settings
        self.high_score = rgf.get_data('highest_score', 0)
        self.reset_stats()
        self.partial_reset()
        # Start Alien Invasion in an active state.
        self.game_active = False
        self.state = 1

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.rocket_left = self.a1_settings.rocket_limit
        self.score = 0
    def partial_reset(self):
        """It was not added to reset_stats() so that if player wants to continue from the previous level he can; the rocket and score being reset but speed and scoring settings left unchanged. """
        rgf.store_data('level', 1)
        self.level = rgf.get_data('level', 1)

    def increase_stats(self):
        self.level += 1
