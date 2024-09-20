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
        self.mouse_pos = pygame.mouse.get_pos()
        self.sound_played = False

        self.setup_rects()

        self.debug()

    def load_sounds(self):
        self.shop_sound = pygame.mixer.Sound('Data/Sounds/shop.mp3')
        self.catching = pygame.mixer.Sound('Data/Sounds/catching.mp3')
        self.nope = pygame.mixer.Sound('Data/Sounds/nope.mp3')

    def load_assets(self):
        self.shop_bg = pygame.image.load('Data/Sprites/shopin.png')
        self.close_button_img = self.load_and_scale_image('Data/Sprites/shop_close.png', (75, 125))
        self.close_button_img_hover = self.load_and_scale_image('Data/Sprites/shop_close_hover.png', (75, 125))
        self.bag_img = self.load_and_scale_image('Data/Sprites/bag.png', (100, 100))
        self.bag_img_hover = self.load_and_scale_image('Data/Sprites/bag_hover.png', (100, 100))
        self.coin_img = self.load_and_scale_image('Data/Sprites/coin.png', (35, 35))

    def load_and_scale_image(self, path, size):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)

    def setup_rects(self):
        self.close_button_img_rect = self.close_button_img.get_rect(topright=(1280 - 10, 10))
        self.bag_img_rect = self.bag_img.get_rect(bottomright=(1280 - 10, 720 - 10))
        self.coin_rect = self.coin_img.get_rect(topright=(self.close_button_img_rect.left - 80, 20))

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
                # Set up the dragged item with the item and its rect
                self.dragged_item = {
                    "item": item,
                    "rect": item_rect,
                    "offset": (pos[0] - item_rect.x, pos[1] - item_rect.y)
                }
                break

    def handle_mouse_button_up(self, pos):
        if self.dragged_item:
            # Check if the dragged item is dropped on the bag
            if self.bag_img_rect.collidepoint(pos):
                self.add_item_to_bag(self.dragged_item["item"])
            # Reset the dragged item after dropping
            self.dragged_item = None

    def draw(self):
        self.screen.blit(self.shop_bg, (0, 0))
        self.draw_coin()
        self.draw_close_button()
        self.draw_bag()
        self.draw_items()

        if self.dragged_item:
            item = self.dragged_item["item"]
            item_image = pygame.image.load(item.sprite_path).convert_alpha()
            # Calculate the position to draw the image based on the mouse position and offset
            item_position = (self.mouse_pos[0] - self.dragged_item["offset"][0],
                             self.mouse_pos[1] - self.dragged_item["offset"][1])
            # Draw the image at the calculated position
            self.screen.blit(item_image, item_position)

    def draw_items(self):
        x, y = 100, 200
        self.item_rects = []

        for item in self.ingame.shop:
            # Skip drawing the item if it's currently being dragged
            if self.dragged_item and self.dragged_item["item"] == item:
                continue

            item_image = pygame.image.load(item.sprite_path).convert_alpha()
            item_rect = item_image.get_rect(topleft=(x, y))
            self.item_rects.append((item, item_rect))

            self.screen.blit(item_image, (x, y))
            x += 120  # Adjust the spacing as needed

            if x > self.screen.get_width() - 120:  # Move to the next row if needed
                x = 100
                y += 120

    def draw_close_button(self):
        img = self.close_button_img_hover if self.close_button_img_rect.collidepoint(self.mouse_pos) else self.close_button_img
        self.screen.blit(img, self.close_button_img_rect)

    def draw_bag(self):
        img = self.bag_img_hover if self.bag_img_rect.collidepoint(self.mouse_pos) else self.bag_img
        self.screen.blit(img, self.bag_img_rect)

    def draw_coin(self):
        self.screen.blit(self.coin_img, self.coin_rect.topleft)
        coin_value_text = self.font.render(f"= {self.player.money}", True, (255, 255, 255))
        text_x = self.coin_rect.right + 2
        text_y = self.coin_rect.y + 8
        self.screen.blit(coin_value_text, (text_x, text_y))

    def check_hovered_item(self):
        self.hovered_item = None

        for item, item_rect in self.item_rects:
            if item_rect.collidepoint(self.mouse_pos):
                self.hovered_item = item
                self.display_item_info(item)
                break

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
                self.ingame.shop.remove(item)  # Remove the item from the shop after purchase
                self.catching.play()
            else:
                self.nope.play()

    def play_shop_sound(self):
        self.shop_sound.play()

    def debug(self):
        for item in self.ingame.shop:
            print(f"Item ID: {item.item_id}, Name: {item.name}, Price: {item.price}, Description: {item.description}")
