import os
import json


class Configurations:

    def get_config(self):
        debug = True
        config = dict()
        if debug:
            with open(os.getcwd() + '/config.json') as file:  # Opening JSON file
                config_file = json.load(file)  # returns JSON object as a dictionary
                config['google_key'] = config_file['configs']['local_key']
                config['access_id'] = config_file['configs']['access_id']
                config['access_key'] = config_file['configs']['access_key']
                config['bucket_name'] = config_file['configs']['bucket_name']
        else:
            config['google_key'] = os.getenv("HEROKU_GOOGLE_API")
            config['access_id'] = os.environ.get("ACCESS_ID")
            config['access_key'] = os.environ.get("ACCESS_KEY")
            config['bucket_name'] = os.environ.get("BUCKET_NAME")
        return config
