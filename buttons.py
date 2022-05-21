import pygame

class Buttons():
    def __init__(self, a1_settings, screen, stats):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 200, 50
        # Set the dimensions and properties of the button.
        self.during_button_colour = (60, 60, 60)
        self.button_colour = (231, 12, 60)
        self.text_colour = (22, 255, 25)
        self.font = pygame.font.SysFont(None, 48)
        self.during_font = pygame.font.SysFont('Consolas', 15)
        self.during_colour = (255, 255, 255)
        self.stats = stats
        # self.font_path = r'‪C:\Users\User\Desktop\python\CS6\Fonts\AdobeFanHeitiStd-Bold.otf'
        # self.font = pygame.font.SysFont(self.font_path, 48)

        #Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # for attributes changing through passes of game loop
        self.initialize_dynamically_changing()

        # The button message needs to appear only once.
        self.prep_play()
        self.prep_question()
        self.prep_yes()
        self.prep_no()
        self.during_play()
        self.during_pause()

    def initialize_dynamically_changing(self):
        """for attributes that changes during pass through game loop"""
        self.play_button_clicked = 0
        self.yes_button_clicked = 0
        self.no_button_clicked = 0
        self.during_pause_button_clicked = 0

    def prep_play(self):
        msg = 'Play'
        self.play_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.play_image_rect = self.play_image.get_rect()
        self.play_image_rect.center = self.rect.center

    def prep_question(self):
        """Turn msg into a rendered image and center text on the button."""
        msg = 'Do you want to continue from level ' + str(self.stats.level) + '?'
        self.question_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.question_image_rect = self.question_image.get_rect()
        self.question_image_rect.center = self.rect.center
        self.question_image_rect.centery = self.play_image_rect.centery - 100

    def prep_yes(self):
        msg = 'yes'
        self.yes_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.yes_image_rect = self.yes_image.get_rect()
        self.yes_image_rect.centery = self.question_image_rect.centery + 30
        self.yes_image_rect.left = self.screen_rect.left + 100

    def prep_no(self):
        msg = 'no'
        self.no_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.no_image_rect = self.no_image.get_rect()
        self.no_image_rect.centery = self.question_image_rect.centery + 30
        self.no_image_rect.right = self.screen_rect.right - 100

    def during_play(self):
        msg = 'Play'
        self.during_play_image = self.during_font.render(msg, True, self.during_colour, self.during_button_colour)
        self.during_play_image_rect = self.during_play_image.get_rect()
        self.during_play_image_rect.topright = self.screen_rect.topright

    def during_pause(self):
        msg = 'Pause'
        self.during_pause_image = self.during_font.render(msg, True, self.during_colour, self.during_button_colour)
        self.during_pause_image_rect = self.during_play_image.get_rect()
        self.during_pause_image_rect.topright = self.screen_rect.topright
        self.during_pause_image_rect.right = self.screen_rect.right - 15

    def draw_during_bottons(self):
        """Draws buttons to the screen while game is still active and playing"""
        self.screen.blit(self.during_pause_image, self.during_pause_image_rect)

    def draw_during_offbuttons(self):
        """Draws buttons to the screen while game is active but paused"""
        self.screen.blit(self.during_play_image, self.during_play_image_rect)

    def draw_buttons(self):
        """Draws button to the screen."""
        #self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.play_image, self.play_image_rect)

    def draw_prompt_buttons(self):
        """Should be drawn after after play button has been clicked"""
        self.screen.blit(self.question_image, self.question_image_rect)
        self.screen.blit(self.yes_image, self.yes_image_rect)
        self.screen.blit(self.no_image, self.no_image_rect)