from performers.data_performer import DataPerformer
from app import Application

def start():
    dp = DataPerformer()
    service_data: dict = dp.load_service_data()
    appearance_data: dict = dp.load_appearance_data(service_data['path'])
    
    Application().start(service_data, appearance_data)

if __name__ == '__main__':
    start()