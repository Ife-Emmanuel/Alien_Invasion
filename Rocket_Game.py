"""To make a game that begins with a rocket at center that can be moved up, down, left or right. """
import pygame
import pygame
import rocket_game_functions as rgf
from rocket import Rocket
from rg_settings import Settings
from pygame.sprite import Group
from game_stats import GameStats
from buttons import Buttons
from scoreboard import Scoreboard


def run_game():
    # Creating a pygame window
    pygame.init()
    pygame.display.set_caption(' Alien Invasion '.center(28, 'Y'))
    #Create an instance to store game statistics.
    a1_settings = Settings()
    stats = GameStats(a1_settings)
    # Create an instance to store game statistics and create a scoreboard
    screen = pygame.display.set_mode((a1_settings.screen_width, a1_settings.screen_height))
    sb = Scoreboard(a1_settings, screen, stats)
    rocket_speed_factor = a1_settings.rocket_speed_factor
    rocket = Rocket(a1_settings.image_path, a1_settings.screen, rocket_speed_factor)
    bullets = Group()
    aliens = Group()
    #Create the fleet of aliens.
    rgf.create_fleet(a1_settings, screen, aliens, rocket)
    a1_settings.screen.fill(a1_settings.bg_colour)
    buttons = Buttons(a1_settings, screen, stats)
    RUNNING, PAUSE = 1, -1
    #Start the main loop for the game.
    state = RUNNING

    while True:
        #Event loop for checking out for events
        rgf.check_event(a1_settings, screen, rocket, aliens, bullets, stats, sb, buttons)
        if stats.game_active:
            #Updating positions of several game objects.
            #sb.prep_score()
            if state == RUNNING:
                rocket.update()
                rgf.bullet_update(a1_settings, screen, rocket, aliens, bullets, stats, sb)
                rgf.update_aliens(a1_settings, rocket, aliens, stats, screen, bullets, sb)

        #Update to the screen showing several objects at their different positions.
        rgf.update_changes_and_flip(a1_settings, screen, rocket, aliens, bullets, stats, sb, buttons, state)

run_game()