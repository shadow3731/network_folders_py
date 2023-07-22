import tkinter as tk
from tkinter import ttk

import json

from group import Group

class Window():
    
    def __init__(self):
        self.root = tk.Tk()
        self.group = Group()
        
    def start(self, data: dict):
        self._show_groups(data)
        self._show_window(data)
        self.root.mainloop()
        
    def _configure_buttons(self, data: dict): 
    
        
    def _show_groups(self, data: dict):
        groups_data = data['groups']
        
        tk.LabelFrame(
            master=self.root, 
            text=groups_data['group1']['name']
        ).place(
            x=int(data['window']['padding']),
            y=int(data['window']['padding']),
            width=int(data['window']['width']) - 2 * int(data['window']['padding']),
            height=int(data['window']['button_height']) + 4 * int(data['window']['padding']),
        )
        
    def _show_window(self, data: dict):
        self.root.title(data['app_name'])
        self.root.iconbitmap(default=data['app_icon'])
        self.root.resizable(width=False, height=False)
        
        self._center_window(
            width=data['window']['width'],
            height=data['window']['height']
        )
    
        
        
        
    def _show(self):
        data = self._load_data()
        
        self._configure_window(data)
        self.group.show(data)
            
    def _load_data(self) -> dict:
        try:
            with open('data.json', encoding='utf8') as f:
                return json.load(f)
                
        except OSError as e:
            print(e)
            
    def _configure_window(self, data: dict):
        self.root.title(data['app_name'])
        self.root.iconbitmap(default=data['app_icon'])
        self.root.resizable(width=False, height=False)
        self.root.maxsize(
            width=data['window']['width'],
            height=self.root.winfo_screenheight()
        )
        self._center_window(
            width=data['window']['width'],
            height=data['window']['height']
        )
        
        self._set_frame(bg=data['window']['bg_color'])
        
    def _center_window(self, width="800", height="100"):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x_offset = (screen_width - int(width)) // 2
        y_offset = (screen_height - int(height)) // 2
        
        self.root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
        
    def _set_frame(self, bg="white"):
        frame = tk.Frame(master=self.root, bg=bg)
        frame.pack(fill=tk.BOTH, expand=True)
        
        separator = ttk.Separator(master=frame, orient="horizontal")
        separator.pack(side="top", fill='x')
        
        self.group.frame = frame