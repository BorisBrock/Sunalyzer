import yaml
import traceback


class Config:
    def __init__(self, file_name):
        try:
            with open(file_name, "r", encoding="utf-8") as file:
                self.config_data = yaml.safe_load(file)
                self.load_settings(self.config_data)
        except Exception as e:
            print("""Config error:
                loading/parsing the configuration file failed""")
            print(e)
            traceback.print_exc()
            exit()

    def load_settings(self, yaml_data):
        '''Copy settings from the yaml data for easier access.'''
        # Logging
        self.verbose_logging = False
        if self.config_data['logging'] == 'verbose':
            print("Verbose logging is enabled")
            self.verbose_logging = True
