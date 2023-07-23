import tkinter as tk
from tkinter.font import Font

from cursor import Cursor

class ButtonsPerformer():
    
    def __init__(self, cursor: Cursor):
        self.cursor = cursor
    
    def configure_buttons(self, data: dict) -> list:
        positions: list = []
        
        groups_data: dict = data['groups']
        group_index = 0
        
        while True:
            group_index += 1
            
            if groups_data.get(f'group{group_index}'):
                buttons_data: dict = groups_data[f'group{group_index}']['buttons']
                button_index = 0
                positions.append([])
                
                while True:
                    button_index += 1
                    
                    if buttons_data.get(f'button{button_index}'):               
                        positions[group_index-1].append(
                            self.cursor.place_button(
                                buttons_data[f'button{button_index}']
                            )
                        )
                    
                    else:
                        self.cursor.move_to_new_group()  
                        break
            else:
                return positions
            
    def show_buttons(self, data: dict, positions: list, root: tk.Tk):
        for i in range(len(positions)):
            group_data: dict = data['groups'][f'group{i+1}']
            
            for j in range(len(positions[i])):
                button_data = group_data['buttons'][f'button{j+1}']
                
                tk.Button(
                    master=root,
                    text=button_data['name'],
                    font=Font(family='Calibri', size=11, weight='bold')
                ).place(
                    x=positions[i][j][0],
                    y=positions[i][j][1],
                    width=positions[i][j][2],
                    height=positions[i][j][3]
                )