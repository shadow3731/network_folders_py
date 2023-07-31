import os, json, pickle, re

from dialog import Dialog

class DataPerformer():
    
    def __init__(self):
        self.service_filepath = 'files/local_data.picke'
        self.appearance_filepath = 'files/local_visual.json'
        
        self.password_filename = 'password.picke'
        
        self.a_data_key: str = 'appearance_file_path'
                
    def load_service_data(self) -> dict:
        self._create_if_not_exists('service_data')
        
        with open(self.service_filepath, 'rb') as f:
            return pickle.load(f)
        
    def save_service_data(self, savable_data: dict):
        with open(self.service_filepath, 'wb') as f:
            pickle.dump(savable_data, f)
        
    def load_appearance_data(self, filepath: str) -> dict:
        try:
            if os.path.exists(filepath):
                with open(filepath, encoding='utf8') as f:
                    data = json.load(f)
                    self.save_appearance_data(data, self.appearance_filepath)
                    
                    self._create_if_not_exists(
                        target='password',
                        filepath=filepath
                    )
                    
                    return data
                
            elif os.path.exists(self.appearance_filepath):
                with open(self.appearance_filepath, encoding='utf8') as f:
                    return json.load(f)
                
        except json.JSONDecodeError as e:
            message = f'Не удалось сохранить файл конфигурации. Проверьте синтаксис файла. Возможно присутствует лишний или отсутсвует необходимый знак.\n\n{e}'
            Dialog().show_error(message)
        
        return None
    
    def save_appearance_data(self, savabale_data: dict, filepath: str):
        with open(filepath, 'w', encoding='utf8') as f:
            json.dump(savabale_data, f, indent=4)
            
    def load_password(self) -> str:
        filepath = f'{self.load_service_data()[self.a_data_key]}/{self.password_filename}'
        if os.path.exists()
            
    def save_password(self, savable_psw: str):
        filepath = self.load_service_data()[self.a_data_key]
        
        self._create_if_not_exists(
            target='password',
            filepath=filepath
        )
        
        with open(filepath, 'wb') as f:
            pickle.dump(savable_psw, f)
    
    def _create_if_not_exists(self, target: str, filepath=None):
        if target == 'service_data':
            if not os.path.exists(self.service_filepath):
                data = {self.a_data_key: ''}
                
                with open(self.service_filepath, 'wb') as f:
                    pickle.dump(data, f)
                    
        elif target == 'password':
            match: re.Match[str] = re.search(r'\\([^\\]+)$', filepath)
            if match:
                psw_filepath = f'{filepath[:match.start()]}\\password.picke'
                if not os.path.exists(psw_filepath):
                    data = {'password': '1111'}
                    
                    with open(psw_filepath, 'wb') as f:
                        pickle.dump(data, f)
    