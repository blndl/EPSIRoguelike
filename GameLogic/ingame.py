
import pygame
from Events.event_gestion import Event
from Items.item_gestion import Item
pygame.font.init()

# made in game states to have an easier time managing the game
class InGameState:
    EVENT_PROGRESS = 0
    PHASE_PROGRESS = 1
    CHOICE_MAKING = 2

# main class of the file
class InGame:
    def __init__(self, screen, player, seed, game):
        # data from the main game class
        self.screen = screen
        self.player = player
        self.seed = seed
        self.game = game  # Reference to the main Game class

        # In-game state data and variables
        self.ingame_state = InGameState.EVENT_PROGRESS # state of the game
        self.current_event = None
        self.current_advancement = 0
        self.events = Event.load_events("Events/events.json") # load the events
        self.items = Item.load_items("Items/items.json") # load the items
        self.shop = []
        self.week_event = None
        self.index = 0
        self.buttons_rects = []

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

        # debugging only
        print("Seed: ", self.seed)

    def game_over(self):
        print("Game Over")
        self.game.state = "game_over"
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

        elif self.ingame_state == InGameState.EVENT_PROGRESS:
            self.advance_event()

        elif self.ingame_state == InGameState.PHASE_PROGRESS:
            self.advance_phases()

            self.ingame_state = InGameState.CHOICE_MAKING

        elif self.ingame_state == InGameState.CHOICE_MAKING:
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
        self.ingame_state = InGameState.PHASE_PROGRESS # change the state to phase progress

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
            print(self.shop)
            print(self.shop[0])
            print(self.shop[1])
            print(self.shop[0].item_id)
            print(self.shop[1].item_id)
            print(type(self.shop[1]))


            self.index += 3  # increment index for the 3 values used

            # debugging only
            print("Week event : ", self.week_event)
            print("Shop : ", self.shop)
            print("New week !")
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
                print("From based event : ", self.current_event , "00 seed")

            else:
                seed = self.seed[self.index]
                print("Random event seed : ", seed)
                print("Index : ", self.index)
                print(self.events)
                print(self.events.keys())
                if seed in self.events.keys() and seed != "00" : # if the seed is a number, char value
                    self.current_event = self.events[seed]
                    print("Random event : ", self.current_event)
                    self.index += 1  # increment index because the event had a seed
                elif seed in self.items.keys() and seed != "00": # if the seed is not 00 and is char, number value
                    print("Random item")
                    item = self.items[seed]
                    self.inventory_adder(item)  # manages the inventory of the player
                elif seed == "00":
                    print("No item")
                else:
                    print("SEED ERROR for item or item: ", seed)
                    error += 1
                    if error > 3:
                        print("Error count : ", error)
                        print("Full seed : ", self.seed)
                        print("Events list : ", self.events)
                        print("Index : ", self.index)
                        raise SystemExit(f"Shutting down the program due to SEED ERROR : {seed}") # avoid infinity loop
                    self.get_event(error) # calls itself back to try to get a new event
            # adds index because the event had a seed
            self.index += 1
            print("Incremented index : ", self.index)

        else:
            self.current_event = Event.get_event_by_is_choice_and_time(True, self.events, self.time_periods[self.time])
            print("From based event : ", self.current_event)

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
        print("len current event : ",len(self.current_event.phases))

        # verify if there are more phases
        if self.current_advancement + 1 < len(self.current_event.phases):
            self.current_advancement += 1  # Increment the advancement
        else:
            print(f"All phases completed for event {self.current_event.event_id}. Moving to next event.")
            self.current_advancement = 0  # Reset the advancement
            self.ingame_state = InGameState.PHASE_PROGRESS  # Go back to event progress state

    def select_choice(self, choice_number):
        choices = self.current_event.phases_choices_data(self.current_advancement)
        choice = choices[choice_number]
        print(f"Selected choice: {choice['description']}, money : {choice['money']}, energy : {choice['energy']}, moral : {choice['moral']}, project : {choice['project']}")
        self.player.update_player(choice)

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

    # method to draw the game with the same states as the handle events
    def draw(self):
        if self.ingame_state == InGameState.PHASE_PROGRESS:
            self.draw_current_phase()

        # Add more drawing logic as needed

    def draw_current_phase(self):
        if self.current_event:
            if not self.current_advancement >= len(self.current_event.phases):
                phase_data = self.current_event.phases_data()[self.current_advancement]
                phase_description = phase_data['description']
                phase_choices = phase_data['choices']
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




                # Create buttons directly using pygame.Rect
                self.buttons_rects = []  # Store rects for each choice to check clicks later
                button_y = 200  # Starting Y position for buttons
                for i, choice in enumerate(phase_choices):
                    choice_text = choice['description']
                    button_rect = pygame.Rect(50, button_y, 300, 50)
                    self.buttons_rects.append(button_rect)

                    # Draw the button (rectangle)
                    pygame.draw.rect(self.screen, (50, 200, 50), button_rect)

                    # Render and draw the text on the button
                    text_surface = font.render(choice_text, True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=button_rect.center)
                    self.screen.blit(text_surface, text_rect)

                    button_y += 60  # Move the next button down

    # draw the choice buttons
    def draw_choice_buttons(self):
        for button in self.buttons_rects:
            button.draw(self.screen)
