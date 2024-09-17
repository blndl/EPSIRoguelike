from Json.json import BaseEntity

class Event(BaseEntity):
    def __init__(self, event_id, description, time_slots, phases):
        self.event_id = event_id
        self.description = description
        self.time_slots = time_slots
        self.phases = phases

    # This method is used to create a list of instances of the class Event with the data from events
    @classmethod
    def load_events(cls, file_path):
        data = cls.load_entity(file_path)
        return {event_id: cls(event_id, event_data['description'], event_data['time_slots'], event_data['phases'])
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
        return self.return_entity_data(self,['event_id', 'description', 'time_slots', 'phases'])

    # Used to return the data of the phases of an event
    def phases_data(self):
        return [
            {
                'description': phase.get('description', 'No description available'),
                'choices': phase['choices'],
                'sprite_path': phase['sprite_path'],
            }
            for phase in self.phases
        ]

    # Used to return the data of the choices of the phases of an event, all of them.
    def phases_choices_data(self):
        return [
            {
                'description': choice['description'],
                'effect': choice['effect'],
                'money': choice.get('money', 0),
                'energy': choice.get('energy', 0),
                'moral': choice.get('moral', 0),
            }
            for phase in self.phases
            for choice in phase['choices']
        ]


# Example usage
events = Event.load_events("events.json")
for event_id, event in events.items():
    print(f"Event ID: {event_id}")
    print(event.get_event_data())
    print(event.phases_data())
    print(event.phases_choices_data())
    print(event)