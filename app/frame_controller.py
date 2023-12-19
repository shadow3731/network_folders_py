import tkinter as tk

class Frame_Controller():
    
    def __init__(self) -> None:
        self.root: tk.Tk = None
    
    def create_root(self):
        self.root = tk.Tk()
        
    def destroy_root(self):
        self.root.destroy()