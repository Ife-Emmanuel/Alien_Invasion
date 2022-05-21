import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, a1_settings, screen):
        """Initialize the alien and sets its starting position."""
        super(Alien, self).__init__()
        self.screen = screen
        self.a1_settings = a1_settings
        #self.speed_factor_x = a1_settings.alien_speed_factor_x
        #self.speed_factor_y = a1_settings.alien_speed_factor_y

        #Load the alien image and set its rect attribute
        self.image = pygame.image.load(r'images/alien.bmp')
        self.rect = self.image.get_rect()

        #Start each new alien near the top of the screen.
        self.rect.x= self.rect.width
        self.rect.y = self.rect.height

        #Store the alien's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.nature = 1

    # def update(self):
    #     """Updating positions of stars."""
    #     if self.rect.y < self.a1_settings.screen_height:
    #         self.y += self.speed_factor_y
    #         self.rect.y = self.y
    #     if self.rect.x < self.a1_settings.screen_width:
    #         self.x += self.nature * self.speed_factor_x
    #         self.rect.x = self.x
    #     if self.rect.y % 100 == 0:
    #         self.nature *= -1

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += (self.a1_settings.alien_speed_factor * self.a1_settings.fleet_direction)
        self.rect.x = self.x