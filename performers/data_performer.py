import os, json, pickle, re, subprocess, socket

from dialog import Dialog

class DataPerformer():
    
    def __init__(self):
        self.documents_folder = self._get_documents_folder()
        
        self.service_file_name = 'local_data.picke'
        self.appearance_file_name = 'local_visual.json'
        # self.password_filename = 'password.picke'
        
        self.a_data_key: str = 'appearance_file_path'
        
        self.server_comp_name = None
                
    def load_service_data(self) -> dict:
        if self.documents_folder:
            filepath = f'{self.documents_folder}\\{self.service_file_name}'
            
            self._create_if_not_exists('service_data', filepath)
            
            with open(filepath, 'rb') as f:
                data: dict = pickle.load(f)
                
                self.server_comp_name = self._get_computer_ip_or_name(
                    filepath=data[self.a_data_key]
                )
                
                return data
            
        return None
        
    def save_service_data(self, savable_data: dict):
        if self.documents_folder:
            filepath = f'{self.documents_folder}/{self.service_file_name}'
            with open(filepath, 'wb') as f:
                pickle.dump(savable_data, f)
                
    def load_appearance_data_from_server(self, filepath: str) -> dict:
        if self.server_comp_name and self._is_server_online(self.server_comp_name):
            if os.path.exists(filepath):
                try:
                    with open(filepath, encoding='utf8') as f:
                        data = json.load(f)
                        
                        local_filepath = f'{self.documents_folder}/{self.appearance_file_name}'
                        self.save_appearance_data(data, local_filepath)
                        
                        return data
                    
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    message = f'Не удалось выгрузить данные из файла визуализации, находящегося на сервере.\n\n{e}'
                    Dialog().show_error(message)
                    
                    return self.load_appearance_data_locally(self)
        
    def load_appearance_data_locally(self) -> dict:
        if self.documents_folder:
            local_filepath = f'{self.documents_folder}/{self.appearance_file_name}'
            if os.path.exists(local_filepath):
                try:
                    with open(local_filepath, encoding='utf8') as f:
                        return json.load(f)
                    
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    message = f'Не удалось выгрузить данные из файла визуализации, находящегося на этом устройстве.\n\n{e}'
                    Dialog().show_error(message)
        
                    return None
    
    def save_appearance_data(self, savabale_data: dict, filepath: str):
        with open(filepath, 'w', encoding='utf8') as f:
            json.dump(savabale_data, f, indent=4)
            
    # def load_password(self) -> str:
    #     filepath = f'{self.load_service_data()[self.a_data_key]}/{self.password_filename}'
    #     if os.path.exists(filepath):
    #         with open(filepath, 'rb') as f:
    #             return pickle.load(f)
            
    #     return None
            
    # def save_password(self, savable_psw: str):
    #     filepath = self.load_service_data()[self.a_data_key]
        
    #     self._create_if_not_exists(
    #         target='password',
    #         filepath=filepath
    #     )
        
    #     with open(filepath, 'wb') as f:
    #         pickle.dump(savable_psw, f)
    
    def _create_if_not_exists(self, target: str, filepath: str=None):
        if target == 'service_data':
            if not os.path.exists(filepath):
                data = {self.a_data_key: ''}
                
                with open(filepath, 'wb') as f:
                    pickle.dump(data, f)
                    
        # elif target == 'password':
        #     match: re.Match[str] = re.search(r'[\\/]([^\\/]+)$', filepath)
        #     if match:
        #         psw_filepath = f'{filepath[:match.start()]}\\{self.password_filename}'
        #         if not os.path.exists(psw_filepath):
        #             data = {'password': '1111'}
                    
        #             with open(psw_filepath, 'wb') as f:
        #                 pickle.dump(data, f)
    
    def _get_documents_folder(self) -> str:
        if os.name == 'nt':
            doc_dir = f"{os.path.join(os.environ['USERPROFILE'], 'Documents')}"
        elif os.name == 'posix':
            doc_dir = f"{os.path.join(os.path.expanduser('~'), 'Documents')}"
        else:
            message = 'Невозможно запустить программу на этой операционной системе.'
            Dialog().show_error(message)
            return None
        
        folder_dir = f'{doc_dir}/Network Folders'
        try:
            os.mkdir(folder_dir)
            
        except FileExistsError:
            pass
        
        except Exception as e:
            message = 'Во время выполнения операции создания локальной папки для этой программы произошла ошибка.\n\n{e}'
            Dialog().show_error(message)
            return None
        
        finally:
            return folder_dir
        
    def _get_computer_ip_or_name(self, filepath: str) -> str:
        match = re.match(r'//([^/]+)', filepath)
        
        if match:
            return match.group(1)
        
        return None
        
    def _is_server_online(self, host: str) -> bool:
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '1', host], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if result.returncode == 0:
            return True
        
        else:
            try:
                ip = socket.gethostbyname(host)
                return True
            
            except socket.gaierror:
                return False