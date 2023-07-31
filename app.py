import tkinter as tk

from cursor import Cursor
from dialog import Dialog
from performers.window_performer import WindowPerformer
from performers.menu_performer import MenuPerformer
from performers.groups_performer import GroupsPerformer
from performers.buttons_performer import ButtonsPerformer

class Application():
    
    def __init__(self):
        self.root = tk.Tk()
        self.cursor = Cursor()
        self.wp = WindowPerformer()
        self.mp = MenuPerformer()
        self.gp = GroupsPerformer(self.cursor)
        self.bp = ButtonsPerformer(self.cursor)
        
    def start(self, s_data: dict, a_data: dict):
        self.mp.show_menu(self.root)
        
        if a_data:
            self._set_cursor_values(a_data)
            buttons_pos = self.bp.configure_buttons(a_data)
            
            if buttons_pos and len(buttons_pos) > 0:
                self._set_cursor_values(a_data)
                groups_pos = self.gp.configure_groups(buttons_pos)
            
                self.gp.show_groups(
                    data=a_data, 
                    positions=groups_pos,
                    root=self.root
                )
                self.bp.show_buttons(
                    data=a_data, 
                    positions=buttons_pos,
                    root=self.root
                )
            
                self.wp.show_window(
                    root=self.root, 
                    data=a_data, 
                    groups_pos=groups_pos
                )
                
            else:
                self.wp.show_window(root=self.root, data=a_data)
            
        else:
            self.wp.show_window(root=self.root)
            
        self.root.mainloop()
        
    def _set_cursor_values(self, data: dict):
        self.cursor.x = 5
        self.cursor.y = 5
        self.cursor.width = 90
        self.cursor.height = 40
        self.cursor.padding = 5
        self.cursor.screen_width = 680
        
        if isinstance(data, dict) and data.get('window') and isinstance(data['window'], dict):
            try:
                if data['window'].get('padding'):
                    self.cursor.x = int(data['window']['padding'])
                    self.cursor.y = int(data['window']['padding'])
                    self.cursor.padding = int(data['window']['padding'])
                    
                if data['window'].get('button_width'):
                    self.cursor.width = int(data['window']['button_width'])
                    
                if data['window'].get('button_height'):
                    self.cursor.height = int(data['window']['button_height'])
                    
                if data['window'].get('width'):
                    self.cursor.screen_width = int(data['window']['width'])
            
            except ValueError as e:
                message = f'Неправильные значения размеров окна. Проверьте файл визуализации.\n\n{e}'
                Dialog().show_error(message)