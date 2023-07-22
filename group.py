import tkinter as tk

class Group():
    
    def __init__(self):
        self.frame = None
        
    def show(self, data: dict):
        groups_data = data['groups']
        
        self._place_groups(groups_data=groups_data)
        
    def _place_groups(self, groups_data: dict):
        index = 0
        
        for v in groups_data.values():
            if isinstance(v, dict):
                index += 1
                
                labelframe = tk.LabelFrame(
                    master=self.frame, 
                    height=int(groups_data['height']),
                    text=groups_data[f'group{index}']['name'],
                    bg=groups_data['bg_color']
                )
                labelframe.pack(
                        anchor=tk.N,
                        fill=tk.X,  
                        padx=int(groups_data['width_diff']), 
                        pady=int(groups_data['height_diff'])
                    )