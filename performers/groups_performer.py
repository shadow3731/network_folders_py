import tkinter as tk
from tkinter.font import Font

from cursor import Cursor

class GroupsPerformer():
    
    def __init__(self, cursor: Cursor):
        self.cursor = cursor
        
    def configure_groups(self, buttons_pos: list) -> list:
        positions: list = []
        
        for i in range(len(buttons_pos)):
            lower_y = buttons_pos[i][-1][1] + buttons_pos[i][-1][3]
            positions.append(self.cursor.place_group(lower_y))
            
        return positions
    
    def show_groups(self, data: dict, positions: list, root: tk.Tk):
        for i in range(len(positions)):
            group_data: dict = data['groups'][f'group{i+1}']
            
            tk.LabelFrame(
                master=root,
                text=group_data['name'],
                font=Font(family='Calibri', size=11, weight='bold')
            ).place(
                x=positions[i][0],
                y=positions[i][1],
                width=positions[i][2],
                height=positions[i][3]
            )