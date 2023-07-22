import json

from window import Window

def start():
    data = _load_data()
    
    Window().start(data)
    
def _load_data() -> dict:
    try:
        with open('data.json', encoding='utf8') as f:
            return json.load(f)
                
    except OSError as e:
        print(e)

if __name__ == '__main__':
    start()