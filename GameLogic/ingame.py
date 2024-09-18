import pygame
from Events.event_gestion import Event
from Items.item_gestion import Item
pygame.font.init()

# made in game states to have an easier time managing the game
class InGameState:
    EVENT_PROGRESS = 0
    PHASE_PROGRESS = 1
    CHOICE_MAKING = 2
    INVENTORY_VIEW = 3
    PAUSED = 4

# made a class to draw the text and buttons, but I don't know if it's useful
class ToDraw:
    FONT = pygame.font.Font(None, 36)

# button class again idk if it's useful
class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = (50, 200, 50)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        label = self.font.render(self.text, True, (0, 0, 0))
        text_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

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
        self.buttons = []

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
        # debugging only
        print("Seed: ", self.seed)

    # method to handle the time
    def handle_time(self):
        if self.time >= 4:
            self.time = 0
            self.day += 1
            if self.day >= 7:
                self.day = 0
                self.week += 1
                if self.week >= 4:
                    self.week = 0
                    self.month += 1
        else:
            self.time += 1

        # line to print the time
        print(f"Time: {self.time}, Day: {self.day}, Week: {self.week}, Month: {self.month}")
        print(f"Current time period: {self.time_periods[self.time]}")

    # method to handle the in game states
    def handle_events(self, event):
        if self.ingame_state == InGameState.EVENT_PROGRESS:
            self.handle_event_progress(event) # handle the event progress
        elif self.ingame_state == InGameState.PHASE_PROGRESS:
            self.handle_phase_progress(event) # handle the phase progress
        elif self.ingame_state == InGameState.INVENTORY_VIEW:
            self.handle_inventory_view(event) # not sure about this one
        elif self.ingame_state == InGameState.PAUSED:
            self.handle_paused(event) # this one either

    # method to handle the event progress
    def handle_event_progress(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: # debugging for now, i mean event then shouldn't change much
            self.advance_event()

    # method to advance the event
    def advance_event(self):
        # debugging only info
        print("index : ", self.index)
        print("Items : ", self.items.keys())
        print("Events : ", self.events.keys())
        # assign week event and shop
        self.week_start()
        # get the event
        self.get_event()
        # adjust the time
        self.handle_time()
        self.ingame_state = InGameState.PHASE_PROGRESS # change the state to phase progress

    def week_start(self):
        if self.time == 0 and self.week == 0 and self.day == 0:
            self.week_event = None
            self.shop = []
            if self.seed[self.index] != "00":  # if the seed is not 00
                self.week_event = self.events[self.seed[self.index]]
                print("Week event changed !")
            for i in range (1, 3):
                if self.seed[self.index + i] != "00":
                    self.shop.append(self.items[self.seed[self.index + i]])

            self.index += 3  # increment index for the 3 values used

            # debugging only
            print("Week event : ", self.week_event)
            print("Shop : ", self.shop)
            print("New week !")
            print("increment index : ", self.index)

    def get_event(self, error=0):
        random_event = self.should_trigger_random_event()
        if random_event:
            if self.seed[self.index] == "00":
                print("No random event")
                self.current_event = Event.get_event_by_is_choice_and_time(True, self.events, self.time_periods[self.time])
                print("From based event : ", self.current_event)

            else:
                if self.seed[self.index] != "00" and self.seed[self.index][1].isdigit():
                    self.current_event = Event.get_event_by_is_choice_and_time(True, self.events,
                                                                               self.time_periods[self.time])
                    self.current_event = Event.get_event_by_is_choice_and_time(True, self.events,
                                                                               self.time_periods[self.time])
                    print("From based event : ", self.current_event, "00 seed")
                else:
                    if self.seed[self.index][1].isdigit():
                        self.current_event = self.events[self.seed[self.index]]
                        print("Random event : ", self.current_event)
                        if self.seed[self.index][0].isdigit():
                            item = self.items[self.seed[self.index]]
                            self.index += 1  # increment index because the item had a seed
                            self.inventory_adder(item)  # manages the inventory of the player
                        else:
                            print("SEED ERROR for item : ", self.seed[self.index])
                    else:
                        print("SEED ERROR for event: ", self.seed[self.index])
                        error += 1
                        if error < 3:
                            print("Error count : ", error)
                            raise SystemExit("Shutting down the program due to SEED ERROR") # avoid infinity loop
                        self.get_event(error) # calls itself back to try to get a new event

            # adds index because the event had a seed
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

    # method to handle the phase progress
    def handle_phase_progress(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: # debugging for now
            self.advance_phases()
            self.create_choice_buttons(self.current_event.phases_choices_data(self.current_advancement)) # to make the buttons based on the choices get the choices values

    # method to advance the phases
    def advance_phases(self):
        # verify if there are more phases
        print("Curent game state : ", self.ingame_state)
        if self.current_advancement < len(self.current_event.phases):
            self.get_choices() # get the choices

            if self.current_advancement +1 < len(self.current_event.phases):
                self.current_advancement += 1 # increment the advancement
            else:
                self.ingame_state = InGameState.EVENT_PROGRESS  # commes back to event progress

    # method to get the choices used to debug
    def get_choices(self):
        choices = self.current_event.phases_choices_data(self.current_advancement) # get the choices
        for choice in choices: # loop through the choices
            # debugging only
            print("\nChoice: ", choice)
            print("Description: ", choice['description'])
            print("Effect: ", choice['effect'])
            print("Energy: ", choice['energy'])
            print("Money: ", choice['money'])
            print("Moral: ", choice['moral'])
            print("Project: ", choice['project'])

    def select_choice(self, choice_number):
        choices = self.current_event.phases_choices_data(self.current_advancement)
        choice = choices[choice_number]
        self.player.update_player(choice)

    # to create the buttons by using a class
    def create_choice_buttons(self, choices):
        self.buttons = []
        for i, choice in enumerate(choices):
            button = Button(50, 200 + i * 60, 200, 50, choice, ToDraw.FONT)
            self.buttons.append(button)

    # not yet
    def handle_choice_making(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(self.buttons):
                if button.is_clicked(event.pos):
                    self.select_choice(i)
                    self.buttons = []  # Clear buttons after choice
                    if len(self.current_event.phases) > self.current_advancement :
                        print(f"Event {self.current_event.event_id} complete.")
                        self.current_event = None
                        self.ingame_state = InGameState.EVENT_PROGRESS
                    else:
                        self.ingame_state = InGameState.EVENT_PROGRESS
                    break

    # could be used to show the inventory
    @staticmethod
    def handle_inventory_view(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                pass
                # i don't know if values are kept betwen the differnt states so i'll just leave it like this for now

    # could be used to pause the game
    @staticmethod
    def handle_paused(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pass
                # same thing

    # method to draw the game with the same states as the handle events
    def draw(self):
        if self.ingame_state == InGameState.EVENT_PROGRESS:
            self.draw_current_event()
        elif self.ingame_state == InGameState.PHASE_PROGRESS:
            self.draw_current_phase()
        elif self.ingame_state == InGameState.INVENTORY_VIEW:
            self.game.inventory.draw_inventory()
        elif self.ingame_state == InGameState.PAUSED:
            self.game.pause_menu.draw()
        # Add more drawing logic as needed

    # draws on the screen the name and description of the current event
    def draw_current_event(self):
        if self.current_event:
            event_name = self.current_event.name
            event_description = self.current_event.description

            # Set up font and colors
            font = pygame.font.Font(None, 36)
            text_color = (255, 255, 255)  # White
            background_color = (0, 0, 0)  # Black

            # Render the text
            name_surface = font.render(f"Event name: {event_name}", True, text_color)
            description_surface = font.render(f"Event description: {event_description}", True, text_color)

            # Fill the screen with the background color
            self.screen.fill(background_color)

            # Blit the text surfaces onto the screen
            self.screen.blit(name_surface, (50, 50))
            self.screen.blit(description_surface, (50, 100))

            # Update the display
            pygame.display.flip()

    def draw_current_phase(self):
        if self.current_event:
            if not self.current_advancement >= len(self.current_event.phases):
                phase_data = self.current_event.phases_data()[self.current_advancement]
                phase_description = phase_data['description']
                phase_choices = phase_data['choices']
                phase_sprite_path = phase_data['sprite_path']

                # Set up font and colors
                font = pygame.font.Font(None, 36)
                text_color = (255, 255, 255)

                # Render the text
                description_surface = font.render(f"Phase description: {phase_description}", True, text_color)
                choices_surface = font.render(f"Choices: {phase_choices}", True, text_color)
                # Load the sprite image
                sprite_image = pygame.image.load(phase_sprite_path)

                # show the sprite image
                self.screen.blit(sprite_image, (0, 0))

                # Blit the text surfaces onto the screen
                self.screen.blit(description_surface, (50, 100))
                self.screen.blit(choices_surface, (50, 50))

                # Update the display
                pygame.display.flip()


    def draw_choice_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)

    # don't know if i'll use it
    def update(self):
        # Update game logic, such as event progression, animations, etc.
        pass  # Add any necessary update logic here

    # method to change the phase to the inventory view don't know if it's useful but it's here
    def interrupt_to_inventory(self):
        # Method to switch to inventory view
        self.ingame_state = InGameState.INVENTORY_VIEW