from performers.data_performer import DataPerformer
from app import Application
from converter import Converter

def start(): 
    """Starts the application.
    
    Creates DataPerformer() object and gets service and appearance data.
    The service data is used for backend working of the application,
    the appearance one is used for frontend working.
    
    The appearance data is taken from a JSON-file,
    so it has only string-type values and might have unnecessary keys.
    So that this data is being converting to suitable dictionary,
    that optimizes working of the application.
    After converting, the appearance data is used for visualizing
    the application main window.
    """
    
    dp = DataPerformer()
    service_data = dp.load_service_data()
    if service_data:
        raw_appearance_data = dp.load_appearance_data_from_server(
            filepath=service_data['appearance_file_path']
        )
        
        appearance_data = Converter().return_valid_dictionary(
            raw_appearance_data
        )
        
        Application(dp).start(appearance_data)

if __name__ == '__main__':
    start()