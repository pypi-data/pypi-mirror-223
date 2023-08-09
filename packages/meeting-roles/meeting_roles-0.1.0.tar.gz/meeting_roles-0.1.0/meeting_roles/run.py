import os
import uvicorn
import configparser

current_directory = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_directory, 'config.ini')
config = configparser.ConfigParser()
config.read(config_file_path)

port = int(config['server']['port'])
reload = config['server']['reload'] == 'True'


def main():
    uvicorn.run("meeting_roles.app:app", host="0.0.0.0", port=port, reload=True)
