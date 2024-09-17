import json
import random

with open('events/events.json') as f:
    edata = json.load(f)
with open('items/items.json') as t:
    idata = json.load(t)

class Day:
    WEEKTIME = ["Early-Morning", "Morning", "Lunch", "Afternoon", "Evening"]

    def __init__(self, max_event=4):
        self.max_event = max_event
        self.events = {time: 0 for time in self.WEEKTIME}  # Initialize each time slot with 0
        self.items = {items: "00" for items in self.WEEKTIME}

    def add_event(self, event_id, time_slot):
        """ Adds an event ID to the time slot """
        if self.events[time_slot] == 0:
            self.events[time_slot] = event_id


        


    def generate_day(self):
        """ Randomly generates a day's schedule with events assigned to available time slots """
        available_time_slots = self.WEEKTIME[:]
        random.shuffle(available_time_slots)

        for event_id, event_data in edata['events'].items():
            possible_times = event_data["time_slots"]
            for time_slot in available_time_slots:
                if time_slot in possible_times and list(self.events.values()).count(0) > (5 - self.max_event):
                    self.add_event(event_id, time_slot)
                    available_time_slots.remove(time_slot)
                    break

    def get_event_ids(self):
        """ Returns a list of event IDs for the day, where 0 represents no event """
        return [self.events[time] for time in self.WEEKTIME]

    def display_schedule(self):
        print("Day's Schedule (Event IDs):", self.get_event_ids())


class Week:
    def __init__(self):
        self.days = {
            "Monday": Day(),
            "Tuesday": Day(),
            "Wednesday": Day(),
            "Thursday": Day(),
            "Friday": Day(),
            "Saturday": Day(),
            "Sunday": Day()
        }
        self.event = "00"

    def generate_week(self):
        self.generate_weekend()
        for day_name in self.days:
            self.days[day_name].generate_day()
        


    def generate_weekend(self):
        if random.choice([True, False]):
            for event_id, event_data in edata['events'].items():
                if "Weekend" in event_data["time_slots"]:
                    self.days["Saturday"].add_event(event_id, "Morning")
                    self.days["Sunday"].add_event(event_id, "Morning")
                

    def display_week_schedule(self):
        for day_name, day in self.days.items():
            print(f"{day_name}: {day.get_event_ids()}")

class Month:
    def __init__(self):
        self.weeks = {
            "0": Week(),
            "1": Week(),
            "2": Week(),
            "3": Week(),
        }
    def generateMonth(self):
        for week in self.weeks:
            self.weeks[week].generate_week()

    def displayMonth(self):
        for id, week in self.weeks.items():
            print(f"{id}: {week.display_week_schedule()}")

    
# Example usage
month = Month()
month.generateMonth()
month.displayMonth()