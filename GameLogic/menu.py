import pygame


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.start_game = False
        self.start_button_color = (170, 170, 170)
        self.start_button_hover_color = (100, 100, 100)
        self.start_button_rect = pygame.Rect(490, 300, 300, 100)

        # Load fonts for the title and buttons
        self.title_font = pygame.font.Font("pixeboy.ttf", 96)  # Larger font for the title
        self.button_font = pygame.font.Font("pixeboy.ttf", 36)  # Smaller font for the button

        self.menu_bg_img = pygame.image.load("Sprites/epsi.jpg")

        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

    def handle_events(self, event):
        # Handle button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button_rect.collidepoint(event.pos):
                self.start_game = True

    def draw(self):
        self.draw_bg()

        # Draw the title text
        title_text = self.title_font.render("EPSImester", True, (255, 255, 255))  # White color for the title
        title_text_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(title_text, title_text_rect)

        # Draw the start button
        mouse_pos = pygame.mouse.get_pos()
        if self.start_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.start_button_hover_color, self.start_button_rect)
        else:
            pygame.draw.rect(self.screen, self.start_button_color, self.start_button_rect)

        # Render the start button text
        button_text = self.button_font.render("Start Game", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(button_text, button_text_rect)

    def draw_bg(self):
        bg_scale = pygame.transform.scale(self.menu_bg_img, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(bg_scale, (0, 0))  # (0, 0) is the top-left corner of the screen
