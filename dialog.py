import os

from tkinter import messagebox as mb
from tkinter import filedialog as fd

class Dialog():
    """The class for working with dialog windows."""
    
    def __init__(self):
        pass
    
    def show_error(self, message: str):
        """Shows the 'askerror' dialog window with certain message.
        
        Args:
            message (str): Error message to be shown.
        """
        
        mb.showerror(
            title='Ошибка',
            message=message
        )
    
    def open_file_dialog(self) -> str:
        """Opens bult-in file dialog window 
        to find a file with some data.
        
        Only JSON-files are suitable to open, 
        because it is supposed that the data 
        must be contained in this type of files.
        
        If a user opened file of another type, 
        shows the 'askerror' window with error description.
        
        In case of safety, the default directory of file dialog 
        is user's desktop.
        
        Returns:
            str: File name of the JSON-file with the data.
        """
        
        file = fd.askopenfile(
            title='Открыть файл визуализации',
            initialdir=os.path.expanduser('~/Desktop'),
            defaultextension='.json',
            filetypes=[('JSON файлы', '*.json'), ('Все файлы', '*.*')]
        )
        if file:
            if file.name.endswith('.json'):
                return file.name
                
            else:
                message = "Файл визуализации должен иметь расширение .json."
                self.show_error(message)
                
                return None
                
        return None