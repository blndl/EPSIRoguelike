import pygame
from Events.event_gestion import Event
from Items.item_gestion import Item

pygame.font.init()

# Define in-game states
class InGameState:
    EVENT_PROGRESS = 0
    PHASE_PROGRESS = 1
    CHOICE_MAKING = 2

# Main class for the in-game logic and rendering
class InGame:
    def __init__(self, screen, player, seed, game):
        # Data from the main game class
        self.screen = screen
        self.player = player
        self.seed = seed
        self.game = game  # Reference to the main Game class
        self.load_assets()

        # In-game state data and variables
        self.ingame_state = InGameState.EVENT_PROGRESS  # State of the game
        self.current_event = None
        self.current_advancement = 0
        self.events = Event.load_events("Events/events.json")  # Load the events
        self.items = Item.load_items("Items/items.json")  # Load the items
        self.shop = []
        self.week_event = None
        self.index = 0

        self.buttons_rects = []
        self.available = []
        self.not_available = []

        # Time data
        self.time = 0
        self.day = 0
        self.week = 0
        self.month = 0
        self.time_periods = {
            0: "Early-Morning",
            1: "Morning",
            2: "Lunch",
            3: "Afternoon",
            4: "Evening"
        }
        self.day_of_the_week = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

        # Debugging only
        print("Seed: ", self.seed)

    def game_over(self):
        print("Game Over")
        self.game.state = "game_over"

    def win(self):
        print('Score : ', self.player.score)
        print("YOU WIN !")

    def handle_time(self):
        print(f"Time: {self.time}, Day: {self.day}, Week: {self.week}, Month: {self.month}")
        print(f"Current time period: {self.time_periods[self.time]}")
        if self.time >= 4:
            self.time = 0
            self.day += 1
            if self.day >= 7:
                self.day = 0
                self.week += 1
                if self.player.project < self.player.max_project:
                    self.game_over()
                else:
                    self.player.score = self.player.score + self.player.project
                if self.week >= 4:
                    self.week = 0
                    self.month += 1
                    if self.index == len(self.seed):
                        self.win()
        else:
            self.time += 1

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                print("Inventory passed")
                print(self.game.state)
                self.game.state = "inventory"
                print(self.game.state)
            elif event.key == pygame.K_ESCAPE:
                self.game.state = "pause_menu"

        elif self.ingame_state == InGameState.EVENT_PROGRESS:
            self.advance_event()

        elif self.ingame_state == InGameState.PHASE_PROGRESS:
            self.advance_phases()
            self.ingame_state = InGameState.CHOICE_MAKING

        elif self.ingame_state == InGameState.CHOICE_MAKING:
            self.handle_choice_making(event)

    def advance_event(self):
        print("\nIndex : ", self.index)
        self.week_start()
        self.open_shop()
        self.get_event()
        self.handle_time()
        self.ingame_state = InGameState.PHASE_PROGRESS

    def week_start(self):
        if self.time == 0 and self.day == 0:
            self.week_event = None
            self.shop = []
            if self.seed[self.index] != "00":
                self.week_event = self.events[self.seed[self.index]]
                print("Week event changed !")
            for i in range(1, 3):
                if self.seed[self.index + i] != "00":
                    self.shop.append(self.items[self.seed[self.index + i]])
            self.index += 3
            print("increment index : ", self.index)

    def open_shop(self):
        if self.day == 2 and self.time == 2:
            print(self.time)
            self.game.state = "shop"

    def get_event(self, error=0):
        random_event = self.should_trigger_random_event()
        print("get event entered")
        if random_event:
            if self.seed[self.index] == "00":
                print("No random event")
                self.current_event = Event.get_event_by_is_choice_and_time(True, self.events, self.time_periods[self.time])
                print("From based event : ", self.current_event, "00 seed")
            else:
                seed = self.seed[self.index]
                print("Random event seed : ", seed)
                if seed in self.events.keys() and seed != "00":
                    self.current_event = self.events[seed]
                    print("Random event : ", self.current_event)
                    self.index += 1
                elif seed in self.items.keys() and seed != "00":
                    print("Random item")
                    item = self.items[seed]
                    self.inventory_adder(item)
                elif seed == "00":
                    print("No item")
                else:
                    print("SEED ERROR for item or item: ", seed)
                    error += 1
                    if error > 3:
                        raise SystemExit(f"Shutting down the program due to SEED ERROR : {seed}")
                    self.get_event(error)
            self.index += 1
            print("Incremented index : ", self.index)
        else:
            self.current_event = Event.get_event_by_is_choice_and_time(True, self.events, self.time_periods[self.time])
            print("From based event : ", self.current_event)

    def should_trigger_random_event(self):
        return self.time not in [0, 2, 4]

    def inventory_adder(self, item):
        if item.consommable:
            if len(self.player.bag) < 32:
                self.player.bag.append(item.item_id)
                print("Item added to the bag : ", item.item_id, " ", item.name)
                print("Bag: ", self.player.bag)
            else:
                print("Bag full")
                print("Item not added to the bag : ", item.item_id, " ", item.name)
        else:
            if self.player.inventory_slot_1 is None:
                self.player.inventory_slot_1 = item.item_id
                print("Item added to the inventory slot 1 : ", item.item_id, " ", item.name)
            elif self.player.inventory_slot_2 is None:
                self.player.inventory_slot_2 = item.item_id
                print("Item added to the inventory slot 2 : ", item.item_id, " ", item.name)
            elif self.player.inventory_slot_3 is None:
                self.player.inventory_slot_3 = item.item_id
                print("Item added to the inventory slot 3 : ", item.item_id, " ", item.name)
            elif self.player.inventory_slot_4 is None:
                self.player.inventory_slot_4 = item.item_id
                print("Item added to the inventory slot 4 : ", item.item_id, " ", item.name)
            else:
                print("Inventory full")
                print("Item not added to the inventory : ", item.item_id, "", item.name)

    def advance_phases(self):
        if self.current_event is None:
            print("No current event to advance phases.")
            return

        if self.current_advancement + 1 < len(self.current_event.phases):
            self.current_advancement += 1
        else:
            print(f"All phases completed for event {self.current_event.event_id}. Moving to next event.")

    def select_choice(self, choice_number):
        choices = self.current_event.phases_choices_data(self.current_advancement)
        choice = choices[choice_number]

        # Update the player's stats using the update_player method
        self.player.update_player(choice)

        print(
            f"Selected choice: {choice['description']}, money : {choice['money']}, energy : {choice['energy']}, moral : {choice['moral']}, project : {choice['project']}")

        if self.current_advancement + 1 < len(self.current_event.phases):
            self.advance_phases()
        else:
            self.advance_event()

        self.buttons_rects = []

    def handle_choice_making(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons_rects):
                if button.collidepoint(event.pos):
                    self.select_choice(i)
                    self.buttons_rects = []  # Clear buttons after choice

                    # Check if the event is finished
                    if self.current_advancement >= len(self.current_event.phases) - 1:
                        print(f"Event {self.current_event.event_id} complete.")
                        self.current_event = None  # Clear current event
                        self.current_advancement = 0  # Reset phase advancement
                        self.ingame_state = InGameState.EVENT_PROGRESS  # Go back to event progress state
                    else:
                        self.ingame_state = InGameState.PHASE_PROGRESS  # Continue to phase progress
                    break

    def check_available(self, choice):
        if choice['energy'] + self.player.energy < 0:
            return False
        elif choice['money'] + self.player.energy < 0:
            return False
        elif choice['moral'] + self.player.energy < 0:
            return False
        else:
            return True

    def draw(self):
        if self.ingame_state == InGameState.PHASE_PROGRESS:
            self.draw_current_phase()
            self.draw_coin()
            self.draw_bars()
            self.draw_day_time_bar()
            self.draw_project_bar()

    def draw_current_phase(self):
        if self.current_event:
            if not self.current_advancement >= len(self.current_event.phases):
                phase_data = self.current_event.phases_data()[self.current_advancement]
                phase_description = phase_data['description']
                phase_choices = phase_data['choices']
                phase_sprite_path = phase_data['sprite_path']
                event_description = self.current_event.description

                font = pygame.font.Font(None, 36)
                text_color = (255, 255, 255)

                event_description_surface = font.render(f"Event description: {event_description}", True, text_color)
                phase_description_surface = font.render(f"Phase description: {phase_description}", True, text_color)

                # Load the sprite image
                sprite_image = pygame.image.load(phase_sprite_path)
                self.screen.blit(sprite_image, (0, 0))

                # Blit the text surfaces onto the screen
                self.screen.blit(event_description_surface, (50, 50))
                self.screen.blit(phase_description_surface, (50, 80))

                # Set initial positions for the first button (top-left)
                initial_button_x = 50  # Starting X position for the first button in the row
                initial_button_y = 500  # Starting Y position for the first button in the first row
                button_x_gap = 50  # Horizontal gap between buttons
                button_y_gap = 20  # Vertical gap between rows

                scaled_button_width = 350  # Desired width
                scaled_button_height = 75  # Desired height

                self.buttons_rects = []  # Store rects for each choice to check clicks later

                # Loop to create the buttons
                for i, choice in enumerate(phase_choices):
                    choice_text = choice['description']
                    is_good_choice = self.check_available(choice)  # Check if the choice is available

                    # Calculate the position for the button
                    button_x = initial_button_x + (i % 2) * (scaled_button_width + button_x_gap)
                    button_y = initial_button_y + (i // 2) * (scaled_button_height + button_y_gap)
                    button_rect = pygame.Rect(button_x, button_y, scaled_button_width, scaled_button_height)
                    self.buttons_rects.append(button_rect)

                    # Select the appropriate button image and scale it
                    if is_good_choice:
                        button_image = pygame.transform.scale(self.choice_button_img,
                                                              (scaled_button_width, scaled_button_height))
                    else:
                        button_image = pygame.transform.scale(self.choice_button_false,
                                                              (scaled_button_width, scaled_button_height))

                    # Draw the button
                    self.screen.blit(button_image, button_rect.topleft)

                    # Render the text and center it on the button
                    text_surface = font.render(choice_text, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=button_rect.center)
                    self.screen.blit(text_surface, text_rect)

    def load_assets(self):
        self.bag_img = pygame.image.load("Sprites/bag.png")
        self.bag_hover_img = pygame.image.load("Sprites/bag_hover.png")
        self.energy_bar = pygame.image.load("Sprites/bar_energy.png")
        self.moral_bar = pygame.image.load("Sprites/bar_moral.png")
        self.coin_img = pygame.image.load("Sprites/coin.png")
        self.choice_button_img = pygame.image.load("Sprites/choice_button.png")
        self.choice_button_hover_img = pygame.image.load("Sprites/choice_btn_hover.png")
        self.day_bar_img = pygame.image.load("Sprites/day_box.png")
        self.project_img = pygame.image.load("Sprites/winror.png")
        self.choice_button_false = pygame.image.load("Sprites/choice_btn_false.png")

    def load_and_scale(self, path, size):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)

    def setup_rects(self):
        self.bag_rect = self.bag_hover_img.get_rect()

    def draw_coin(self):
        scaled_coin_img = pygame.transform.scale(self.coin_img, (35, 35))

        coin_x = 1100
        coin_y = 120

        self.screen.blit(scaled_coin_img, (coin_x, coin_y))

        coin_font = pygame.font.Font("pixeboy.ttf", 30)
        coin_text = f"{self.player.money}"
        coin_text_surface = coin_font.render(coin_text, True, (255, 255, 255))

        text_x = coin_x + scaled_coin_img.get_width() + 10
        text_y = coin_y + scaled_coin_img.get_height() - 25

        self.screen.blit(coin_text_surface, (text_x, text_y))

    def draw_bars(self):
        energy_bar_x = 1000
        energy_bar_y = 10
        moral_bar_x = 1000
        moral_bar_y = 60
        bar_width = 225
        bar_height = 20

        energy_color_bar_x = energy_bar_x + 50
        energy_color_bar_y = energy_bar_y + 19
        moral_color_bar_x = moral_bar_x + 50
        moral_color_bar_y = moral_bar_y + 15

        current_energy_width = (self.player.energy / self.player.max_energy) * bar_width
        current_moral_width = (self.player.moral / self.player.max_moral) * bar_width

        pygame.draw.rect(self.screen, (255, 255, 0), (energy_color_bar_x, energy_color_bar_y, current_energy_width, bar_height))
        pygame.draw.rect(self.screen, (0, 0, 255), (moral_color_bar_x, moral_color_bar_y, current_moral_width, bar_height))

        self.screen.blit(self.energy_bar, (energy_bar_x, energy_bar_y))
        self.screen.blit(self.moral_bar, (moral_bar_x, moral_bar_y))

    def draw_day_time_bar(self, day_font_size=26, time_font_size=26, day_bar_scale=(200, 75), time_bar_scale=(400, 75)):
        scaled_day_bar_img = pygame.transform.scale(self.day_bar_img, day_bar_scale)
        scaled_time_bar_img = pygame.transform.scale(self.day_bar_img, time_bar_scale)

        day_bar_x = 350
        bar_y = 0
        time_bar_x = 550

        self.screen.blit(scaled_day_bar_img, (day_bar_x, bar_y))
        self.screen.blit(scaled_time_bar_img, (time_bar_x, bar_y))

        day_font = pygame.font.Font("pixeboy.ttf", day_font_size)
        time_font = pygame.font.Font("pixeboy.ttf", time_font_size)

        day_text = f"Day: {self.day_of_the_week[self.day]}"
        time_text = f"Time: {self.time_periods[self.time]}"

        day_text_x = day_bar_x
        day_text_y = 35

    def draw_project_bar(self):
        scaled_project_img = pygame.transform.scale(self.project_img, (50, 50))

        project_x = 1100
        project_y = 170

        self.screen.blit(scaled_project_img, (project_x, project_y))

        project_text = f"{self.player.project} / {self.player.max_project}"
        project_font = pygame.font.Font("pixeboy.ttf", 26)
        project_text_surface = project_font.render(project_text, True, (255, 255, 255))

        text_x = project_x + scaled_project_img.get_width() + 10
        text_y = project_y + (scaled_project_img.get_height() // 2) - 10

        self.screen.blit(project_text_surface, (text_x, text_y))
