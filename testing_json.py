import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep
from buttons import Buttons
import json

def store_data(data_name, data_value):
    """Uses json module to store the highest player score by dump method.
    data_name should be in string form."""
    with open(data_name + '.txt', 'w') as file_object:
        json.dump(data_value, file_object)


def get_data(data_name, data_value= 0):
    """Retrieves originally stored score. expected data should be a string."""
    try:       #r'highest_score'
        with open(data_name + '.txt') as file_object:
            data_value = json.load(file_object)
    except json.decoder.JSONDecodeError:
        store_data(data_name, data_value)
        return data_value
    except FileNotFoundError:
        store_data(data_name, data_value)
        return data_value
    else:
        return data_value



def bullet_firing(a1_settings, screen, rocket, bullets):
    """Fire a bullet if limit not reached yet."""
    new_bullet = Bullet(a1_settings, screen, rocket)
    bullets.add(new_bullet)


def start_game(stats, aliens, bullets, a1_settings, screen, rocket, sb):
    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)
    # Reset the game statistics.
    stats.reset_stats()
    #a1_settings.initialize_dynamic_settings()
    stats.game_active = True

    # Reset the scoreboard images
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_rockets()

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the rocket.
    create_fleet(a1_settings, screen, aliens, rocket)
    rocket.center_rocket()


def check_key_down_event(event, a1_settings, screen, rocket, bullets, stats, aliens, sb):
    """for press_down keys events."""
    if event.key == pygame.K_LEFT:
        rocket.moving_left = True
    elif event.key == pygame.K_RIGHT:
        rocket.moving_right = True
    elif event.key == pygame.K_SPACE:
        if len(bullets) < a1_settings.bullets_allowed:
            bullet_firing(a1_settings, screen, rocket, bullets)
    elif event.key == pygame.K_p:
        if not stats.game_active:
            start_game(stats, aliens, bullets, a1_settings, screen, rocket, sb)

    elif event.key == pygame.K_q:
        sys.exit()

    # elif event.key == pygame.K_UP:
    #     rocket.moving_up = True
    # elif event.key == pygame.K_DOWN:
    #     rocket.moving_down = True


def check_key_up_event(event, rocket):
    """for keys up events"""
    if event.key == pygame.K_LEFT:
        rocket.moving_left = False
    elif event.key == pygame.K_RIGHT:
        rocket.moving_right = False

def check_play_button(a1_settings, screen, stats, buttons, mouse_x, mouse_y, rocket, aliens, bullets, sb):
    """Start a new game when the player clicks Play."""
    button_clicked = buttons.play_image_rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        start_game(stats, aliens, bullets, a1_settings, screen, rocket, sb)

def check_yes_or_no_button(a1_settings, screen, stats, buttons, mouse_x, mouse_y, rocket, aliens, bullets, sb):
    """Checks if pos detected by mouse collides with yes button's position."""
    yes_button_clicked = buttons.yes_image_rect.collidepoint(mouse_x, mouse_y)
    no_button_clicked = buttons.no_image_rect.collidepoint(mouse_x, mouse_y)
    if yes_button_clicked:
        pass
    elif no_button_clicked:
        a1_settings.initialize_dynamic_settings()




