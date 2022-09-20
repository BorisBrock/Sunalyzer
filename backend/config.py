import yaml
import traceback
import logging


class Config:
    def __init__(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                self.config_data = yaml.safe_load(file)
                self.load_settings(self.config_data)
        except Exception as e:
            logging.error("Config error: "
                          "loading/parsing the configuration file failed")
            logging.error(e)
            traceback.print_exc()
            exit()

    def load_settings(self, yaml_data):
        '''Copy settings from the yaml data for easier access.'''
        # Logging
        self.log_level = logging.INFO
        if self.config_data['logging'] == 'verbose':
            logging.info("Verbose logging is enabled")
            self.log_level = logging.DEBUG
