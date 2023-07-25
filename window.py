import tkinter as tk
from tkinter import ttk

from cursor import Cursor
from performers.menu_performer import MenuPerformer
from performers.groups_performer import GroupsPerformer
from performers.buttons_performer import ButtonsPerformer

class Window():
    
    def __init__(self):
        self.root = tk.Tk()
        self.cursor = Cursor()
        self.mp = MenuPerformer()
        self.gp = GroupsPerformer(self.cursor)
        self.bp = ButtonsPerformer(self.cursor)
        
    def start(self, data: dict):
        self.mp.show_menu(self.root)
        
        self._set_calculator_values(data)
        buttons_pos = self.bp.configure_buttons(data)
        
        self._set_calculator_values(data)
        groups_pos = self.gp.configure_groups(buttons_pos)
        
        self.gp.show_groups(
            data=data, 
            positions=groups_pos,
            root=self.root
        )
        self.bp.show_buttons(
            data=data, 
            positions=buttons_pos,
            root=self.root
        )
        
        self._show_window(data, groups_pos)
        self.root.mainloop()
        
    def _set_calculator_values(self, data: dict):
        self.cursor.x = int(data['window']['padding'])
        self.cursor.y = int(data['window']['padding'])
        self.cursor.width = int(data['window']['button_width'])
        self.cursor.height = int(data['window']['button_height'])
        self.cursor.padding = int(data['window']['padding'])
        self.cursor.max_width = int(data['window']['width'])
        
    def _show_window(self, data: dict, groups_pos: list):
        self.root.title(data['app_name'])
        self.root.iconbitmap(default=data['app_icon'])
        self.root.resizable(width=False, height=False)
        
        window_height = groups_pos[-1][1] + groups_pos[-1][-1] + int(data['window']['padding'])
        self._center_window(
            width=data['window']['width'],
            height=window_height
        )
        
    def _center_window(self, width="300", height="300"):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x_offset = (screen_width - int(width)) // 2
        y_offset = (screen_height - int(height)) // 2
        
        self.root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")