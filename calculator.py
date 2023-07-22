class Calculator():
    
    def __init__(self):
        pass
    
    def calculate_positions(self, data: dict) -> dict:
        max_groups_width = int(data['window']['width']) - 2 * int(data['groups']['width_diff'])
        max_buttons_width = max_groups_width - 2 * int(data['groups']['width_diff'])
        
        