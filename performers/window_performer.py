import tkinter as tk

class WindowPerformer():
    
    def __init__(self):
        pass
    
    def show_window(self, root: tk.Tk, data: dict = None, groups_pos: list = None):
        window_width = "500"
        window_height = "0"
        
        if data:
            root.title(data['app_name'])
            
            window_width = data['window']['width']
        
            if groups_pos and len(groups_pos) > 0:
                window_height = groups_pos[-1][1] + groups_pos[-1][-1] + int(data['window']['padding'])
            else:
                window_height = "0"
            
        self.center_window(
            root=root,
            width=window_width,
            height=window_height
        )
        
        root.title('Network Folders')
        root.iconbitmap(default='files/icon.ico')
        root.resizable(width=False, height=False)
        
    def center_window(self, root: tk.Tk, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        x_offset = (screen_width - int(width)) // 2
        y_offset = (screen_height - int(height)) // 2
        
        root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")