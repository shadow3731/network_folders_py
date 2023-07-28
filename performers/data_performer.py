import os, json, pickle

class DataPerformer():
    
    def __init__(self):
        self.service_filepath = 'files/local_data.picke'
        self.appearance_filepath = 'files/visual.json'
                
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
                data = json.load(f)
                self.save_appearance_data(data, self.appearance_filepath)
                return data
            
        elif os.path.exists(self.appearance_filepath):
            with open(self.appearance_filepath, encoding='utf8') as f:
                return json.load(f)
        
        return None
    
    def save_appearance_data(self, savabale_data: dict, filepath: str):
        with open(filepath, 'w', encoding='utf8') as f:
            json.dump(savabale_data, f, indent=4)
    
    def _create_if_not_exists(self):
        if not os.path.exists(self.service_filepath):
            data = {'appearance_file_path': ''}
            
            with open(self.service_filepath, 'wb') as f:
                pickle.dump(data, f)
    