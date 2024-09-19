import pygame


class Shop:
    def __init__(self, screen, player, ingame, game):
        self.screen = screen
        self.player = player
        self.ingame = ingame
        self.game = game

        self.shop_sound = pygame.mixer.Sound('Sounds/shop.mp3')
        self.sound_played = False

        self.catching = pygame.mixer.Sound('Sounds/catching.mp3')
        self.nope = pygame.mixer.Sound('Sounds/nope.mp3')


        self.item_rects = []
        self.dragged_item = None
        self.dragged_item_offset = (0, 0)

        # Load the font using pygame.font.Font
        self.font = pygame.font.Font(self.game.font, 36)  # 36 is the font size

        self.coin = self.player.money
        self.bag = self.player.bag

        self.week_items = self.ingame.shop
        self.mouse_pos = pygame.mouse.get_pos()

        self.shop_bg = pygame.image.load('Sprites/shop_bg.png')

        # Load and scale the close button images
        self.close_button_img = pygame.image.load('Sprites/shop_close.png').convert_alpha()
        self.close_button_img = pygame.transform.scale(self.close_button_img, (75, 125))
        self.close_button_img_hover = pygame.image.load("Sprites/shop_close_hover.png").convert_alpha()
        self.close_button_img_hover = pygame.transform.scale(self.close_button_img_hover, (75, 125))
        self.close_button_img_rect = self.close_button_img.get_rect(topright=(1280 - 10, 10))  # Adjusted rect size

        # Load and scale the bag images
        self.bag_img = pygame.image.load('Sprites/bag.png').convert_alpha()
        self.bag_img = pygame.transform.scale(self.bag_img, (100, 100))
        self.bag_img_hover = pygame.image.load('Sprites/bag_hover.png').convert_alpha()
        self.bag_img_hover = pygame.transform.scale(self.bag_img_hover, (100, 100))
        self.bag_img_rect = self.bag_img.get_rect(bottomright=(1280 - 10, 720 - 10))  # Adjusted rect size

        # Load and scale the coin image
        self.coin_img = pygame.image.load('Sprites/coin.png').convert_alpha()
        self.coin_img = pygame.transform.scale(self.coin_img, (35, 35))
        self.coin_rect = self.coin_img.get_rect(
            topright=(self.close_button_img_rect.left - 50, 20))  # Adjusted rect size

        self.debug()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state = "pause_menu"

        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            self.check_hovered_item()

            # Update the position of the dragged item if there is one
            if self.dragged_item:
                self.dragged_item_offset = (event.pos[0] - self.dragged_item["rect"].x,
                                            event.pos[1] - self.dragged_item["rect"].y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.close_button_img_rect.collidepoint(event.pos):
                    self.play_shop_sound()
                    self.game.state = "in_game"

                # Start dragging an item if clicked
                for item, item_rect in self.item_rects:
                    if item_rect.collidepoint(event.pos):
                        self.dragged_item = {"item": item, "rect": item_rect}
                        self.dragged_item_offset = (event.pos[0] - item_rect.x, event.pos[1] - item_rect.y)
                        break  # Only drag one item at a time

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragged_item:
                # Check if the item is dropped on the bag
                if self.bag_img_rect.collidepoint(event.pos):
                    self.add_item_to_bag(self.dragged_item["item"])
                # Reset dragged item after drop
                self.dragged_item = None

    def draw(self):
        self.screen.blit(self.shop_bg, (0, 0))  # Draw the background
        self.draw_coin()
        self.draw_close_button()
        self.draw_bag()
        self.draw_items()

        # Draw the dragged item (if any)
        if self.dragged_item:
            item = self.dragged_item["item"]
            item_rect = self.dragged_item["rect"]
            item_position = (self.mouse_pos[0] - self.dragged_item_offset[0],
                             self.mouse_pos[1] - self.dragged_item_offset[1])
            self.screen.blit(item.image, item_position)

    def draw_items(self):
        x, y = 100, 200  # Starting position for the first item
        item_spacing = 120  # Space between items

        self.item_rects = []  # Reset item rects for fresh drawing

        for item in self.week_items:
            # Draw the item image
            self.screen.blit(item.image, (x, y))
            # Create a rect for this item and store it
            item_rect = item.image.get_rect(topleft=(x, y))
            self.item_rects.append((item, item_rect))  # Store the item and its rect together

    def draw_close_button(self):
        if self.close_button_img_rect.collidepoint(self.mouse_pos):
            self.screen.blit(self.close_button_img_hover, self.close_button_img_rect)
        else:
            self.screen.blit(self.close_button_img, self.close_button_img_rect)

    def draw_bag(self):
        if self.bag_img_rect.collidepoint(self.mouse_pos):
            self.screen.blit(self.bag_img_hover, self.bag_img_rect)
        else:
            self.screen.blit(self.bag_img, self.bag_img_rect)

    def draw_coin(self):
        self.screen.blit(self.coin_img, self.coin_rect.topleft)
        coin_value_text = self.font.render(f"= {self.coin}", True, (255, 255, 255))
        text_x = self.coin_rect.right +2
        text_y = self.coin_rect.y +8
        self.screen.blit(coin_value_text, (text_x, text_y))

    def check_hovered_item(self):
        mouse_pos = pygame.mouse.get_pos()

        for item, item_rect in self.item_rects:
            if item_rect.collidepoint(mouse_pos):
                self.display_item_info(item)

    def display_item_info(self, item):
        # Fetch item data
        name = item.name
        price = item.price
        description = item.description
        consommable = "Oui" if item.consommable else "Non"

        # Render text for each piece of information
        font = pygame.font.SysFont(None, 24)
        info_text = [
            font.render(f"Nom: {name}", True, (255, 255, 255)),
            font.render(f"Prix: {price}", True, (255, 255, 255)),
            font.render(f"Description: {description}", True, (255, 255, 255)),
            font.render(f"Consommable: {consommable}", True, (255, 255, 255)),
        ]

        # Display the information box near the mouse cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        info_box_x, info_box_y = mouse_x + 20, mouse_y  # Position info box near the mouse

        # Draw each line of the info box
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
        for item in self.week_items:
            print(f"Item ID: {item.item_id}, Name: {item.name}, Price: {item.price}, Description: {item.description}")
