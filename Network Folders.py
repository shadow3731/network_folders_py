from performers.data_performer import DataPerformer
from app import Application

def start():
    dp = DataPerformer()
    service_data: dict = dp.load_service_data()
    if service_data:
        appearance_data: dict = dp.load_appearance_data(
            filepath=service_data['appearance_file_path']
        )
    
        Application().start(service_data, appearance_data)

if __name__ == '__main__':
    start()