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
        raw_appearance_data = dp.load_data_from_server(
            filepath=service_data[dp.a_data_key]
        )
        appearance_data = Converter().return_valid_dictionary(
            raw_appearance_data
        )
        
        if service_data[dp.creds_import_mode_key] == 'True':
            credentials_data = dp.load_data_from_server(
                filepath=service_data[dp.c_data_key]
            )
            
            if credentials_data:
                service_data[dp.username_cred_key] = credentials_data['username']
                service_data[dp.password_cred_key] = credentials_data['password']
                
                dp.save_service_data(service_data)
            
        
        Application(dp).start(appearance_data)

if __name__ == '__main__':
    start()