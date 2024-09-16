import json
import random

with open('Events/events.json') as f:
    data = json.load(f)

class Day:
    TIME = ["Early-Morning", "Morning", "Lunch", "Afternoon", "Evening"]

    def __init__(self, max_event):
        self.max_event = max_event
        self.events = {time: 0 for time in self.TIME}  # Initialize each time slot with 0

    def add_event(self, event_id, time_slot):
        """ Adds an event ID to the time slot """
        if self.events[time_slot] == 0:
            self.events[time_slot] = int(event_id)

    def generate_day(self):
        """ Randomly generates a day's schedule with events assigned to available time slots """
        available_time_slots = self.TIME[:]
        random.shuffle(available_time_slots)

        for event_id, event_data in data['events'].items():
            possible_times = event_data["time_slots"]
            for time_slot in available_time_slots:
                if time_slot in possible_times and list(self.events.values()).count(0) > (5 - self.max_event):
                    self.add_event(event_id, time_slot)
                    available_time_slots.remove(time_slot)
                    break

    def get_event_ids(self):
        """ Returns a list of event IDs for the day, where 0 represents no event """
        return [self.events[time] for time in self.TIME]

    def display_schedule(self):
        print("Day's Schedule (Event IDs):", self.get_event_ids())

# Example usage
day = Day(4)
day.generate_day()
day.display_schedule()
