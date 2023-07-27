import os, json, pickle

class DataPerformer():
    
    def __init__(self):
        self.service_filepath = 'files/data.picke'
        self.appearance_filepath = 'files/data.json'
                
    def load_service_data(self) -> dict:
        self._create_if_not_exists()
        
        with open(self.service_filepath, 'rb') as f:
            return pickle.load(f)
        
    def save_service_data(self, savable_data: dict):
        with open(self.service_filepath, 'wb') as f:
            pickle.dump(savable_data, f)
        
    def load_appearance_data(self, filepath: str) -> dict:
        if os.path.exists(filepath):
            with open(filepath, encoding='utf8') as f:
                return json.load(f)
            
        elif os.path.exists(self.appearance_filepath):
            with open(self.appearance_filepath, encoding='utf8') as f:
                return json.load(f)
        
        return None
    
    def _create_if_not_exists(self):
        if not os.path.exists(self.service_filepath):
            data = {'path': '', 'password': '1111'}
            
            with open(self.service_filepath, 'wb') as f:
                pickle.dump(data, f)
    