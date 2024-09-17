import json

class Event:
    def __init__(self, event_id, description, time_slots, phases):
        self.event_id = event_id
        self.description = description
        self.time_slots = time_slots
        self.phases = phases

    @classmethod
    def load_events(cls, file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return {event_id: cls(event_id, event_data['description'], event_data['time_slots'], event_data['phases'])
                for event_id, event_data in data['events'].items()}

    def get_event_data(self):
        return {
            "event_id": self.event_id,
            "description": self.description,
            "time_slots": self.time_slots,
            "phases": self.phases
        }

    def phases_data(self):
        return [
            {
                'description': phase.get('description', 'No description available'),
                'choices': phase['choices'],
                'sprite_path': phase['sprite_path'],
            }
            for phase in self.phases
        ]

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
events = Event.load_events('events.json')
print(json.dumps(events, default=lambda o: o.__dict__, indent=4))

event_id = '1A'
if event_id in events:
    print(f"Event ID: {event_id}")
    print(json.dumps(events[event_id].get_event_data(), indent=4))
    print(json.dumps(events[event_id].phases_data(), indent=4))
    print(json.dumps(events[event_id].phases_choices_data(), indent=4))
else:
    print(f"Event ID not found: {event_id}")

# Example usage
print(Event.load_events('events.json'))
event_id = '1A'
events_id = Event.load_events('events.json')
if event_id in events_id:
    print(f"Event ID: {event_id}")
    print(events_id[event_id].get_event_data())
    print(events_id[event_id].phases_data())
    print(events_id[event_id].phases_choices_data())
else:
    print(f"Event ID not found: {event_id}")