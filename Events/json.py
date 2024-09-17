import json

class Json:
    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def load(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data