import requests
import json


# Fronius Symo/Gn24 devices
class Fronius:
    def __init__(self, config):
        # Demo code for config access
        print(
            f"Fronius device: configured host name is {config['fronius']['host_name']}")

        self.host_name = config['fronius']['host_name']

        # Initialize with values
        self.total_energy_produced_kwh = 0.0
        self.total_energy_consumed_kwh = 0.0
        self.total_energy_fed_in_kwh = 0.0
        self.current_power_produced_kw = 0.0
        self.current_power_consumed_kw = 0.0
        self.current_power_fed_in_kw = 0.0

    def update(self):
        '''Updates all device stats.'''
        powerflow_url = f"http://{self.host_name}/solar_api/v1/GetPowerFlowRealtimeData.fcgi"
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            copy_data(r.json())
        except requests.exceptions.Timeout:
            print(f"Fronius device: Timeout requesting {url}")
        except requests.exceptions.RequestException as e:
            print(f"Fronius device: requests exception {e} for URL {url}")

    def copy_data(data):
        '''Copies the results from the API request.'''
        # Todo
        self.total_energy_produced_kwh = self.total_energy_produced_kwh + 1
        self.total_energy_consumed_kwh = self.total_energy_consumed_kwh + 1
        self.total_energy_fed_in_kwh = self.total_energy_fed_in_kwh + 1
        self.current_power_produced_kw = self.current_power_produced_kw + 1
        self.current_power_consumed_kw = self.current_power_consumed_kw + 1
        self.current_power_fed_in_kw = self.current_power_fed_in_kw + 1
