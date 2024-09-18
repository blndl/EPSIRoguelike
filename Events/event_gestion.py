from Json.json import BaseEntity

class Event(BaseEntity):
    def __init__(self, event_id, description, time_slots, phases, week_event, week_end, is_choice):
        self.event_id = event_id
        self.description = description
        self.time_slots = time_slots
        self.phases = phases
        self.week_event = week_event
        self.week_end = week_end
        self.is_choice = is_choice

    # This method is used to create a list of instances of the class Event with the data from events
    @classmethod
    def load_events(cls, file_path):
        data = cls.load_entity(file_path)
        return {event_id: cls(event_id, event_data['description'], event_data['time_slots'], event_data['phases'], event_data['week_event'], event_data['week_end'], event_data['is_choice'])
                for event_id, event_data in data['events'].items()}
        # the instances are the values of the dictionary, the keys are the event_id
        # example :
        # events = {
        #   'event_id': Event('event_id', 'description', 'time_slots', 'phases'), key : object
        #   'event_id2': Event('event_id2', 'description2', 'time_slots2', 'phases2'),
        # }
        # events['event_id']  returns -> Event('event_id', 'description', 'time_slots', 'phases')

        # Used to return the date of an event

    def get_event_data(self):
        return self.return_entity_data(self, ['event_id', 'description', 'time_slots', 'phases', 'week_event', 'week_end', 'is_choice'])

    # Used to return the data of the phases of an event
    def phases_data(self):
        return [
            {
                'description': phase.get('description', 'No description available'),
                'choices': phase.get('choices', 'No choices available'),
                'sprite_path': phase.get('sprite_path', 'No sprite path available'),
            }
            for phase in self.phases
        ]

    # Used to return the data of the choices of the phases of an event, all of them.
    def phases_choices_data(self, phase_number):
        phase = self.phases[phase_number]
        if phase:
            return [
                {
                    'description': choice.get('description', 'No description available'),
                    'effect': choice.get('effect', 'No effect available'),
                    'energy' : choice.get('energy', 'No energy available'),
                    'money' : choice.get('money', 'No money available'),
                    'moral' : choice.get('moral', 'No moral available'),
                }
                for choice in phase['choices']
            ]
        return False

# Example usage
#events = Event.load_events("events.json")
#for event_id, event in events.items():
#    print(f"Event ID: {event_id}")
#    print(event.get_event_data())
#    print(event.phases_data())
#    print(event.phases_choices_data())
#    print(event)

    @staticmethod
    def get_event_by_time(time, events):
        return {event_id : event for event_id, event in events.items() if time in event.time_slots}

    @staticmethod
    def get_event_by_week_event(week_event, events):
        return {event_id : event for event_id, event in events.items() if week_event == event.week_event}

    @staticmethod
    def get_event_by_week_end(week_end, events):
        return {event_id : event for event_id, event in events.items() if week_end == event.week_end}

    @staticmethod
    def get_event_by_is_choice_and_time(is_choice, events, time):
        return {event_id : event for event_id, event in events.items() if is_choice == event.is_choice and time in event.time_slots}