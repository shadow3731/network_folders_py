class Cursor():
    
    def __init__(
        self, 
        init_x = 0, 
        init_y = 0, 
        width = 0, 
        height = 0, 
        padding = 0,
        max_width = 0
    ):
        self.x = init_x
        self.y = init_y
        self.width = width
        self.height = height
        self.padding = padding
        self.max_width = max_width
    
    def place_button(self, button: dict) -> tuple:
        if self.x + int(button['size'])*self.width > self.max_width - self.padding:
            self.x = self.padding
            self.y += self.height - self.padding
            
        button_positions: tuple = (
            self.x + self.padding,
            self.y + 3*self.padding,
            int(button['size'])*self.width + (int(button['size'])-1)*self.padding,
            self.height - 2*self.padding
        )
        
        self.x += int(button['size'])*self.width + self.padding
            
        return button_positions
    
    def place_group(self, lower_y: int) -> tuple:
        group_positions: tuple = (
            self.x,
            self.y,
            self.max_width - 2*self.padding,
            lower_y + self.padding - self.y
        )
        
        self.y = lower_y + self.padding
        
        return group_positions
    
    def move_to_new_group(self):
        self.x = self.padding
        self.y = self.height + 4*self.padding