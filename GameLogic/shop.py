import pygame


class Shop:
    def __init__(self, screen, player, ingame, game):
        self.screen = screen
        self.player = player
        self.ingame = ingame
        self.game = game
        self.font = self.game.font

        self.coin = self.player.money
        self.bag = self.player.bag

        self.week_items = self.ingame.shop
        self.mouse_pos = pygame.mouse.get_pos()

        self.shop_bg = pygame.image.load('Sprites/shop_bg.png')

        self.close_button_img = pygame.image.load('Sprites/shop_close.png').convert_alpha()
        self.close_button_img_hover = pygame.image.load("Sprites/shop_close_hover.png").convert_alpha()
        self.close_button_img_rect = self.close_button_img_hover.get_rect(botttomright=(150, 150))

        self.bag_img = pygame.image.load('Sprites/bag.png').convert_alpha()
        self.bag_img_hover = pygame.image.load('Sprites/bag_hover.png').convert_alpha()
        self.bag_img_rect = self.bag_img_hover.get_rect(topleft=(150, 150))

        self.coin_img = pygame.image.load('Sprites/coin.png').convert_alpha()
        self.coin_rect = self.coin_img.get_rect(topleft=(150, 150))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.close_button_img_rect.collidepoint(event.pos):
                    self.game.state = "in_game"

    def draw(self):
        self.screen.blit(self.shop_bg, (0, 0))  # Draw the background
        self.draw_coin()
        self.draw_close_button()
        self.draw_bag()
        self.draw_items()

    def draw_items(self):
        pass

    def draw_close_button(self):
        close = pygame.transform.scale(self.close_button_img, (50, 50))
        close_hover = pygame.transform.scale(self.close_button_img_hover, (50, 50))

        if self.close_button_img_rect.collidepoint(self.mouse_pos):
            self.screen.blit(close_hover, self.close_button_img_rect)
        else:
            self.screen.blit(close, self.close_button_img_rect)

    def draw_bag(self):
        bag = pygame.transform.scale(self.bag_img, (50, 50))
        bag_hover = pygame.transform.scale(self.bag_img_hover, (50, 50))

        if self.bag_img_rect.collidepoint(self.mouse_pos):
            self.screen.blit(bag_hover, self.bag_img_rect)
        else:
            self.screen.blit(bag, self.bag_img_rect)

    def draw_coin(self):
        self.screen.blit(self.coin_img, self.coin_rect.topleft)
        coin_value_text = self.font.render(f"= {self.coin}", True, (255, 255, 255))
        text_x = self.coin_rect.right + 10
        text_y = self.coin_rect.y
        self.screen.blit(coin_value_text, (text_x, text_y))
