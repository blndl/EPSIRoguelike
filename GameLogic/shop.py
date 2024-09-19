import pygame

class Shop:
    def __init__(self, screen, player, ingame, game):
        self.screen = screen
        self.player = player
        self.ingame = ingame
        self.game = game

        self.load_sounds()
        self.load_assets()

        self.item_rects = []
        self.dragged_item = None
        self.dragged_item_offset = (0, 0)

        self.font = pygame.font.Font(self.game.font, 36)
        self.coin = self.player.money
        self.bag = self.player.bag
        self.mouse_pos = pygame.mouse.get_pos()
        self.sound_played = False

        self.setup_rects()

        self.debug()

    def load_sounds(self):
        self.shop_sound = pygame.mixer.Sound('Sounds/shop.mp3')
        self.catching = pygame.mixer.Sound('Sounds/catching.mp3')
        self.nope = pygame.mixer.Sound('Sounds/nope.mp3')

    def load_assets(self):
        self.shop_bg = pygame.image.load('Sprites/shop_bg.png')
        self.close_button_img = self.load_and_scale_image('Sprites/shop_close.png', (75, 125))
        self.close_button_img_hover = self.load_and_scale_image('Sprites/shop_close_hover.png', (75, 125))
        self.bag_img = self.load_and_scale_image('Sprites/bag.png', (100, 100))
        self.bag_img_hover = self.load_and_scale_image('Sprites/bag_hover.png', (100, 100))
        self.coin_img = self.load_and_scale_image('Sprites/coin.png', (35, 35))

    def load_and_scale_image(self, path, size):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)

    def setup_rects(self):
        self.close_button_img_rect = self.close_button_img.get_rect(topright=(1280 - 10, 10))
        self.bag_img_rect = self.bag_img.get_rect(bottomright=(1280 - 10, 720 - 10))
        self.coin_rect = self.coin_img.get_rect(topright=(self.close_button_img_rect.left - 50, 20))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state = "pause_menu"

        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            self.check_hovered_item()

            if self.dragged_item:
                self.dragged_item_offset = (event.pos[0] - self.dragged_item["rect"].x,
                                            event.pos[1] - self.dragged_item["rect"].y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.handle_click(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_button_up(event.pos)

    def handle_click(self, pos):
        if self.close_button_img_rect.collidepoint(pos):
            self.play_shop_sound()
            self.game.state = "in_game"

        for item, item_rect in self.item_rects:
            if item_rect.collidepoint(pos):
                self.dragged_item = {"item": item, "rect": item_rect}
                self.dragged_item_offset = (pos[0] - item_rect.x, pos[1] - item_rect.y)
                break

    def handle_mouse_button_up(self, pos):
        if self.dragged_item:
            if self.bag_img_rect.collidepoint(pos):
                self.add_item_to_bag(self.dragged_item["item"])
            self.dragged_item = None

    def draw(self):
        self.screen.blit(self.shop_bg, (0, 0))
        self.draw_coin()
        self.draw_close_button()
        self.draw_bag()
        self.draw_items()

        if self.dragged_item:
            item = self.dragged_item["item"]
            item_image = pygame.image.load(item.sprite_path).convert_alpha()  # Load the image here
            item_position = (self.mouse_pos[0] - self.dragged_item_offset[0],
                             self.mouse_pos[1] - self.dragged_item_offset[1])
            self.screen.blit(item_image, item_position)  # Blit the loaded surface, not the string

    def draw_items(self):
        x, y = 100, 200

        self.item_rects = []

        for item in self.ingame.shop:
            item_image = pygame.image.load(item.sprite_path).convert_alpha()  # Load the image here
            self.screen.blit(item_image, (x, y))
            x += 100

            item_rect = item_image.get_rect(topleft=(x, y))
            self.item_rects.append((item, item_rect))

    def draw_close_button(self):
        img = self.close_button_img_hover if self.close_button_img_rect.collidepoint(self.mouse_pos) else self.close_button_img
        self.screen.blit(img, self.close_button_img_rect)

    def draw_bag(self):
        img = self.bag_img_hover if self.bag_img_rect.collidepoint(self.mouse_pos) else self.bag_img
        self.screen.blit(img, self.bag_img_rect)

    def draw_coin(self):
        self.screen.blit(self.coin_img, self.coin_rect.topleft)
        coin_value_text = self.font.render(f"= {self.coin}", True, (255, 255, 255))
        text_x = self.coin_rect.right + 2
        text_y = self.coin_rect.y + 8
        self.screen.blit(coin_value_text, (text_x, text_y))

    def check_hovered_item(self):
        for item, item_rect in self.item_rects:
            if item_rect.collidepoint(self.mouse_pos):
                self.display_item_info(item)

    def display_item_info(self, item):
        info_text = [
            self.font.render(f"Nom: {item.name}", True, (255, 255, 255)),
            self.font.render(f"Prix: {item.price}", True, (255, 255, 255)),
            self.font.render(f"Description: {item.description}", True, (255, 255, 255)),
            self.font.render(f"Consommable: {'Oui' if item.consommable else 'Non'}", True, (255, 255, 255)),
        ]

        mouse_x, mouse_y = self.mouse_pos
        info_box_x, info_box_y = mouse_x + 20, mouse_y

        for i, text_surface in enumerate(info_text):
            self.screen.blit(text_surface, (info_box_x, info_box_y + i * 25))

    def add_item_to_bag(self, item):
        if self.player.money >= item.price:
            self.player.money -= item.price
            if len(self.player.bag) < 32:
                self.player.bag.append(item.item_id)
                self.catching.play()
            else:
                self.nope.play()

    def play_shop_sound(self):
        self.shop_sound.play()

    def debug(self):
        for item in self.ingame.shop:
            print(f"Item ID: {item.item_id}, Name: {item.name}, Price: {item.price}, Description: {item.description}")
