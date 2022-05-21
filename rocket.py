import pygame
from pygame.sprite import Sprite
class Rocket(Sprite):
    def __init__(self, image_path, screen, rocket_speed_factor):
        super(Rocket, self).__init__()
        self.image = pygame.image.load(image_path)
        self.screen = screen
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        #self.rect.centery = self.screen_rect.bottom - self.rect.height

        #initialize movement in all four corner directions
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.speed_factor = rocket_speed_factor
        self.center = float(self.rect.centerx)

    def update(self):
        """Updating rect object values for different types of events detected. """
        if self.moving_right and self.rect.right <= self.screen_rect.right:
            self.center += self.speed_factor
        if self.moving_left and self.rect.left >= self.screen_rect.left:
            self.center -= self.speed_factor
        self.rect.centerx = self.center

        # if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
        #     self.rect.centery += self.speed_factor
        # if self.moving_up and self.rect.top >= self.screen_rect.top:
        #     self.rect.centery -= self.speed_factor

    def center_rocket(self):
        """Center the rocket on the screen."""
        self.rect.center = self.screen_rect.midbottom


    def blitme(self):
        """Draws the rocket at the current rect values."""
        self.screen.blit(self.image, self.rect)