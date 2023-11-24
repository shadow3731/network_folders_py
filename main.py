from performers.data_performer import DataPerformer
from app import Application
from converter import Converter

def start(): 
    """Starts the application.
    
    Creates DataPerformer() object and gets service and application data.
    The service data is used for only backend working of the application,
    the application one is used for both backend and frontend working.
    
    The application data is taken from a JSON-file,
    so it has only string-type values and might have unnecessary keys.
    So that this data is being converted to a suitable dictionary,
    that optimizes working of the application.
    
    After converting, the application data is used for visualizing
    the application main window and for saving network credentials.
    If credentials data are updatable, gets credentials from the 
    application data and rewrites them to the service data.
    """
    
    dp = DataPerformer()
    service_data = dp.load_service_data()
    if service_data:
        raw_data = dp.load_data_from_server(service_data[dp.a_data_key])
        formatted_data = Converter().return_valid_dictionary(raw_data)
        
        if service_data[dp.creds_import_mode_key] == 'True':
            if formatted_data['credentials']:
                service_data[dp.username_cred_key] = formatted_data['credentials']['username']
                service_data[dp.password_cred_key] = formatted_data['credentials']['password']
                
                dp.save_service_data(service_data)
            
        
        Application(dp).start(formatted_data)

if __name__ == '__main__':
    start()