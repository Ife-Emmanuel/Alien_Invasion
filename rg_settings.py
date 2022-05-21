import pygame
import rocket_game_functions as rgf
class Settings:
    def __init__(self):
        """Initialize the game's static settings."""
        #Screen settings
        self.screen_width = 1280
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.bg_colour = (230, 230, 230)
        self.screen_rect = self.screen.get_rect()

        #Rocket settings
        self.image_path = r'images/rocket.bmp'
        self.rocket_limit = 3

        #Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = 60, 60, 60
        self.bullets_allowed = 3

        #Alien settings
        self.fleet_drop_speed = 3
        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        # How quickly the point values increase
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        rgf.store_data('rocket_speed_factor', 1.3)
        self.rocket_speed_factor = rgf.get_data('rocket_speed_factor', 1.3)
        rgf.store_data('bullet_speed_factor', 3)
        self.bullet_speed_factor = rgf.get_data('bullet_speed_factor', 3)
        rgf.store_data('alien_speed_factor', 1)
        self.alien_speed_factor = rgf.get_data('alien_speed_factor', 1)
        rgf.store_data('alien_points', 50)
        self.alien_points = rgf.get_data('alien_points', 50)
        self.fleet_direction = 1 # fleet direction of 1 represents right; -1 represents left.

    def increase_speed(self):
        """Increase speed settings."""
        self.rocket_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # Scoring


