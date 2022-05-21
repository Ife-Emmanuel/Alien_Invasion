import pygame.font
from pygame.sprite import Group
from rocket import Rocket

class Scoreboard():
    """A class to report scoring information."""
    def __init__(self, a1_settings, screen, stats):
        """Initializes scorekeeping attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.a1_settings = a1_settings
        self.stats = stats

        # Font settings for scoring information.
        self.text_colour = (231, 12, 60)
        self.font = pygame.font.SysFont(None, 30)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_rockets()

    def prep_score(self):
        """Turn the score into a rendered image."""
        self.rounded_score = int(round(self.stats.score, -1))
        score_str = 'Score : ' +  '{:,}'.format(self.rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_colour, self.a1_settings.bg_colour)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = 'All Time Highest Score : ' + '{:,}'.format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_colour)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """To prepare the image of the current game level from its text."""
        self.str_level =  'Level : ' + str(self.stats.level)
        self.level_image = self.font.render(self.str_level, True, self.text_colour, self.a1_settings.bg_colour)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_rockets(self):
        """Show how many rockets are left"""
        self.rockets = Group()
        for rocket_number in range(self.stats.rocket_left):
            image_path = self.a1_settings.image_path
            rocket_left_text = 'Rocket left'
            self.rocket_text_image = self.font.render(rocket_left_text, True, (230, 0, 0))
            self.rocket_text_image_rect = self.rocket_text_image.get_rect()
            rocket_speed_factor = self.a1_settings.rocket_speed_factor
            rocket = Rocket(image_path, self.screen, rocket_speed_factor)
            rocket.rect.x = 10 + rocket_number * rocket.rect.width
            rocket.rect.y = 10
            self.rockets.add(rocket)

        def prep_level_response():
            """Asks player if he wants to continue to continue from previous level or starts from level 1"""
            self_question_str = 'Do you want to continue from level '



    def show_score(self):
        """Draw / Display rendered score_image to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.rockets.draw(self.screen)
        self.screen.blit(self.rocket_text_image, self.rocket_text_image_rect)
        self.screen.blit(self.level_image, self.level_rect) 