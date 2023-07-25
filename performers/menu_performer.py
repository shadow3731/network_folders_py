import tkinter as tk

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
            menu=self._show_config_file_menu(options_menu)
        )
        options_menu.add_command(label='Изменить пароль')
        
        return options_menu
    
    def _show_config_file_menu(self, root: tk.Menu) -> tk.Menu:
        config_file_menu = tk.Menu(master=root, tearoff=0)
        config_file_menu.add_command(label='Указать путь')
        config_file_menu.add_command(label='Изменить')
        
        return config_file_menu