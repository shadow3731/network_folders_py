import sys, os

import tkinter as tk

from dialog import Dialog

class WindowPerformer():
    
    def __init__(self):
        pass
    
    def show_window(self, roots: dict, data: dict = None, groups_pos: list = None):
        roots['root'].title(data['app_name'])
        roots['root'].iconbitmap(self._get_icon_path('network_folders_py/icon.ico'))
        roots['root'].resizable(width=False, height=False)
        
        window_width = 500
        window_height = 0
        widgets_height = 0
        
        try:
            window_width = data['window']['width']
            window_padding = data['window']['padding']
                        
        except ValueError as e:
            message = f'Неправильные значения размеров окна. Проверьте файл визуализации.\n\n{e}'
            Dialog().show_error(message)
                
            window_width = 680
            window_padding = 5
        
        if groups_pos and len(groups_pos) > 0:
            window_height = groups_pos[-1][1] + groups_pos[-1][-1] + window_padding
            widgets_height = window_height
                
            if window_height > 570:
                window_height = 570
                
            else:
                window_height = 0
                
        self._congigure_roots(roots, widgets_height)
            
        self.center_window(
            root=roots['root'],
            width=window_width,
            height=window_height
        )
        
    def center_window(self, root: tk.Tk, width: int, height: int):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        x_offset = (screen_width - width) // 2
        y_offset = (screen_height - height) // 2
        
        root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
        
    def configure_window(self, window: tk.Tk, root: tk.Tk):
        window.resizable(width=False, height=False)
        window.iconbitmap('')
        window.attributes('-toolwindow', 1)
        window.transient(root)
        
    def _congigure_roots(self, roots: dict, height: int):
        roots['frame'].config(height=height)
        roots['canvas'].config(height=height)
        
    def _get_icon_path(self, rel_path) -> str:
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath('.')
            
        return os.path.join(base_path, rel_path)