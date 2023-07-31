import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog as fd

import json

class Dialog():
    
    def __init__(self):
        pass
    
    def show_error(self, message: str):
        mb.showerror(
            title='Ошибка',
            message=message
        )
        
    def save_file_dialog(self) -> str:
        file = fd.asksaveasfile(
            title='Создать файл визуализации',
            defaultextension='.json',
            filetypes=[('JSON файлы', '*.json'), ('Все файлы', '*.*')]
        )
        if file:
            if file.name.endswith('.json'):
                with open(file.name, 'w', encoding='utf8'):
                    json.dump('{}', file)
                    return file.name
                
            else:
                message = "Файл визуализации должен иметь расширение .json."
                self.show_error(message)
                return None
                
        return None
    
    def open_file_dialog(self) -> str:
        file = fd.askopenfile(
            title='Открыть файл визуализации',
            defaultextension='.json',
            filetypes=[('JSON файлы', '*.json'), ('Все файлы', '*.*')]
        )
        if file:
            if file.name.endswith('.json'):
                return file.name
                
            else:
                message = "Файл визуализации должен иметь расширение .json."
                self.show_error(message)
                return None
                
        return None