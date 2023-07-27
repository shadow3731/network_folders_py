import tkinter as tk

from performers.data_performer import DataPerformer
from performers.window_performer import WindowPerformer

class MenuPerformer():
    
    def __init__(self):
        self.menu = None
    
    def show_menu(self, root: tk.Tk):
        self.menu = tk.Menu(master=root, tearoff=0)
        root.config(menu=self.menu)
        
        options_menu = self._show_options_menu(root)
        
        self.menu.add_cascade(label='Опции', menu=options_menu)
        
    def _show_options_menu(self, root: tk.Tk) -> tk.Menu:
        options_menu = tk.Menu(master=root, tearoff=0)
        options_menu.add_cascade(
            label='Файл конфигурации',
            menu=self._show_config_file_menu(options_menu, root)
        )
        options_menu.add_command(label='Изменить пароль')
        
        return options_menu
    
    def _show_config_file_menu(
        self, 
        master_menu: tk.Menu, 
        root: tk.Menu
    ) -> tk.Menu:
        config_file_menu = tk.Menu(master=master_menu, tearoff=0)
        config_file_menu.add_command(
            label='Указать путь', 
            command=lambda: self._show_win_to_change_entry(
                root,
                DataPerformer().load_service_data()['path']
            )
        )
        config_file_menu.add_command(label='Изменить')
        
        return config_file_menu
    
    def _show_win_to_change_entry(
        self, 
        root: tk.Tk, 
        data: str = ''
    ):
        modal_window = tk.Toplevel(root)
        
        WindowPerformer().center_window(modal_window, "400", "60")
        
        modal_window.title('Указать путь к файлу визуализации')
        self._confugure_window(modal_window, root)
        
        entry = tk.Entry(
            master=modal_window,
            width=modal_window.winfo_screenwidth()
        )
        entry.insert(0, data)
        entry.pack(anchor=tk.CENTER, padx=5, pady=5)
        entry.focus_set()
        
        button = tk.Button(
            master=modal_window, 
            text='Сохранить',
            width=12,
            command=lambda: self._save_data(modal_window, entry.get())
        )
        button.pack(side=tk.RIGHT, padx=5)
        
        modal_window.wait_window()
        
    def _confugure_window(self, window: tk.Toplevel, root: tk.Tk):
        window.resizable(width=False, height=False)
        window.iconbitmap('')
        window.attributes('-toolwindow', 1)
        window.transient(root)
        
    def _save_data(
        self, 
        root: tk.Toplevel, 
        data: str, 
        is_entry: bool = True
    ):
        if is_entry:
            dp = DataPerformer()
            
            service_data: dict = dp.load_service_data()
            service_data['path'] = data
            dp.save_service_data(service_data)
            
        root.destroy()
        