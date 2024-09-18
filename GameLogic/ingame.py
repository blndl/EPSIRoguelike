from Events.event_gestion import Event
from player import Player
from generator import Month

# InGame class is used to manage the game loop, the events, the player and the month.
class InGame:
    def __init__(self, screen, player, month_data = None):
        self.player = player
        self.week_event = None
        self.events = Event.load_events("../Events/events.json")
        self.month = Month()
        self.month_data = month_data
        self.item = None
        self.update()

    # events for pygames
    def handle_event(self): # like clicks DO NOT FORGET
        pass

    # draw the screen
    def draw(self):
        pass

    # update the game
    def update(self, month_data=None):
        pass
        self.initialize_month_data(month_data)
        print(self.month_data)
        self.process_month_data()


    # run some functions
    def run(self):
        pass


    # initialize the month data
    def initialize_month_data(self, month_data):
        if not month_data:
            self.month.generateMonth()
            self.month_data = self.month.return_month()
        else:
            self.month_data = month_data

    # process the month data also the main loop of the game
    def process_month_data(self):
        time = 0
        day = 0
        week = 0
        month = 0
        for data in self.month_data:
            event, item = self.get_event_or_item(data)
            if day == 0 and time == 0: # start of a new week
                print("Week Start !")
                self.week_event = event
            time, day, week, month = self.update_time_day_week_month(time, day, week, month)
            if event:
                print("Event: ", event)
                self.event_phase(event)
            else:
                print("No event")
                self.choices(time)
            time += 1


    # get the event or item id
    def get_event_or_item(self, data):
        event = None
        item = None
        if data in self.events and data != "00":
            event = self.events[data]
        elif data[0].isalpha() and data != "00":
            item = self.events[data]
        return event, item


    # update the time, day, week and month of the game
    def update_time_day_week_month(self, time, day, week, month):
        # the time of a day
        if time >= 5:
            time = 0
            day += 1
        # the number of days in a week
        if day >= 7:
            day = 0
            week += 1
        #the number of weeks in a month
        if week >= 4:
            week = 0
            month += 1
            # recreate a seed for the month
            self.month_data = self.initialize_month_data()

        print("\nTime: ", time)
        print("Day: ", day)
        print("Week: ", week)
        print("Month: ", month)
        switch = {
            0 : "Early-Morning",
            1 : "Morning",
            2 : "Lunch",
            3 : "Afternoon",
            4 : "Evening",
        }
        print(switch.get(time))

        return time, day, week, month

    # the differents phases of an event are treated here
    def event_phase(self, event):
        for phase in event.phases_data():
            user_choice = None
            print("Phase: ", phase)
            # the choices inside an event phase are searched here
            switch = {i: choice for i, choice in enumerate(phase['choices'])}
            print(switch)
            print({key: switch[key]['description'] for key in switch})
            # if there are choices, the player will have to choose
            if switch != {}:
                while user_choice not in switch:
                    user_choice = int(input("Select a choice: "))
                    # if the choice is not in the choices, the player will have to choose again
                    if user_choice not in switch:
                        print("Invalid choice")
                print(switch.get(user_choice))
            # if there is only one choice, the player will have no choice

            elif len(switch) == 1:
                user_choice = 0
                print(switch.get(user_choice))

            # something went wrong...
            else:
                print("Something went wrong...")
                return

            self.player = self.player.update_player(switch.get(user_choice))

    # the choices when no event is happening
    def choices(self, time):
        # needed to get the choices at a specific time
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
        print(f"Your choices : {choices}")
        # if no choices found, print a message
        if choices == {}:
            print("No choices available")
            return
        # if there is only one choice, the player will have no choice
        if len(choices) == 1:
            self.event_phase(choices.get(0))
        # if there are choices, the player will have to choose
        else:
            user_choice = None
            while user_choice not in choices:
                user_choice = int(input("Select a choice: "))
                if user_choice not in choices:
                    print("Invalid choice")
            self.event_phase(choices.get(user_choice))




        print(Event.get_event_by_time(switch.get(time), self.events))
        print(switch.get(time, False))


user = Player("Gin")
game = InGame(None, user)