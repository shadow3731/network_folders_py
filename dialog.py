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
            title='Создать',
            defaultextension='.json',
            filetypes=[('JSON файлы', '*.json'), ('Все файлы', '*.*')]
        )
        if file:
            if file.name.endswith('.json'):
                with open(file.name, 'w', encoding='utf8'):
                    json.dump({}, file)
                    return file.name
                
            else:
                message = "Файл визуализации должен иметь расширение .json."
                self.show_error(message)
                return None
                
        return None
        
    def open_filedialog(self) -> dict:
        try:
            filename = fd.askopenfile(
                title='Открыть файл визуализации',
                filetypes=(('JSON files', '*.json'))
            )
            with open(filename, encoding='utf8') as f:
                return f.read()
            
        except json.JSONDecodeError as e:
            message = 'Не удалось открыть файл визуализации. Возможно файл имеет несоответствующий тип либо в файле имеются синтаксические ошибки.\n\n{e}'
            self.show_error(message)
            return None