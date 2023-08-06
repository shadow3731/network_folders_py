from performers.data_performer import DataPerformer
from app import Application

def start():
    dp = DataPerformer()
    service_data = dp.load_service_data()
    if service_data:
        appearance_data = dp.load_appearance_data_from_server(
            filepath=service_data['appearance_file_path']
        )
        
        Application().start(appearance_data)

if __name__ == '__main__':
    start()