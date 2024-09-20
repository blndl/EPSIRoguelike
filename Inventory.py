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
        self.inv_bg_img = pygame.image.load(os.path.join(self.game.base_dir, "Data/Sprites/inv_bg.png")).convert_alpha()

        # Load buttons
        self.close_button_img = pygame.image.load(os.path.join(self.game.base_dir, "Data/Sprites/close_button.png")).convert_alpha()
        self.close_button_rect = self.close_button_img.get_rect(topleft=(1150, 50))

        self.trash_img = pygame.image.load(os.path.join(self.game.base_dir, "Data/Sprites/trash.png")).convert_alpha()
        self.trash_hover_img = pygame.image.load(os.path.join(self.game.base_dir, "Data/Sprites/trash_hover.png")).convert_alpha()
        self.trash_rect = self.trash_img.get_rect(bottomleft=(1135, 700))

        self.inventory_slot_rects = [
            pygame.Rect(415, 565, 100, 100),  # Slot 1
            pygame.Rect(530, 565, 100, 100),  # Slot 2
            pygame.Rect(640, 565, 100, 100),  # Slot 3
            pygame.Rect(750, 565, 100, 100)   # Slot 4
        ]

        # Load item data from JSON file
        with open(os.path.join(self.game.base_dir, "Data/Items/items.json"), "r") as file:
            self.item_data = json.load(file)["items"]  # Load the 'items' dictionary

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.state = "pause_menu"

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the left mouse button is clicked for dragging or other actions
            if event.button == 1:
                self.handle_click(event.pos)

            # Right-click to use an item
            elif event.button == 3:
                for index, item_id in enumerate(self.player.bag):
                    item_info = self.item_data.get(item_id)
                    if item_info:
                        item_rect = self.get_item_rect(index)
                        if item_rect.collidepoint(event.pos):
                            # Check if the item is consumable and use it
                            if item_info.get("consommable", False):
                                self.use_item(index)
                                break

        elif event.type == pygame.MOUSEBUTTONUP:
            # Handle logic for dropping the dragged item
            if self.dragged_item:
                # If dropped on trash, delete the item
                if self.trash_rect.collidepoint(event.pos):
                    if self.dragged_item["from"] == "bag":
                        del self.player.bag[self.dragged_item["index"]]
                    elif self.dragged_item["from"] == "inventory":
                        setattr(self.player, f'inventory_slot_{self.dragged_item["index"] + 1}', None)
                    self.dragged_item = None  # Reset dragged item
                    return

                # Check if the dragged item is dropped into one of the inventory slots
                if self.dragged_item["from"] == "bag":
                    for i, slot_rect in enumerate(self.inventory_slot_rects):
                        if slot_rect.collidepoint(event.pos):
                            current_slot_item = getattr(self.player, f'inventory_slot_{i + 1}')
                            item_info = self.item_data.get(self.dragged_item['id'])

                            # Check if the item is consumable, prevent equipping
                            if item_info and item_info.get("consommable", False):
                                print("This item is consumable and cannot be equipped.")
                                self.dragged_item = None
                                return

                            # If the slot is empty, place the dragged item in the slot
                            if current_slot_item is None:
                                setattr(self.player, f'inventory_slot_{i + 1}', self.dragged_item['id'])
                                del self.player.bag[self.dragged_item['index']]
                                self.dragged_item = None
                                return
                            else:
                                # Swap the current slot item with the dragged item
                                old_item_id = current_slot_item
                                setattr(self.player, f'inventory_slot_{i + 1}', self.dragged_item['id'])
                                # Remove dragged item from bag, add old item to bag
                                del self.player.bag[self.dragged_item['index']]
                                self.player.bag.append(old_item_id)
                                self.dragged_item = None
                                return

                # If the dragged item is from the inventory and dropped back into the bag
                if self.dragged_item["from"] == "inventory":
                    # Add the item back to the bag and clear the inventory slot
                    self.player.bag.append(self.dragged_item["id"])
                    setattr(self.player, f'inventory_slot_{self.dragged_item["index"] + 1}', None)
                    self.dragged_item = None  # Reset dragged item

            # Reset dragged item after drop
            self.dragged_item = None

    def handle_click(self, pos):
        if self.close_button_rect.collidepoint(pos):
            self.game.state = "in_game"

        # Check if an item in the bag is clicked for dragging
        for index, item_id in enumerate(self.player.bag):
            item_info = self.item_data.get(item_id)
            if item_info:
                item_rect = self.get_item_rect(index)
                if item_rect.collidepoint(pos):
                    # Setup the dragged item similar to shop.py
                    self.dragged_item = {
                        "id": item_id,
                        "index": index,
                        "rect": item_rect,
                        "offset": (pos[0] - item_rect.x, pos[1] - item_rect.y),
                        "from": "bag"
                    }
                    break  # Only drag one item at a time

        # Check if an item in the inventory slot is clicked for dragging
        for i, slot_rect in enumerate(self.inventory_slot_rects):
            current_slot_item = getattr(self.player, f'inventory_slot_{i + 1}')
            if current_slot_item:
                if slot_rect.collidepoint(pos):
                    # Setup the dragged item similar to shop.py
                    self.dragged_item = {
                        "id": current_slot_item,
                        "index": i,
                        "rect": slot_rect,
                        "offset": (pos[0] - slot_rect.x, pos[1] - slot_rect.y),
                        "from": "inventory"
                    }
                    break  # Only drag one item at a time

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

        # Draw items in the inventory slots
        self.draw_inventory_slots()

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

    def draw_inventory_slots(self):
        # Check and draw items in each inventory slot
        inventory_slots = [self.player.inventory_slot_1, self.player.inventory_slot_2,
                           self.player.inventory_slot_3, self.player.inventory_slot_4]

        for i, slot_item_id in enumerate(inventory_slots):
            if slot_item_id:
                item_info = self.item_data.get(slot_item_id)
                if item_info:
                    # Load and scale the item image
                    item_img = pygame.image.load(os.path.join(self.game.base_dir, item_info["image"])).convert_alpha()
                    item_img_scaled = pygame.transform.scale(item_img, (60, 60))

                    # Get the rect for the slot
                    slot_rect = self.inventory_slot_rects[i]

                    # Get the rect for the scaled image and center it inside the slot
                    item_rect = item_img_scaled.get_rect(center=slot_rect.center)

                    # Draw the item in the centered position
                    self.screen.blit(item_img_scaled, item_rect.topleft)

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
        spacing = 50  # Space between each item
        row_spacing = 2  # Space between rows
        items_per_row = 8  # Number of items to display per row
        start_x = 210  # Starting X position for items
        start_y = 60  # Starting Y position for items

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
        close_button_scaled = pygame.transform.scale(self.close_button_img, (75, 75))
        self.screen.blit(close_button_scaled, self.close_button_rect.topleft)

    def draw_trash_button(self):
        mouse_pos = pygame.mouse.get_pos()
        trash_scaled = pygame.transform.scale(self.trash_img, (100, 125))
        trash_hover_scaled = pygame.transform.scale(self.trash_hover_img, (100, 125))

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

            del self.player.bag[index]
