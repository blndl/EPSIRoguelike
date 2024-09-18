import pygame
import json
import os


class Inventory:
    def __init__(self, game, screen, player):
        self.screen = screen
        self.player = player
        self.game = game
        self.dragged_item = None  # To store the currently dragged item
        self.dragged_item_offset = (0, 0)  # Offset to ensure smooth dragging
        self.hovered_item_index = None  # Track the index of the hovered item

        # Load the background image
        self.inv_bg_img = pygame.image.load(os.path.join(self.game.base_dir, "Sprites/inventory.jpg")).convert_alpha()

        # Load buttons
        self.close_button_img = pygame.image.load(os.path.join(self.game.base_dir, "Sprites/close_button.png")).convert_alpha()
        self.close_button_rect = self.close_button_img.get_rect(topleft=(1200, 50))

        self.trash_img = pygame.image.load(os.path.join(self.game.base_dir, "Sprites/trash.png")).convert_alpha()
        self.trash_hover_img = pygame.image.load(os.path.join(self.game.base_dir, "Sprites/trash_hover.png")).convert_alpha()
        self.trash_rect = self.trash_img.get_rect(bottomleft=(1200, 600))

        # Load item data from JSON file
        with open(os.path.join(self.game.base_dir, "Items/items.json"), "r") as file:
            self.item_data = json.load(file)["items"]  # Load the 'items' dictionary

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the left mouse button is clicked for dragging
            if event.button == 1:
                # Close button check
                if self.close_button_rect.collidepoint(event.pos):
                    self.game.state = "ingame"

                # Check if an item is clicked for dragging
                for index, item_id in enumerate(self.player.bag):
                    item_info = self.item_data.get(item_id)
                    if item_info:
                        item_rect = self.get_item_rect(index)
                        if item_rect.collidepoint(event.pos):
                            self.dragged_item = {"id": item_id, "index": index, "rect": item_rect}
                            self.dragged_item_offset = (event.pos[0] - item_rect.x, event.pos[1] - item_rect.y)

            # Check if the right mouse button is clicked for consuming an item
            elif event.button == 3:
                for index, item_id in enumerate(self.player.bag):
                    item_info = self.item_data.get(item_id)
                    if item_info:
                        item_rect = self.get_item_rect(index)
                        if item_rect.collidepoint(event.pos):
                            # Use the item if right-clicked
                            if item_info and item_info["consommable"]:
                                self.use_item(index)

        elif event.type == pygame.MOUSEBUTTONUP:
            # Handle item dropping (left-click drag and drop logic)
            if self.dragged_item:
                if self.trash_rect.collidepoint(event.pos):
                    del self.player.bag[self.dragged_item["index"]]
                self.dragged_item = None  # Reset dragged item

    def draw_inventory(self):
        # Blit the loaded background image
        self.load_and_scale_bg_img()

        # Draw close button and trash button
        self.draw_close_button()
        self.draw_trash_button()

        # Draw each item in the player's bag, except the one being dragged
        for index, item_id in enumerate(self.player.bag):
            if not self.dragged_item or self.dragged_item["index"] != index:
                self.draw_item(index, item_id)

        # Check for hovered item and display info
        self.check_hovered_item()

        # Draw the dragged item (if any)
        if self.dragged_item:
            item_info = self.item_data.get(self.dragged_item["id"])
            if item_info:
                item_img = pygame.image.load(os.path.join(self.game.base_dir, item_info["image"])).convert_alpha()
                item_img_scaled = pygame.transform.scale(item_img, (60, 60))
                # Follow the mouse position while dragging
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.screen.blit(item_img_scaled,
                                 (mouse_x - self.dragged_item_offset[0], mouse_y - self.dragged_item_offset[1]))

    def draw_item(self, index, item_id):
        item_info = self.item_data.get(item_id)
        if item_info:
            # Load and scale the item image
            item_img = pygame.image.load(os.path.join(self.game.base_dir, item_info["image"])).convert_alpha()
            item_img_scaled = pygame.transform.scale(item_img, (60, 60))

            # Calculate position for the item
            item_rect = self.get_item_rect(index)

            # Blit the item image onto the screen at the calculated position
            self.screen.blit(item_img_scaled, item_rect.topleft)

    def get_item_rect(self, index):
        # Define item display parameters (reuse logic from draw_items)
        item_width = 60  # Width of each item image after scaling
        item_height = 60  # Height of each item image after scaling
        spacing = 60  # Space between each item
        row_spacing = -7  # Space between rows
        items_per_row = 8  # Number of items to display per row
        start_x = 200  # Starting X position for items
        start_y = 170  # Starting Y position for items

        # Calculate position for the item
        row = index // items_per_row
        col = index % items_per_row
        x = start_x + col * (item_width + spacing)
        y = start_y + row * (item_height + row_spacing + spacing)

        # Return a pygame.Rect for the item's position
        return pygame.Rect(x, y, item_width, item_height)

    def check_hovered_item(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_item_index = None

        # Check if the mouse is hovering over any item
        for index, item_id in enumerate(self.player.bag):
            item_rect = self.get_item_rect(index)
            if item_rect.collidepoint(mouse_pos):
                self.hovered_item_index = index
                self.display_item_info(index)
                break  # Only show one item info at a time

    def display_item_info(self, index):
        # Fetch item data
        item_id = self.player.bag[index]
        item_info = self.item_data.get(item_id)
        if item_info:
            # Display information about the hovered item
            name = item_info["name"]
            price = item_info["price"]
            description = item_info["description"]
            consommable = "Oui" if item_info["consommable"] else "Non"

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

    def load_and_scale_bg_img(self):
        img = pygame.transform.scale(self.inv_bg_img, (1280, 720))
        self.screen.blit(img, (0, 0))

    def draw_close_button(self):
        close_button_scaled = pygame.transform.scale(self.close_button_img, (50, 50))
        self.screen.blit(close_button_scaled, self.close_button_rect.topleft)

    def draw_trash_button(self):
        mouse_pos = pygame.mouse.get_pos()
        trash_scaled = pygame.transform.scale(self.trash_img, (50, 75))
        trash_hover_scaled = pygame.transform.scale(self.trash_hover_img, (50, 75))

        if self.trash_rect.collidepoint(mouse_pos):
            self.screen.blit(trash_hover_scaled, self.trash_rect.topleft)
        else:
            self.screen.blit(trash_scaled, self.trash_rect.topleft)

    def use_item(self, index):
        item_id = self.player.bag[index]
        item_info = self.item_data.get(item_id)

        if item_info:
            if "sound" in item_info and item_info["sound"]:
                sound = pygame.mixer.Sound(item_info["sound"])
                sound.play()
                self.player.statchange(item_info['money'],item_info['moral'], item_info['energy'])

            del self.player.bag[index]

