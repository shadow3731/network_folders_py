import os, json, pickle, re, subprocess, socket, threading

from dialog import Dialog

class DataPerformer():
    """The class for manipulating with service and appearance data.
    
    Attributes:
        documents_folder (str): the user's local documents folder.
        service_file_name (str): the name of the file where service data is contained.
        appearance_file_name (str): the name of the file where appearance data is contained.
        a_data_key (str): the key of service data which contains the filepath to JSON appearance file.
        username_cred_key (str): the key of service data which contains the username of network credentials.
        password_cred_key (str): the key of service data which contains the password of network credentials.
        server_comp_name (str | None): the computer name where the appearance data is taken from.
    """
    
    def __init__(self):
        """Initializes DataPerformer instance.
        
        If a user has suitable OS, then gets the user's Documents folder.
        """
        
        self.documents_folder = self._get_documents_folder()
        
        self.service_file_name = 'local_data.picke'
        self.appearance_file_name = 'local_visual.json'
        
        self.a_data_key = 'appearance_file_path'
        self.creds_import_mode_key = 'credentials_import_mode'
        self.c_data_key = 'credentials_file_path'
        self.username_cred_key = 'username_credentials'
        self.password_cred_key = 'password_credentials'
        
        self.server_comp_name = None
                
    def load_service_data(self) -> dict:  
        """Loads the service data.
        
        If the user's Documents folder is defined, 
        tries to get file with the service data of the application. 
        If there is no file containing the service data, creates it.
        
        Returns:
            dict: The service data, if the service data from file was read successfully;
            None: If not or if the user's Documents folder was not defined.
        """
        
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
        """Saves the service data.
        
        If the user's Documents folder is defined, 
        tries to save new or updated service data into the file,
        which is inside of the user's Documents folder.
        
        Args:
            savable_data (dict): the new or updated service data.
        """
        
        if self.documents_folder:
            filepath = f'{self.documents_folder}\\{self.service_file_name}'
            with open(filepath, 'wb') as f:
                pickle.dump(savable_data, f)
                
    def load_data_from_server(self, filepath: str) -> dict:
        """Loads the appearance data from a server.
        
        If the server is defined and is currently online,
        connects to the filepath of the server, where the appearance data is.
        If the filepath exists, reads the appearance data
        and saves it into the user's local Documents folder.
        
        UTF-8-sig is used as a decoder of the appearance data,
        because the file with the appearance data might have
        unrecognized for regular UTF-8 decoder characters.
        
        If the file has invalid JSON syntaxis or unrecognized
        for UTF-8-sig decoder characters, creates 'askerror' window
        with error description and tries to load the appearance data locally.
        
        Args:
            filepath (str): the filepath of the file with appearance data which is on the server computer.
            
        Returns:
            dict: The appearance data, if the file was found and was correctly read or tries to do it locally.
        """
        
        if self.server_comp_name and self._is_server_online(self.server_comp_name):
            if os.path.exists(filepath):
                try:
                    with open(filepath, encoding='utf-8-sig') as f:
                        data = json.load(f)
                        
                        if filepath == self.a_data_key:
                            local_filepath = f'{self.documents_folder}/{self.appearance_file_name}'
                            self.save_appearance_data(data, local_filepath)
                        
                        return data
                    
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    if filepath == self.a_data_key:
                        message = f'Не удалось выгрузить данные из файла визуализации, находящегося на сервере.\n\n{e}'
                    elif filepath == self.c_data_key:
                        message = f'Не удалось выгрузить данные из файла сетевых учетных данных, находящегося на сервере.\n\n{e}'
                        
                    dialog = Dialog()
                    threading.Thread(
                        target=dialog.show_error,
                        args=(message,)
                    ).start()
                    
                    if filepath == self.a_data_key:
                        return self.load_data_locally()
                    else:
                        return None
        
        if filepath == self.a_data_key:
            return self.load_data_locally()
        else:
            return None
        
    def load_data_locally(self) -> dict:
        """Loads the appearance data from the user's local computer.
        
        If the user's Documents folder is defined, and the the path 
        to the file with appearance data exists, reads it.
        
        UTF-8-sig is used as a decoder of the appearance data,
        because the file with the appearance data might have
        unrecognized for regular UTF-8 decoder characters.
        
        If the file has invalid JSON syntaxis or unrecognized
        for UTF-8-sig decoder characters, creates 'askerror' window
        with error description.
            
        Returns:
            dict: The appearance data, if the file was found and was correctly read. 
            None: If the user's Documents folder or filepath to the file does not exist, or if an error occured while reading the file.
        """
        
        if self.documents_folder:
            local_filepath = f'{self.documents_folder}/{self.appearance_file_name}'
            if os.path.exists(local_filepath):
                try:
                    with open(local_filepath, encoding='utf-8-sig') as f:
                        return json.load(f)
                    
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    message = f'Не удалось выгрузить данные из файла визуализации, находящегося на этом устройстве.\n\n{e}'
                    dialog = Dialog()
                    threading.Thread(
                        target=dialog.show_error,
                        args=(message,)
                    ).start()
        
        return None
    
    def save_appearance_data(self, savable_data: dict, filepath: str):
        """Saves the appearance data.
        
        UTF-8-sig is used as an encoder of the appearance data,
        because the savable appearance data might have
        unrecognized for regular UTF-8 encoder characters.
        
        Args:
            savable_data (dict): the new or updated appearance data,
            filepath (str): the path where the appearance data is needed to be saved.
        """
        
        with open(filepath, 'w', encoding='utf-8-sig') as f:
            json.dump(savable_data, f, indent=4)
    
    def _create_if_not_exists(self, target: str, filepath: str=None):
        """Creates file if it does not exist.
        
        The file with service data is required to be not readable 
        with regular methods, so it is encrypted 
        (and then decrypted when is loaded) with pickle module.
        
        Args:
            target (str): the file which is needed to create,
            filepath (str): the path of this file.
        """
        
        if target == 'service_data':
            if not os.path.exists(filepath):
                data = {
                    self.a_data_key: '',
                    self.creds_import_mode_key: 'False',
                    self.c_data_key: '',
                    self.username_cred_key: '',
                    self.password_cred_key: ''
                }
                
                with open(filepath, 'wb') as f:
                    pickle.dump(data, f)
    
    def _get_documents_folder(self) -> str:
        """Gets the user's Documetns folder.
        
        Defines the user's OS and gets the local Documents folder.
        If it is impossible to define the OS, creates 'askerror' window
        reporting about the imposibillity to launch this application.
        
        If the Documents folder is defined, creates (if does not exist) 
        inner folder called as 'Network Folder' where the local service and
        appearance data are to contain. If failed to create inner folder,
        creates 'askerror' window reporting about the error.
        
        Returns:
            str: Local folder of data of the application.
            None: If unable to define the user's OS or create local folder.
        """
        
        if os.name == 'nt':
            doc_dir = f"{os.path.join(os.environ['USERPROFILE'], 'Documents')}"
        elif os.name == 'posix':
            doc_dir = f"{os.path.join(os.path.expanduser('~'), 'Documents')}"
        else:
            message = 'Невозможно запустить программу на этой операционной системе.'
            Dialog().show_error(message)
            
            return None
        
        folder_dir = f'{doc_dir}\\Network Folders'
        try:
            os.mkdir(folder_dir)
            
        except FileExistsError:
            pass
        
        except Exception as e:
            message = f'Во время выполнения операции создания локальной папки для этой программы произошла ошибка.\n\n{e}'
            Dialog().show_error(message)
            
            return None
        
        return folder_dir
        
    def _get_computer_ip_or_name(self, filepath: str) -> str:
        """Gets the server computer IP or name.
        
        Defines the server computer IP or name by the path
        where the file with appearance data is.
        Separates the server name from the filepath by RegEx.
        
        Args:
            filepath (str): the path to the file with appearance data.
            
        Returns:
            str:The server computer IP or name if defined.
            None: If not.
        """
        
        match = re.match(r'//([^/]+)', filepath)
        
        if match:
            return match.group(1)
        
        return None
        
    def _is_server_online(self, host: str) -> bool:
        """Defines if the server computer is online.
        
        Run command to define if the server computer is online.
        The command pings the server computer sending there
        1 packet within 1 second. After that generates a code
        of the command result. If it differs from 0,
        tries to connect to the server computer by sockets.
        
        Returns:
            bool (True): If the result code is 0 or the socket connection to the server computer is established.
            bool (False): If not.
        """
        
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