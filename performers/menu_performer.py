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
        # self.menu.add_cascade(label='Справка')
        
    def _show_options_menu(self, root: tk.Tk) -> tk.Menu:
        options_menu = tk.Menu(master=root, tearoff=0)
        options_menu.add_cascade(
            label='Файл конфигурации',
            menu=self._show_config_file_menu(options_menu, root)
        )
        # options_menu.add_command(
        #     label='Изменить пароль',
        #     command=lambda: self._set_new_password(root)
        # )
        
        return options_menu
    
    def _show_config_file_menu(
        self, 
        master_menu: tk.Menu, 
        root: tk.Tk
    ) -> tk.Menu:
        config_file_menu = tk.Menu(master=master_menu, tearoff=0)
        # config_file_menu.add_command(
        #     label='Создать',
        #     command=self._create_visual_file
        # )
        config_file_menu.add_command(
            label='Открыть', 
            command=self._open_visual_file
        )
        # dp = DataPerformer()
        # config_file_menu.add_command(
        #     label='Изменить',
        #     command=lambda: self._edit_visual_file(
        #         root=root,
        #         data=dp.load_appearance_data(
        #             filepath=dp.load_service_data()[dp.a_data_key]
        #         )
        #     )
        # )
        
        return config_file_menu
    
    # def _set_new_password(self, root: tk.Menu) -> bool: 
    #     modal_window = tk.Toplevel(root)
        
    #     WindowPerformer().center_window(modal_window, 400, 60)
    #     WindowPerformer().configure_window(modal_window, root)
    #     modal_window.title('Введите новый пароль')
        
    #     entry = tk.Entry(
    #         master=modal_window,
    #         width=modal_window.winfo_screenwidth(),
    #         show='*'
    #     )
    #     entry.pack(anchor=tk.CENTER, padx=5, pady=5)
    #     entry.focus_set()
        
    #     button = tk.Button(
    #         master=modal_window, 
    #         text='Сохранить',
    #         width=12,
    #         command=lambda: self._save_new_password(
    #             window=modal_window,
    #             password=entry.get()
    #         )
    #     )
    #     button.pack(side=tk.RIGHT, padx=5)
        
    #     modal_window.wait_window()
        
    # def _save_new_password(self, window: tk.Toplevel, password: str):
    #     window.destroy()
    #     DataPerformer().save_password(password)
    
    def _create_visual_file(self):
        filedir = Dialog().save_file_dialog()
        self._save_file_directory(filedir)
            
    def _open_visual_file(self):
        filedir = Dialog().open_file_dialog()
        self._save_file_directory(filedir)
        
    def _edit_visual_file(self, root: tk.Menu, data: dict):
        if data:
            modal_window = tk.Toplevel(root)
            
            WindowPerformer().center_window(modal_window, 650, 500)
            WindowPerformer().configure_window(modal_window, root)
            modal_window.title('Редактировать файл визуализации')
            
            upper_frame = tk.Frame(
                master=modal_window,
                width=modal_window.winfo_screenwidth(),
                height=modal_window.winfo_screenheight()-45
            )
            upper_frame.pack(padx=5, pady=(5, 0))
            
            lower_frame = tk.Frame(
                master=modal_window,
                width=modal_window.winfo_screenwidth(),
                height=modal_window.winfo_screenheight() - modal_window.winfo_screenheight()-45
            )
            lower_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
            
            text = tk.Text(
                master=upper_frame, 
                width=78,
                height=28,
                wrap=tk.WORD
            )
            text.insert(1.0, json.dumps(data, ensure_ascii=False, indent=4))
            
            y_scrollbar = tk.Scrollbar(
                master=upper_frame,
                command=text.yview
            )
            
            text.config(yscrollcommand=y_scrollbar.set)
            text.pack(side=tk.LEFT, anchor=tk.NW)
            text.focus_set()
            
            label = tk.Label(
                master=lower_frame, 
                text='Строка: 0, символ: 0'
            )
            label.pack(side=tk.LEFT, padx=5, pady=5)
            
            text.bind(
                '<KeyRelease>', 
                lambda e, text=text, label=label: 
                    self._show_cursor_position(e, text, label)
            )
            
            text.bind(
                '<ButtonRelease-1>', 
                lambda e, text=text, label=label: 
                    self._show_cursor_position(e, text, label)
            )
            
            y_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
            
            button = tk.Button(
                master=lower_frame, 
                text='Сохранить',
                width=12,
                command=lambda: self._save_visual_data(
                    root=modal_window, 
                    data=text.get(1.0, tk.END)
                )
            )
            button.pack(side=tk.RIGHT, padx=5, pady=5)
            
            modal_window.wait_window()
        
        else:
            message = 'Укажите путь к файлу визуализации.'
            Dialog().show_error(message)
            
    def _save_file_directory(self, dir: str):
        if dir:
            dp = DataPerformer()
            service_data = dp.load_service_data()
            if service_data:
                service_data[dp.a_data_key] = dir
                dp.save_service_data(service_data)
        
    def _save_visual_data(self, root: tk.Toplevel, data: str):
        dp = DataPerformer()
        try:
            dp.save_appearance_data(
                savabale_data=json.loads(data),
                filepath=dp.load_service_data()[dp.a_data_key]
            )
                
            root.destroy()
                
        except json.JSONDecodeError as e:
            message = f'Не удалось сохранить файл конфигурации. Проверьте синтаксис файла. Возможно присутствует лишний или отсутсвует необходимый знак.\n\n{e}'
            Dialog().show_error(message)
            
    def _show_cursor_position(
        self, 
        event, 
        text: tk.Text, 
        label: tk.Label
    ):
        cursor = text.index(tk.INSERT)
        r, c = map(int, cursor.split('.'))
        label.config(text=f'Строка: {r}, символ: {c}')
        