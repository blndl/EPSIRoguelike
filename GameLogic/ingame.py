import pygame
from Events.event_gestion import Event
from Items.item_gestion import Item
from generator import Month

# InGame class is used to manage the game loop, the events, the player and the month.
class InGame:
    def __init__(self, screen, player, month_data, game,  shop=None, day=0, week=0, month=0, time=0):
        self.game = game
        self.player = player
        self.week_event = None
        self.events = Event.load_events("Events/events.json")
        self.items = Item.load_items("Items/items.json")
        self.month = Month()
        self.month_data = month_data
        self.shop = shop
        self.day = day
        self.week = week
        self.month_int = month
        self.time = time

    # events for pygames
    def handle_events(self, game_event): # like clicks DO NOT FORGET
        if game_event.type == pygame.KEYDOWN:
            if game_event.key == pygame.K_ESCAPE:
                self.game.state = "Pause_menu"

        if game_event.type == pygame.MOUSEBUTTONDOWN:
            self.update()



    # draw the screen
    def draw(self):
        pass

    # update the game
    def update(self):
        pass
        self.initialize_month_data()
        self.process_month_data()


    # run some functions
    def run(self):
        pass


    # initialize the month data
    def initialize_month_data(self):
        if not self.month_data:
            self.month.generateMonth()
            self.month_data = self.month.return_month()
            print(self.month_data)
        else:
            print("Month data already initialized")
            print(self.month_data)
            return
    # process the month data also the main loop of the game
    def process_month_data(self):
        index = 0
        while index < len(self.month_data):
            index = self.process_week_start(index)
            print("\nindex : ", index)
            print("time : ", self.time)
            if self.time == 0 or self.time == 2 or self.time == 4:
                self.choices(self.time)
            else:
                index += 1
                event, item = self.get_event_or_item(self.month_data[index])
                if item and len(self.player.bag) <= 32:
                    self.player.bag.append(item.item_id)
                    print("\nItem added to the bag : ", item.item_id)
                    print("Bag: ", self.player.bag, "\n")
                else:
                    self.process_data_entry(event)

            self.update_time_day_week_month()
            self.time += 1

    def process_week_start(self, index):
        if self.day == 0 and self.time == 0:  # start of a new week
            self.week_event = self.month_data[index]
            self.shop = [self.month_data[index + 1], self.month_data[index + 2]]
            index += 3
            print("\nWeek Event: ", self.week_event)
            print("Shop: ", self.shop)
        return index

    def process_data_entry(self, event):
        print("Event: ", event)
        switch = [0, 2, 4]
        if self.time in switch or event == False:
            if self.time in switch:
                print("it is choice Time: ", self.time)
            else:
                print("No event")
            self.choices(self.time)
            return

        elif event:
            print("Event: ", event)
            self.event_phase(event)
            return
        else:
            print("Something went wrong... in process_data_entry")
            print("Event: ", event)
            return


    # get the event or item id
    def get_event_or_item(self, data):
        print("Data: ", data)
        print("Events: ", self.events.keys())
        print("Items: ", self.items.keys())
        event = None
        item = None
        if data in self.events and data != "00":
            event = self.events[data]
        elif data in self.items and data != "00":
            item = self.items[data]
        else :
            print("No event or item found")
            return False, False
        print("Event in get_event_or_item: ", event)
        return event, item


    # update the time, day, week and month of the game
    def update_time_day_week_month(self):
        # the time of a day
        if self.time >= 4:
            self.time = 0
            self.day += 1
        # the number of days in a week
        if self.day >= 7:
            self.day = 0
            self.week += 1
        #the number of weeks in a month
        if self.week >= 4:
            self.week = 0
            self.day = 0
            self.time = 0
            self.month_int += 1
            # recreate a seed for the month
            self.initialize_month_data() # creates a new seed for the month
        return

    # the differents phases of an event are treated here
    def event_phase(self, event):
        print("event_phase is running")
        print("Event: ", event)
        for phase in event.phases_data():
            print("Phase: ", phase)
            # the choices inside an event phase are searched here
            switch = {i: choice for i, choice in enumerate(phase['choices'])}
            print(switch)
            print({key: switch[key]['description'] for key in switch})
            player_choice = self.player_choose(switch)
            self.player = self.player.update_player(player_choice)
            print("player updated")

    def player_choose(self, choices, event = None):
        print("player_choose is running")
        player_choice = None
        print("Choices: ", choices)

        #if there is only one choice, the player will have no choice
        #if len(choices) == 1:
        #    player_choice = choices.get(0)
        #    print("player not choice : ", player_choice)

        # if there are choices, the player will have to choose
        if choices != {}:
            while player_choice not in choices:
                player_choice = int(input("Select a choice: "))
                # if the choice is not in the choices, the player will have to choose again
                if player_choice not in choices:
                    print("Invalid choice")
            player_choice = choices.get(player_choice)
            print("player_choice: ", player_choice)


        elif len(choices) == 0:
            print("No choices found")
            return None
        # something went wrong...
        else:
            print("Something went wrong... in player_choose")
            return False

        return player_choice


    # the choices when no event is happening
    def choices(self, time):
        # needed to get the choices at a specific time
        print("choices is running")
        switch = {
            0 : "Early-Morning",
            1 : "Morning",
            2 : "Lunch",
            3 : "Afternoon",
            4 : "Evening",
        }
        # get the choices in dict format {0: choice, 1: choice, ...}
        choices = {i: choice for i, (key, choice) in
                   enumerate(Event.get_event_by_is_choice_and_time(True, self.events, switch.get(time)).items())
                    }
        # if no choices found, print a message
        self.event_phase(choices.get(0))
