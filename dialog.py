import tkinter as tk
from tkinter import messagebox as mb

class Dialog():
    
    def __init__(self):
        pass
    
    def show_error(self, message: str):
        mb.showerror(
            title='Ошибка',
            message=message
        )