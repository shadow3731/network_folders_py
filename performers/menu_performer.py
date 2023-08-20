import tkinter as tk
import json

from performers.data_performer import DataPerformer
from performers.window_performer import WindowPerformer
from dialog import Dialog

class MenuPerformer():
    """The class for toolbar menu handling.
    
    Attributes:
        menu (optional): The toolbar menu object of tkinter.
        dp (DataPerformer): The DataPerformer object for handling the data.
    """
    
    
    def __init__(self, data_performer: DataPerformer):
        """Initializes DataPerformer instance."""
        
        self.menu = None
        self.dp = data_performer
        
    
    def show_menu(self, root: tk.Tk):
        """Shows the toolbar menu.

        Args:
            root (tk.Tk): The root window where the toolbar menu is displayed.
        """
        
        self.menu = tk.Menu(master=root, tearoff=0)
        root.config(menu=self.menu)
        
        options_menu = self._show_options_menu(root)
        
        self.menu.add_cascade(label='Опции', menu=options_menu)
        
    def _show_options_menu(self, root: tk.Tk) -> tk.Menu:
        """Shows inner menu of the main toolbar menu.

        Args:
            root (tk.Tk): The main toolbar menu element.

        Returns:
            tk.Menu: Inner toolbar menu element.
        """
        
        options_menu = tk.Menu(master=root, tearoff=0)
        options_menu.add_cascade(
            label='Файл конфигурации',
            menu=self._show_config_file_menu(options_menu)
        )
        options_menu.add_cascade(
            label='Сетевые учетные данные',
            menu=self._show_cred_settings_menu(options_menu)
        )
        
        return options_menu
    
    def _show_config_file_menu(
        self, 
        master_menu: tk.Menu
    ) -> tk.Menu:
        """Shows specififc options of certain inner menu element.
        
        Perfoms operations for opening built-in dialog window 
        to find the file with appearance data.

        Args:
            master_menu (tk.Menu): The inner menu element.

        Returns:
            tk.Menu: Options of the inner menu element.
        """
        
        config_file_menu = tk.Menu(master=master_menu, tearoff=0)
        config_file_menu.add_command(
            label='Открыть', 
            command=self._open_visual_file
        )
        
        return config_file_menu
    
    def _show_cred_settings_menu(
        self, 
        master_menu: tk.Menu
    ) -> tk.Menu:
        """Shows specififc options of certain inner menu element.
        
        Perfoms operations for opening custom dialog window 
        to print and save network credentials.

        Args:
            master_menu (tk.Menu): The inner menu element.

        Returns:
            tk.Menu: Options of the inner menu element.
        """
        
        config_file_menu = tk.Menu(master=master_menu, tearoff=0)
        config_file_menu.add_command(
            label='Изменить', 
            command=lambda: self._set_network_credentials(master_menu)
        )
        
        return config_file_menu
    
    def _set_network_credentials(self, root: tk.Menu):
        """Sets the network credentials.
        
        Creates Toplevel dialog window with some elements 
        to write and save the network credentials.
        
        If the credentials have been saved before, shows these data.

        Args:
            root (tk.Menu): The toolbar menu element of tkinter.
        """
        
        modal_window = tk.Toplevel(root)
        
        WindowPerformer().center_window(modal_window, 400, 120)
        WindowPerformer().configure_window(modal_window)
        modal_window.title('Изменить сетевые учетные данные')
        modal_window.focus_set()
        
        s_data = self.dp.load_service_data()
        
        label_username = tk.Label(
            master=modal_window,
            text='Имя пользователя'
        )
        label_username.pack(anchor=tk.W, padx=5, pady=(5, 0))
        
        entry_username = tk.Entry(
            master=modal_window,
            width=modal_window.winfo_screenwidth()
        )
        entry_username.insert(0, s_data[self.dp.username_cred_key])
        entry_username.pack(anchor=tk.CENTER, padx=5)
        
        label_password = tk.Label(
            master=modal_window,
            text='Пароль'
        )
        label_password.pack(anchor=tk.W, padx=5)
        
        entry_password = tk.Entry(
            master=modal_window,
            width=modal_window.winfo_screenwidth(),
            show='*'
        )
        entry_password.insert(0, s_data[self.dp.password_cred_key])
        entry_password.pack(anchor=tk.CENTER, padx=5, pady=(0, 5))
        
        button = tk.Button(
            master=modal_window, 
            text='Изменить',
            width=12,
            command=lambda: self._save_network_credentials(
                event=None,
                window=modal_window,
                user=entry_username.get(),
                passw=entry_password.get()
            )
        )
        button.pack(side=tk.RIGHT, padx=5)
        button.bind(
                '<Return>', 
                lambda e, 
                window=modal_window, 
                user=entry_username.get(),
                passw=entry_password.get(): 
                    self._save_network_credentials(e, window, user, passw)
            )
        
        modal_window.wait_window()
        
    def _save_network_credentials(
        self, 
        event, 
        window: tk.Toplevel, 
        user: str, 
        passw: str
    ):
        """Saves the network credentials.
        
        Creates a dictionary and saves them as a part 
        of the service data.

        Args:
            window (tk.Toplevel): The dialog window of credentials.
            user (str): The username of credentials.
            passw (str): The password of credentials.
        """
        
        s_data = self.dp.load_service_data()
        s_data[self.dp.username_cred_key] = user
        s_data[self.dp.password_cred_key] = passw
        
        self.dp.save_service_data(s_data)
        
        window.destroy()
            
    def _open_visual_file(self):
        """Opens the built-in filedialog to find the file 
        with appearance data. If user found it, 
        the application saves it."""
        
        filedir = Dialog().open_file_dialog()
        self._save_file_directory(filedir)
            
    def _save_file_directory(self, dir: str):
        """Saves filedirecory of the appearnace data 
        as a part of the service data.
        
        If the service data exists, performs this action.

        Args:
            dir (str): The directory of the file with the appearance data.
        """
        
        if dir:
            s_data = self.dp.load_service_data()
            if s_data:
                s_data[self.dp.a_data_key] = dir
                self.dp.save_service_data(s_data)