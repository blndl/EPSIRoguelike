import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.start_game = False
        self.start_button_color = (170, 170, 170)
        self.start_button_hover_color = (100, 100, 100)
        self.start_button_rect = pygame.Rect(300, 200, 200, 50)
        self.font = pygame.font.Font(None, 36)

        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

        # Input box
        self.input_box_rect = pygame.Rect(300, 300, 200, 50)
        self.input_active = False
        self.input_text = ''
        self.input_color = (170, 170, 170)

    def handle_events(self, event):
        # Handle button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button_rect.collidepoint(event.pos):
                self.start_game = True
            if self.input_box_rect.collidepoint(event.pos):
                self.input_active = True
            else:
                self.input_active = False

        # Handle text input
        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode

            # Handle Ctrl+V
            if event.type == pygame.KEYDOWN and event.mod & pygame.KMOD_CTRL:
                if event.key == pygame.K_v:

                    clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                    if clipboard_text is not None:
                        clipboard_text = clipboard_text.decode("utf-8")  # Ensure it's decoded properly
                        print("Pasted from clipboard:", clipboard_text)
                        self.input_text += clipboard_text

    def draw(self):
        # Draw the start button
        mouse_pos = pygame.mouse.get_pos()
        if self.start_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.start_button_hover_color, self.start_button_rect)
        else:
            pygame.draw.rect(self.screen, self.start_button_color, self.start_button_rect)

        # Render the start button text
        button_text = self.font.render("Start Game", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=self.start_button_rect.center)
        self.screen.blit(button_text, button_text_rect)

        # Draw the input box
        pygame.draw.rect(self.screen, self.input_color, self.input_box_rect, 2)
        input_text_surface = self.font.render(self.input_text, True, (255, 255, 255))
        self.screen.blit(input_text_surface, (self.input_box_rect.x + 5, self.input_box_rect.y + 5))

        # Change input box color if active
        if self.input_active:
            self.input_color = (100, 100, 100)
        else:
            self.input_color = (170, 170, 170)
