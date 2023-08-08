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
        
    def start(self, a_data: dict):
        self.mp.show_menu(self.root)
        
        canvas = tk.Canvas(master=self.root)
        canvas.place(x=0, y=-5, relwidth=1)
        canvas.bind_all(
            '<MouseWheel>', 
            lambda e, canvas=canvas: self._on_mousewheel(e, canvas)
        )
        
        frame = tk.Frame(
            master=canvas, 
            width=canvas.winfo_screenwidth(),
            height=canvas.winfo_screenheight()
        )
        
        root_elements = {
            'root': self.root,
            'canvas': canvas,
            'frame': frame
        }
        
        if a_data and len(a_data) > 0:
            if self._set_cursor_values(a_data):
                buttons_pos = self.bp.configure_buttons(a_data)
            
                if buttons_pos and len(buttons_pos) > 0:
                    if self._set_cursor_values(a_data):
                        groups_pos = self.gp.configure_groups(buttons_pos)
                    
                        self.gp.show_groups(
                            data=a_data, 
                            positions=groups_pos,
                            root=frame
                        )
                        self.bp.show_buttons(
                            data=a_data, 
                            positions=buttons_pos,
                            root=frame
                        )
                    
                        self.wp.show_window(
                            roots=root_elements, 
                            data=a_data, 
                            groups_pos=groups_pos
                        )
                    
                else:
                    self.wp.show_window(roots=root_elements, data=a_data)
            
        else:
            self.wp.show_window(roots=root_elements)
        
        frame.update_idletasks()
        
        canvas.config(scrollregion=(0, 0, frame.winfo_reqwidth(), frame.winfo_reqheight()))
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)
        
        scrollbar = tk.Scrollbar(
            master=self.root, 
            width=self.cursor.right_padding+2,
            command=canvas.yview
        )
        scrollbar.place(relx=1, rely=0, relheight=1, anchor=tk.NE)
        
        canvas.config(yscrollcommand=scrollbar.set)
        
        self.root.mainloop()
        
    def _set_cursor_values(self, data: dict) -> bool:
        try:
            self.cursor.x = data['window']['padding']
            self.cursor.y = data['window']['padding']
            self.cursor.width = data['window']['button_width']
            self.cursor.height = data['window']['button_height']
            self.cursor.padding = data['window']['padding']
            self.cursor.right_padding = data['window']['r_padding']
            self.cursor.screen_width = data['window']['width']
            
            return True
        
        except ValueError as e:
            message = f'Неправильные значения размеров окна. Проверьте файл визуализации.\n\n{e}'
            Dialog().show_error(message)
            
            return False
                
    def _on_mousewheel(self, event, canvas: tk.Canvas):
        canvas.yview_scroll(-1*(event.delta // 120), 'units')