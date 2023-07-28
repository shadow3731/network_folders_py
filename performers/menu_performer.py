import tkinter as tk
import json

from performers.data_performer import DataPerformer
from performers.window_performer import WindowPerformer
from dialog import Dialog

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
                root=root,
                data=DataPerformer().load_service_data()['appearance_file_path']
            )
        )
        config_file_menu.add_command(
            label='Изменить',
            command=lambda: self._show_win_to_change_text(
                root=root,
                data=DataPerformer().load_appearance_data(
                    filepath=DataPerformer().load_service_data()['appearance_file_path']
                )
            )
        )
        
        return config_file_menu
    
    def _show_win_to_change_entry(
        self, 
        root: tk.Tk, 
        data: str = ''
    ):
        modal_window = tk.Toplevel(root)
        
        WindowPerformer().center_window(modal_window, "400", "60")
        
        modal_window.title('Указать путь к папке с файлом визуализации')
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
            command=lambda: self._save_data(
                root=modal_window, 
                data=entry.get()
            )
        )
        button.pack(side=tk.RIGHT, padx=5)
        
        modal_window.wait_window()
        
    def _show_win_to_change_text(
        self, 
        root: tk.Tk, 
        data: dict = None
    ):
        if data:
            modal_window = tk.Toplevel(root)
            
            WindowPerformer().center_window(modal_window, "650", "500")
            
            modal_window.title('Редактировать файл визуализации')
            self._confugure_window(modal_window, root)
            
            frame = tk.Frame(
                master=modal_window,
                width=modal_window.winfo_screenwidth(),
                height=modal_window.winfo_screenheight()-45
            )
            frame.pack(padx=5, pady=5)
            
            text = tk.Text(
                master=frame, 
                width=78,
                height=28,
                wrap=tk.WORD
            )
            text.insert(1.0, json.dumps(data, ensure_ascii=False, indent=4))
            
            y_scrollbar = tk.Scrollbar(
                master=frame,
                command=text.yview
            )
            
            text.config(yscrollcommand=y_scrollbar.set)
            text.pack(side=tk.LEFT, anchor=tk.NW)
            text.focus_set()
            
            y_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
            
            button = tk.Button(
                master=modal_window, 
                text='Сохранить',
                width=12,
                command=lambda: self._save_data(
                    root=modal_window, 
                    data=text.get(1.0, tk.END),
                    is_entry=False
                )
            )
            button.pack(side=tk.BOTTOM, anchor=tk.E, padx=5, pady=5)
            
            modal_window.wait_window()
        
        else:
            message = 'Укажите путь к файлу визуализации.'
            Dialog().show_error(message)
        
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
        dp = DataPerformer()
        
        if is_entry:
            service_data: dict = dp.load_service_data()
            service_data['appearance_file_path'] = data
            dp.save_service_data(service_data)
            
            root.destroy()
            
        else:
            try:
                dp.save_appearance_data(
                    savabale_data=json.loads(data),
                    filepath=dp.load_service_data()['appearance_file_path']
                )
                
                root.destroy()
                
            except json.JSONDecodeError as e:
                message = f'Не удалось сохранить файл конфигурации. Проверьте синтаксис файла. Возможно присутствует лишний или отсутсвует необходимый знак.\n\n{e}'
                Dialog().show_error(message)
        