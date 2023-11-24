import tkinter as tk

from cursor import Cursor
from dialog import Dialog
from performers.window_performer import WindowPerformer
from performers.menu_performer import MenuPerformer
from performers.groups_performer import GroupsPerformer
from performers.buttons_performer import ButtonsPerformer
from performers.data_performer import DataPerformer

class Application():
    """The class for application control.
    
    Attributes:
        root (tk.Tk): The root element of the application.
        cursor (Cursor): The Cursor object for placing object on the window.
        wp (WindowPerformer): The WindowPerformer object for a window control.
        mp (MenuPerformer): The MenuPerformer object for a tool menu control.
        gp (GroupsPerformer): The GroupsPerformer object for groups control.
        bp (ButtonsPerformer): The ButtonsPerformer object for buttons control.
    """
    
    def __init__(self, dp: DataPerformer):
        """Initializes Application instance.
        
        Args:
            data_performer (DataPerformer): The DataPerformer object for service and application data control.
        """
        
        self.root = tk.Tk()
        self.cursor = Cursor()
        self.wp = WindowPerformer()
        self.mp = MenuPerformer(dp, self.wp)
        self.gp = GroupsPerformer(self.cursor)
        self.bp = ButtonsPerformer(self.cursor, dp)
        
    def start(self, a_data: dict):
        """Starts the sequence of operations to launch the application.
        
        Firstly shows tool menu bar, then creates field for displaying
        groups and buttons with ceratain parameters.
        If there is the application data, set initial Cursor values,
        calculates positions of buttons and groups and displays them 
        (if they exists). After this configures main window parameters 
        and creates a scroll bar for scrolling the window
        if there are too much buttons. Then shows the main window to a user.
        
        Args:
            a_data (dict): The application data.
        """
        
        self.mp.show_menu(self.root)
        
        canvas = tk.Canvas(master=self.root)
        canvas.place(x=0, y=-5, relwidth=1, relheight=1)
        
        frame = tk.Frame(
            master=canvas, 
            width=canvas.winfo_screenwidth(),
            height=canvas.winfo_screenheight()
        )
        
        self.wp.bind_scrolling(canvas)
        
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
        """Sets certain values for Cursor.
        
        The values are taken from the application data.
        If there is any invalid value, shows 'askerror' window 
        with error description.
        
        Args:
            data (dict): The application data.
            
        Returns:
            bool (True): If all data are correctly set.
            bool (False): If not.
        """
        
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