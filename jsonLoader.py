import json

class Json:
    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def load(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data

class BaseEntity:

    @classmethod
    def load_entity(cls, file_path):
        data = Json.load(file_path)
        return data

    @staticmethod
    def return_entity_data(self, list_of_return):
        return [getattr(self, return_data, None) for return_data in list_of_return]