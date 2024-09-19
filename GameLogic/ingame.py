
import pygame
from Events.event_gestion import Event
from Items.item_gestion import Item
pygame.font.init()

# main class of the file
class InGame:
    def __init__(self, screen, player, seed, game):
        # data from the main game class
        self.screen = screen
        self.player = player
        self.seed = seed
        self.game = game  # Reference to the main Game class

        # In-game state data and variables
        self.current_event = None
        self.current_advancement = 0
        self.events = Event.load_events("Events/events.json") # load the events
        self.items = Item.load_items("Items/items.json") # load the items
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

        # function call
        self.advance_event()

        # debugging only
        print("Seed: ", self.seed)

    # method to handle the game over
    def game_over(self):
        print("Game Over")
        self.game.state = "game_over"

    # method to handle the win
    def win(self):
        print('Score : ', self.player.score)
        print("YOU WIN !")

    # method to handle the time
    def handle_time(self):
        # line to print the time
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


    # method to handle the in game states
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                print("Inventory passed")
                print(self.game.state)
                self.game.state = "inventory"
                print(self.game.state)
            elif event.key == pygame.K_ESCAPE:
                self.game.state = "pause_menu"
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_choice_making(event) # handle the choice making


    # method to advance the event
    def advance_event(self):
        # debugging only info
        print("\nIndex : ", self.index)
        # assign week event and shop
        self.week_start()

        self.open_shop()
        # get the event
        self.get_event()
        # adjust the time
        self.handle_time()
        self.current_advancement = 0
        print("len(self.current_event.phases) : ", len(self.current_event.phases))
        self.advance_phases()

    def week_start(self):
        if self.time == 0 and self.day == 0:
            self.week_event = None
            self.shop = []
            if self.seed[self.index] != "00":  # if the seed is not 00
                self.week_event = self.events[self.seed[self.index]]
                print("Week event changed !")
            for i in range (1, 3):
                if self.seed[self.index + i] != "00":
                    self.shop.append(self.items[self.seed[self.index + i]])

            self.index += 3  # increment index for the 3 values used
            print("increment index : ", self.index)

    def open_shop(self):
        if self.day == 2 and self.time == 2:
            print(self.time)
            self.game.state = "shop"

    def get_event(self, error=0):
        random_event = self.should_trigger_random_event()
        if not random_event:
            self.current_event = Event.get_event_by_is_choice_and_time(True, self.events, self.time_periods[self.time])
            print("From based event : ", self.current_event)

        else:
            if self.seed[self.index] == "00":
                print("No random event")
                self.current_event = Event.get_event_by_is_choice_and_time(True, self.events,
                                                                           self.time_periods[self.time])
                print("From based event : ", self.current_event, "00 seed")
            else:
                seed = self.seed[self.index]
                print("Random event seed : ", seed)
                print("Index : ", self.index)
                print(self.events)
                print(self.events.keys())
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
                        raise SystemExit("Shutting down the program due to SEED ERROR : ", seed)
                    self.get_event(error)
            self.index += 1
            print("Incremented index : ", self.index)


    def should_trigger_random_event(self):
        return self.time not in [0, 2, 4] # true if in list

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


    # method to advance the phases
    def advance_phases(self):
        if self.current_event is None:
            print("No current event to advance phases.")
            return

        # Check if there are more phases to advance
        if self.current_advancement + 1 < len(self.current_event.phases):
            self.current_advancement += 1
        else:
            print(f"All phases completed for event {self.current_event.event_id}. Moving to next event.")

    def select_choice(self, choice_number):
        choices = self.current_event.phases_choices_data(self.current_advancement)
        choice = choices[choice_number]
        print(
            f"Selected choice: {choice['description']}, money : {choice['money']}, energy : {choice['energy']}, moral : {choice['moral']}, project : {choice['project']}"
        )

        # Move directly to the next phase or event
        if self.current_advancement + 1 < len(self.current_event.phases):
            print(f"Phase {self.current_advancement} complete.")
            self.advance_phases()
        else:
            print("All phases complete.")
            print(f"Event {self.current_event.event_id} complete.")
            self.advance_event()

        self.buttons_rects = []  # Clear buttons after choice

    def handle_choice_making(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            choices = self.current_event.phases_choices_data(self.current_advancement)
            for choice in choices:
                is_good_choice = self.check_available(choice) # true bouton utilisable
                print("is choice good :", is_good_choice)

                # choice is choice data
                # ton bouton

    def check_available(self, choice):
            if choice['energy'] + self.player.energy < 0:
                return False
            elif choice['money'] + self.player.energy < 0:
                return False
            elif choice['moral'] + self.player.energy < 0:
                return False
            else:
                return True

    # method to draw the game with the same states as the handle events
    def draw(self):
        self.draw_current_phase()

        # Add more drawing logic as needed

    def draw_current_phase(self):
        if self.current_event:
            if not self.current_advancement >= len(self.current_event.phases):
                phase_data = self.current_event.phases_data()[self.current_advancement]
                phase_description = phase_data['description']
                phase_sprite_path = phase_data['sprite_path']
                event_description = self.current_event.description

                # Set up font and colors
                font = pygame.font.Font(None, 36)
                text_color = (255, 255, 255)

                # Render the text
                event_description_surface = font.render(f"Event description: {event_description}", True, text_color)
                phase_description_surface = font.render(f"Phase description: {phase_description}", True, text_color)
                current_time_surdace = font.render(f"Current time: {self.time_periods[self.time]}", True, text_color)
                current_day_surface = font.render(f"Current day: {self.day_of_the_week[self.day]}", True, text_color)
                project_surface = font.render(f"Project: {self.player.project}", True, text_color)
                project_max_surface = font.render(f"Max project: {self.player.max_project}", True, text_color)
                money_surface = font.render(f"Money: {self.player.money}", True, text_color)
                energy_surface = font.render(f"Energy: {self.player.energy}", True, text_color)
                moral_surface = font.render(f"Moral: {self.player.moral}", True, text_color)

                # Load the sprite image
                sprite_image = pygame.image.load(phase_sprite_path)

                # show the sprite image
                self.screen.blit(sprite_image, (0, 0))

                # Blit the text surfaces onto the screen
                self.screen.blit(event_description_surface, (50, 50))
                self.screen.blit(phase_description_surface, (50, 80))
                self.screen.blit(current_time_surdace, (1000, 50))
                self.screen.blit(current_day_surface, (1000, 70))
                self.screen.blit(project_surface, (1000, 90))
                self.screen.blit(project_max_surface, (1000, 110))
                self.screen.blit(money_surface, (1000, 130))
                self.screen.blit(energy_surface, (1000, 150))
                self.screen.blit(moral_surface, (1000, 170))
