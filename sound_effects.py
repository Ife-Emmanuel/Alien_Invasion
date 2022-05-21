import pygame
pygame.mixer.init()

from decouple import config
bullet_sound = config('bullet_sound')
alien_sound = config('alien_sound')
start_sound = config('start_game_sound')
bullet_sound = pygame.mixer.Sound(bullet_sound)
alien_sound = pygame.mixer.Sound(alien_sound)

# bullet_sound = pygame.mixer.Sound('sounds/laser1.wav')
# alien_sound = pygame.mixer.Sound('sounds/laser8.wav')
def start_game_sound():
    """Gives some sound once the play button is pressed."""
    pygame.mixer.music.load(start_sound)
    pygame.mixer.music.play(-1)