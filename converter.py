class Converter():
    
    def __init__(self):
        pass
    
    def return_valid_dictionary(self, raw_data: dict) -> dict:      
        data = {}
        
        data['app_name'] = 'Network Folders' if not raw_data.get('app_name') else raw_data['app_name']
        
        data['window'] = {} if not raw_data.get('window') else raw_data['window']
        data['window']['width'] = 695 if not raw_data['window'].get('width') else int(raw_data['window']['width'])
        data['window']['padding'] = 5 if not raw_data['window'].get('padding') else int(raw_data['window']['padding'])
        data['window']['r_padding'] = 15 if not raw_data['window'].get('r_padding') else int(raw_data['window']['r_padding'])
        data['window']['button_width'] = 90 if not raw_data['window'].get('button_width') else int(raw_data['window']['button_width'])
        data['window']['button_height'] = 40 if not raw_data['window'].get('button_height') else int(raw_data['window']['button_height'])
        
        data['groups'] = {}
        
        i = 1
        while True:
            if raw_data['groups'].get(f'group{i}'):
                data['groups'][f'group{i}'] = {}
                data['groups'][f'group{i}']['name'] = f'Group {i}' if not raw_data['groups'][f'group{i}'].get('name') else raw_data['groups'][f'group{i}']['name']
                data['groups'][f'group{i}']['buttons'] = {}
                
                j = 1
                while True:
                    if raw_data['groups'][f'group{i}']['buttons'].get(f'button{j}'):
                        data['groups'][f'group{i}']['buttons'][f'button{j}'] = {}
                        data['groups'][f'group{i}']['buttons'][f'button{j}']['name'] = f'Button {j}' if not raw_data['groups'][f'group{i}']['buttons'][f'button{j}'].get('name') else raw_data['groups'][f'group{i}']['buttons'][f'button{j}']['name']
                        data['groups'][f'group{i}']['buttons'][f'button{j}']['path'] = '' if not raw_data['groups'][f'group{i}']['buttons'][f'button{j}'].get('path') else raw_data['groups'][f'group{i}']['buttons'][f'button{j}']['path']
                        data['groups'][f'group{i}']['buttons'][f'button{j}']['size'] = 1 if not raw_data['groups'][f'group{i}']['buttons'][f'button{j}'].get('size') else int(raw_data['groups'][f'group{i}']['buttons'][f'button{j}']['size'])
                        data['groups'][f'group{i}']['buttons'][f'button{j}']['bg_color'] = 'white' if not raw_data['groups'][f'group{i}']['buttons'][f'button{j}'].get('bg_color') else raw_data['groups'][f'group{i}']['buttons'][f'button{j}']['bg_color']
                        data['groups'][f'group{i}']['buttons'][f'button{j}']['fg_color'] = 'black' if not raw_data['groups'][f'group{i}']['buttons'][f'button{j}'].get('fg_color') else raw_data['groups'][f'group{i}']['buttons'][f'button{j}']['fg_color']
                        
                        j += 1
                        
                    else:
                        break
                
                i += 1
                   
            else:
                break
        
        return data