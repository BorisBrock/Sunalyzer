# import json
import requests


# Fronius Symo/Gn24 devices
class Fronius:
    def __init__(self, config):
        # Demo code for config access
        print(f"""Fronius device:
            configured host name is {config['fronius']['host_name']}""")

        self.host_name = config['fronius']['host_name']

        self.url_inverter = (f"http://{self.host_name}/solar_api/v1/GetPowerFlowRealtimeData.fcgi")
        self.url_meter = (f"http://{self.host_name}/solar_api/v1/GetMeterRealtimeData.cgi?Scope=System")

        # Initialize with values
        self.total_energy_produced_kwh = 0.0
        self.total_energy_consumed_kwh = 0.0
        self.total_energy_fed_in_kwh = 0.0
        self.current_power_produced_kw = 0.0
        self.current_power_consumed_kw = 0.0
        self.current_power_fed_in_kw = 0.0

    def copy_data(self, inverter_data, meter_data):
        '''Copies the results from the API request.'''
        # Inverter data
        strTotalProduced = inverter_data["Body"]["Data"]["Site"]["E_Total"]
        totalProduced = float(strTotalProduced)
        # Meter data
        strConsumedFromGrid = meter_data["Body"]["Data"]["0"]["EnergyReal_WAC_Plus_Absolute"]
        consumedFromGrid = float(strConsumedFromGrid)
        strFedIn = meter_data["Body"]["Data"]["0"]["EnergyReal_WAC_Minus_Absolute"]
        fedIn = float(strFedIn)

        TODO

        # Todo
        self.total_energy_produced_kwh = self.total_energy_produced_kwh + 1
        self.total_energy_consumed_kwh = self.total_energy_consumed_kwh + 1
        self.total_energy_fed_in_kwh = self.total_energy_fed_in_kwh + 1
        self.current_power_produced_kw = self.current_power_produced_kw + 1
        self.current_power_consumed_kw = self.current_power_consumed_kw + 1
        self.current_power_fed_in_kw = self.current_power_fed_in_kw + 1

    def update(self):
        '''Updates all device stats.'''
        try:
            # Query inverter data
            r_inverter = requests.get(self.url_inverter, timeout=10)
            r_inverter.raise_for_status()
            # Query smart meter data
            r_meter = requests.get(self.url_meter, timeout=10)
            r_meter.raise_for_status()
            # Extract and process relevant data
            self.copy_data(r_inverter.json(), r_meter.json())
        except requests.exceptions.Timeout:
            print(f"Fronius device: Timeout requesting {self.url}")
        except requests.exceptions.RequestException as e:
            print(f"Fronius device: requests exception {e} for URL {self.url}")
