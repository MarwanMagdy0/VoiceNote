import json
import os.path

class HandleJsonFiles:
    def __init__(self, file_path):
        self.file_path = file_path
        self.workspace_directory = os.path.dirname(self.file_path)
        if not os.path.isfile(self.file_path):
            self.save_data({})

    def save_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f)

    def read_data(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)
        
    def __getitem__(self, key):
        self.read_data()[key]
    
    def __setitem__(self, key: str, value) -> None:
        data = self.read_data()
        data[key] = value
        self.save_data(data)
        
    def keys(self):
        return self.data.keys()
