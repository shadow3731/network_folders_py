import tkinter as tk
from tkinter.font import Font

import os, subprocess, platform, threading, shlex

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
            map_cmd = f'net use "{dir}" /user:"{creds["username"]}" "{creds["password"]}"'
            expl_cmd = f'explorer "{dir}"'
            disconn_cmd = f'net use "{dir}" /delete'
            
            map_cmd_res, expl_cmd_res = None, None
            
            try:
                map_cmd_res = subprocess.run(map_cmd, shell=True, check=True)
                
                if map_cmd_res.returncode == 0:
                    expl_cmd_res = subprocess.run(expl_cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                    subprocess.run(disconn_cmd, shell=True, check=True)
            
            except subprocess.CalledProcessError as e:
                if e.returncode == 1:
                    disconn_cmd = f'net use "{dir}" /delete'
                    subprocess.run(disconn_cmd, shell=True, check=True)
                
                else:
                    msg_cmd = f'net helpmsg {e.returncode}'
                    msg_cmd_res = subprocess.run(msg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        
                    try:
                        message = f'При подключении к директории {dir} произошла ошибка с кодом {e.returncode}.\n\n{msg_cmd_res.stdout.decode("utf-8").strip()}\n\n'
                        Dialog().show_error(message)
                                
                    except UnicodeDecodeError:
                        message = f'При подключении к директории {dir} произошла ошибка с кодом {e.returncode}.\n\n{msg_cmd_res.stdout.decode("ibm866").strip()}\n\n'
                        Dialog().show_error(message)
        
        else:
            try:
                subprocess.run(f'echo "{creds["password"]}" | sudo -S open "{dir}"')
                
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