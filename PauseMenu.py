import pygame
class PauseMenu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

        # Track the previous state
        self.previous_state = self.game.state

        # Define button properties
        self.continue_button_rect = pygame.Rect(540, 300, 200, 50)  # (x, y, width, height)
        self.restart_button_rect = pygame.Rect(540, 400, 200, 50)  # (x, y, width, height)

        # Define button colors
        self.button_color = (100, 100, 100)
        self.button_hover_color = (150, 150, 150)
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_continue_button()
        self.draw_restart_button()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.continue_button_rect.collidepoint(event.pos):
                    self.game.state = self.previous_state  # Restore the previous state
                elif self.restart_button_rect.collidepoint(event.pos):
                    self.restart_game()  # Restart the game

    def draw_continue_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.continue_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.button_hover_color, self.continue_button_rect)
        else:
            pygame.draw.rect(self.screen, self.button_color, self.continue_button_rect)

        continue_text = self.font.render("Continue", True, (255, 255, 255))
        self.screen.blit(continue_text, self.continue_button_rect.center)

    def draw_restart_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.restart_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.button_hover_color, self.restart_button_rect)
        else:
            pygame.draw.rect(self.screen, self.button_color, self.restart_button_rect)

        restart_text = self.font.render("Restart", True, (255, 255, 255))
        self.screen.blit(restart_text, self.restart_button_rect.center)

    def restart_game(self):
        self.game.__init__()
        self.game.state = "menu"