def check_event(a1_settings, screen, rocket, aliens, bullets, stats,sb, buttons):
    """Checking for different categories and event_types."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down_event(event, a1_settings, screen, rocket, bullets, stats, aliens, sb)
        elif event.type == pygame.KEYUP:
            check_key_up_event(event, rocket)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(a1_settings, screen, stats, buttons, mouse_x, mouse_y, rocket, aliens, bullets, sb)


def update_changes_and_flip(a1_setting, screen, rocket, aliens, bullets, stats,  sb, buttons, state):
    screen.fill(a1_setting.bg_colour)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    rocket.blitme()
    aliens.draw(screen)
    # Draw the score information.
    sb.show_score()
    #Draw the play button if the game is inactive.
    if not stats.game_active:
        stats.reset_stats()
        buttons.draw_buttons()
    if stats.game_active and state == 1:
        buttons.draw_during_bottons()
    if stats.game_active and state == 0:
        buttons.draw_during_offbuttons()


    # if stats.game_active:
    #     pause_button.prep_other_msg(msg)
    #     pause_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def bullet_update(a1_settings, screen, rocket, aliens, bullets, stats, sb):
    """Update position of bullet and get rid of old bullets."""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(a1_settings, screen, rocket, aliens, bullets, stats, sb)

def check_bullet_alien_collisions(a1_settings, screen, rocket, aliens, bullets, stats, sb):
    """Respond to bullet - alien collisions."""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += a1_settings.alien_points * len(aliens)
            store_data('score', stats.score)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        #Destroy existing bullets and create more aliens
        bullets.empty()
        a1_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()
        create_fleet(a1_settings, screen, aliens, rocket)



def get_number_aliens_x(a1_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space = a1_settings.screen_width - 2 * alien_width
    number_of_aliens = int(available_space / (2 * alien_width))
    return number_of_aliens


def number_of_rows(a1_settings, alien, rocket):
    """To determine the numbers of possible rows you can have on a screen at once."""
    possible_vertical_space = a1_settings.screen_height - rocket.rect.height - 3 * alien.rect.height
    number_rows = possible_vertical_space // (2 * alien.rect.height)
    return number_rows


def create_alien(a1_settings, screen, alien_number, number, rocket):
    """Create an alien and fit in a row."""
    alien = Alien(a1_settings, screen)
    alien_width = alien.rect.width
    row_numbers = number_of_rows(a1_settings, alien, rocket)
    alien.y =  2 * alien.rect.height * number # -  1.3 * alien.rect.height * row_numbers
    alien.rect.y = alien.y
    alien.x = alien_width + 2 * alien_number * alien_width
    alien.rect.x = alien.x
    return alien


def create_fleet(a1_settings, screen, aliens, rocket):
    """Create a full fleet of aliens."""
    alien = Alien(a1_settings, screen)
    number_aliens_x = get_number_aliens_x(a1_settings, alien.rect.width)
    row_numbers = int(number_of_rows(a1_settings, alien, rocket))
    for number in range(row_numbers):
        for alien_number in range(number_aliens_x):
            alien = create_alien(a1_settings, screen, alien_number, number, rocket)
            aliens.add(alien)


def check_fleet_edges(a1_settings, aliens):
    """Respond appropriately if any alien have reached the edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(a1_settings, aliens)


def change_fleet_direction(a1_settings, aliens):
    """Make alien drop vertically downwards and later move sideways
     in opposite direction again."""
    for alien in aliens.sprites():
        alien.rect.y += a1_settings.fleet_drop_speed
    a1_settings.fleet_direction *= -1


def update_aliens(a1_settings, rocket, aliens, stats, screen, bullets, sb):
    """Check if the fleet is at the edge, and then update the
    positions of all the aliens in the fleet."""
    check_fleet_edges(a1_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(rocket, aliens):
        rocket_hit(a1_settings, stats, screen, rocket, aliens, bullets, sb)
    # Look for alien hitting the bottom of the screen.
    check_aliens_bottom(a1_settings, stats, screen, rocket, aliens, bullets, sb)


def rocket_hit(a1_settings, stats, screen, rocket, aliens, bullets, sb):
    """Respond to ship being hit by alien."""
    if stats.rocket_left > 0:
        # Decrement ships_left.
        stats.rocket_left -= 1

        #Update scoreboard.
        sb.prep_rockets()

        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #Create a new fleet and center the ship.
        rocket.center_rocket()
        create_fleet(a1_settings, screen, aliens, rocket)

        #pause
        sleep(1.5)
    else:
        stats.reset_stats()
        stats.game_active = False

def check_aliens_bottom(a1_settings, stats, screen, rocket, aliens, bullets, sb):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treating this the same as if the rocket got hit.
            rocket_hit(a1_settings, stats, screen, rocket, aliens, bullets, sb)
            break


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        store_data('highest_score', stats.high_score)
        sb.prep_high_score()
#
# def control_response_to_questions:
#




# def aliens_update(aliens, a1_settings):
#     """updating the position of aliens."""
#     aliens.update()
#     for alien in aliens.copy():
#         if alien.rect.top >= a1_settings.screen_rect.bottom:
#             aliens.remove(alien)