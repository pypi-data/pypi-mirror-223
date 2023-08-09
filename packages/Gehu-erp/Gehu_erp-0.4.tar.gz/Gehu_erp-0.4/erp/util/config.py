import os
from erp.util import headers
import json

def load_config():
    current_dir = os.path.dirname(__file__)
    config_file_path = os.path.join(current_dir, 'config.json')
    
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
            headers.RequestVerificationToken = config_data.get('RequestVerificationToken')
            headers.SessionId = config_data.get('SessionId')
            return True
    else:
        default_config = {
            'RequestVerificationToken': None,
            'SessionId': None
        }
        with open(config_file_path, 'w') as config_file:
            json.dump(default_config, config_file, indent=4)
        return False


def save_config(sessionId, token):
    current_dir = os.path.dirname(__file__)
    config_file_path = os.path.join(current_dir, 'config.json')
    
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
            config_data['RequestVerificationToken'] = token
            config_data['SessionId'] = sessionId
            
        with open(config_file_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
