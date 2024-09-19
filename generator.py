import json
import random

with open('Events/events.json') as f:
    edata = json.load(f)
with open('Items/items.json') as t:
    idata = json.load(t)

class Day:
    WEEKTIME = ["Morning", "Afternoon"]

    def __init__(self, max_event=5):
        self.max_event = max_event
        self.events = {time: 0 for time in self.WEEKTIME}  # Initialize each time slot with 0
        self.items = {items: "00" for items in self.WEEKTIME}

    def add_event(self, event_id, time_slot):
        """ Adds an event ID to the time slot """
        if self.events[time_slot] == 0:
            self.events[time_slot] = event_id
        itemlist = []
        for item_id, item_data in idata['items'].items():
            if item_data["itemshop"] == False:
                itemlist.append(item_id)
        self.items[time_slot] = random.choice(itemlist)


        


    def generate_day(self):
        """ Randomly generates a day's schedule with events assigned to available time slots """
        available_time_slots = self.WEEKTIME
        random.shuffle(available_time_slots)
        for i in available_time_slots:
            list = []
            for event_id, event_data in edata['events'].items():
                if i in event_data["time_slots"] and event_data["week_end"] == False and event_data["is_choice"] == False:
                    list.append(event_id)
            if random.choice([True, False]):
                self.add_event(random.choice(list), i)
            
        #for event_id, event_data in edata['events'].items():
        #    possible_times = event_data["time_slots"]
         #  for time_slot in available_time_slots:
          #      if time_slot in possible_times and list(self.events.values()).count(0) > (5 - self.max_event):
           #         self.add_event(event_id, time_slot)
            #        available_time_slots.remove(time_slot)
             #       break
                    

    def get_event_ids(self):
        """ Returns a list of event IDs for the day, where 0 represents no event """
        list = []
        for i in self.WEEKTIME:
            list.append(self.events[i])
            if self.events[i] != 0:
                list.append(self.items[i])
        return [list]

    def display_schedule(self):
        print("Day's Schedule (Event IDs):", self.get_event_ids())


class Week:
    WEEKTIME = ["Early-Morning", "Morning", "Lunch", "Afternoon", "Evening"]

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
        itemlist = []
        for item_id, item_data in idata['items'].items():
            if item_data["itemshop"]:
                itemlist.append(item_id)
        self.item1 = random.choice(itemlist)
        self.item2 = random.choice(itemlist)
        while (self.item1 == self.item2):
            self.item2 = random.choice(itemlist)

            
            
    def generate_week(self):
        list = []
        self.generate_weekend()
        if random.choice([True, False]):
            for event_id, event_data in edata['events'].items():
                if event_data["week_event"]:
                    list.append(event_id) 
            self.event = random.choice(list)
        for day_name in self.days:
            self.days[day_name].generate_day()
        


    def generate_weekend(self):
        list = []
        if random.choice([True, False]):
            for event_id, event_data in edata['events'].items():
                if event_data["week_end"] and event_data["is_choice"] == False:
                    list.append(event_id) 
            self.days["Saturday"].add_event(random.choice(list), "Morning")
            self.days["Sunday"].add_event(random.choice(list), "Morning")
                

    def display_week_schedule(self, list):
        for day_name, day in self.days.items():
            for i in day.get_event_ids():
                for j in i:
                    if j != 0:
                        list.append(j)
                    else:
                        list.append("00")            
        return(list)


class Month:
    def __init__(self):
        self.weeks = {
            "0": Week(),
            "1": Week(),
            "2": Week(),
            "3": Week(),
        }
        self.list = []
        self.generateMonth()

    def generateMonth(self):
        for week in self.weeks:
            self.weeks[week].generate_week()

    def return_month(self):
        for id, week in self.weeks.items():
            self.list.append(week.event)
            self.list.append(week.item1)
            self.list.append(week.item2)
            self.list = week.display_week_schedule(self.list)
        return self.list
        
            

    
# Example usage
month = Month()
month.generateMonth()
list = month.return_month()
str = "".join(list)
print(str,' ', len(str))
