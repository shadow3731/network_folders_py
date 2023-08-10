import tkinter as tk
from tkinter.font import Font

import re, subprocess, platform, threading

from cursor import Cursor
from dialog import Dialog
from performers.data_performer import DataPerformer

class ButtonsPerformer():
    
    def __init__(self, cursor: Cursor, data_performer: DataPerformer):
        self.cursor = cursor
        self.dp = data_performer
    
    def configure_buttons(self, data: dict) -> list:
        positions: list = []
        
        if data.get('groups'):
            groups_data: dict = data['groups']
            group_index = 0
                
            while True:
                group_index += 1
                    
                if groups_data.get(f'group{group_index}') and groups_data[f'group{group_index}'].get('buttons'):
                    buttons_data: dict = groups_data[f'group{group_index}']['buttons']
                    button_index = 0
                    positions.append([])
                        
                    while True:
                        button_index += 1
                            
                        if buttons_data.get(f'button{button_index}'):               
                            positions[group_index-1].append(
                                self.cursor.place_button(
                                    buttons_data[f'button{button_index}']
                                )
                            )
                            
                        else:
                            self.cursor.move_to_new_group()  
                            break
                else:
                    return positions
                
        return None
            
    def show_buttons(self, data: dict, positions: list, root: tk.Frame):
        s_data = self.dp.load_service_data()
        credentials = {
            'username': s_data[self.dp.username_cred_key],
            'password': s_data[self.dp.password_cred_key]
        }
        
        for i in range(len(positions)):
            group_data: dict = data['groups'][f'group{i+1}']
            
            for j in range(len(positions[i])):
                button_data = group_data['buttons'][f'button{j+1}']
                
                button = tk.Button(
                    master=root,
                    text=button_data['name'],
                    font=Font(family='Calibri', size=11, weight='bold'),
                    relief=tk.SOLID,
                    borderwidth=1,
                    bg=button_data['bg_color'],
                    fg=button_data['fg_color']
                )
                
                button.bind(
                    '<Button-1>', 
                    lambda e, 
                        button=button,
                        data=button_data: 
                            self._start_action(e, button, data, credentials)
                )
                
                button.bind(
                    '<Return>', 
                    lambda e, 
                        button=button,
                        data=button_data: 
                            self._start_action(e, button, data, credentials)
                )
                    
                button.place(
                    x=positions[i][j][0],
                    y=positions[i][j][1],
                    width=positions[i][j][2],
                    height=positions[i][j][3]
                )
                
    def _start_action(
        self, 
        event, 
        button: tk.Button, 
        b_data: dict,
        s_data: dict
    ):
        button_name = b_data['name']
        button_dir = b_data['path']
        button.config(text='Подождите')
        
        threading.Thread(
            target=self._open_directory,
            args=(button_dir, button, button_name, s_data)
        ).start()

        button.config(
            relief=tk.SOLID,
            borderwidth=1,
            bg=b_data['bg_color'],
            fg=b_data['fg_color']
        )
    
    def _open_directory(
        self, 
        dir: str, 
        btn: tk.Button, 
        name: str,
        creds: dict
    ):
        if platform.system() == 'Windows':
            startup_info = subprocess.STARTUPINFO()
            startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup_info.wShowWindow = subprocess.SW_HIDE
            
            if self._is_file(dir):
                file_cmd_res = subprocess.run(
                    dir,
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    startupinfo=startup_info
                )
                
                if file_cmd_res.returncode != 0:
                    self._show_error(file_cmd_res)
                
            else:
                map_cmd = f'net use "{dir}" /user:"{creds["username"]}" "{creds["password"]}"'
                map_cmd_res = subprocess.run(
                    map_cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    startupinfo=startup_info
                )
                
                if map_cmd_res.returncode == 0:
                    dir_cmd = f'explorer "{dir}"'
                    dir_cmd_res = subprocess.run(
                        dir_cmd, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE
                    )
                    
                    if dir_cmd_res.returncode == 0 or dir_cmd_res.returncode == 1:
                        disconn_cmd = f'net use "{dir}" /delete'
                        subprocess.run(
                            disconn_cmd, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            startupinfo=startup_info
                        )
                        
                    else:
                        self._show_error(dir_cmd_res)
                    
                else:
                    self._show_error(map_cmd_res)
        
        else:
            try:
                subprocess.run(
                    f'echo "{creds["password"]}" | sudo -S open "{dir}"'
                )
                
            except subprocess.CalledProcessError as e:
                message = f"Ошибка выполнения консольной команды.\n\n{e}"
                Dialog().show_error(message)
            except FileNotFoundError as e:
                message = f"Не удалось открыть файл или папку. Возможно имеются проблемы с сетью либо данной директории не существует.\n\n{e}"
                Dialog().show_error(message)
            except OSError as e:
                message = f"Ошибка в системе.\n\n{e}"
                Dialog().show_error(message)
            except ValueError as e:
                message = f"Неверное значение.\n\n{e}"
                Dialog().show_error(message)
            except subprocess.TimeoutExpired as e:
                message = f"Превышено время ожидания открытия файла или папки.\n\n{e}"
                Dialog().show_error(message)
                
        btn.config(text=name)
        
    def _show_error(self, command_result: subprocess.CompletedProcess[bytes]):
        msg_cmd = f'net helpmsg {command_result.returncode}'
        msg_cmd_res = subprocess.run(msg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        message = f'Возникла ошибка при выполнении операции.\n\nСетевая ошибка {command_result.returncode}.\n\n{msg_cmd_res.stdout.decode("ibm866").strip()}\n\n{command_result.stderr.decode("ibm866").strip()}'
        Dialog().show_error(message)
        
    def _is_file(self, path: str) -> bool:
        file_extension_pattern = r'\.(?:exe|txt|json|csv|jpg|jpeg|png|pdf|doc|docx|xls|xlsx|bat|mp3|mp4|avi|wav|wmv|mkv)$'
        return re.search(file_extension_pattern, path, re.IGNORECASE) is not None