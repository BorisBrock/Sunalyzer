# import json
import requests


# Fronius Symo/Gn24 devices
class Fronius:
    def __init__(self, config):
        # Demo code for config access
        print(f"""Fronius device:
            configured host name is {config['fronius']['host_name']}""")

        self.verbose_logging = config.verbose_logging
        self.host_name = config['fronius']['host_name']

        self.url_inverter = (
            f"http://{self.host_name}/solar_api/v1/GetPowerFlowRealtimeData.fcgi")
        self.url_meter = (
            f"http://{self.host_name}/solar_api/v1/GetMeterRealtimeData.cgi?Scope=System")

        # Initialize with values
        self.total_energy_produced_kwh = 0.0
        self.total_energy_consumed_kwh = 0.0
        self.total_energy_fed_in_kwh = 0.0
        self.current_power_consumed_from_grid_kw = 0.0
        self.current_power_consumed_from_pv_kw = 0.0
        self.current_power_consumed_total_kw = 0.0
        self.current_power_fed_in_kw = 0.0

    def copy_data(self, inverter_data, meter_data):
        '''Copies the results from the API request.'''
        # Inverter data
        str_total_produced = inverter_data["Body"]["Data"]["Site"]["E_Total"]
        total_produced = float(str_total_produced)
        # Meter data
        str_total_consumed_from_grid = meter_data["Body"]["Data"]["0"]["EnergyReal_WAC_Plus_Absolute"]
        total_consumed_from_grid = float(str_total_consumed_from_grid)
        str_total_fed_in = meter_data["Body"]["Data"]["0"]["EnergyReal_WAC_Minus_Absolute"]
        total_fed_in = float(str_total_fed_in)
        # Compute other values
        total_self_consumption = total_produced - total_fed_in
        total_consumption = total_consumed_from_grid + total_self_consumption

        # Logging
        if self.verbose_logging:
            print(f"Fronius device: Absolute values:\n"
                  f" - Total produced: {str(total_produced)}\n"
                  f" - Total grid consumption: {str(total_consumed_from_grid)}\n"
                  f" - Total self consumption: {str(total_self_consumption)}\n"
                  f" - Total consumption: {str(total_consumption)}\n"
                  f" - Total fed in: {str(total_fed_in)}")

        # Total/absolute values
        self.total_energy_produced_kwh = total_produced
        self.total_energy_consumed_kwh = total_consumption
        self.total_energy_fed_in_kwh = total_fed_in

        # Now extract the momentary values
        str_cur_production = inverter_data["Body"]["Data"]["Site"]["P_PV"]
        cur_production = float(str_cur_production)
        str_grid_power = inverter_data["Body"]["Data"]["Site"]["P_Grid"]
        grid_power = float(str_grid_power)
        cur_feed_in = grid_power if grid_power > 0.0 else 0.0
        cur_consumption_from_grid = (-grid_power) if grid_power < 0.0 else 0.0
        cur_consumption_from_pv = cur_production - cur_feed_in
        if cur_consumption_from_pv < 0.0:
            cur_consumption_from_pv = 0.0
        cur_consumption_total = cur_consumption_from_grid + cur_consumption_from_pv

        # Logging
        if self.verbose_logging:
            print(f"Fronius device: Momentary values:\n"
                  f" - Current production: {str(cur_production)}\n"
                  f" - Current feed-in: {str(cur_feed_in)}\n"
                  f" - Current consumption from grid: {str(cur_consumption_from_grid)}\n"
                  f" - Current consumption from PV: {str(cur_consumption_from_pv)}\n"
                  f" - Current total consumption: {str(cur_consumption_total)}")

        # Store results
        self.current_power_produced_kw = cur_production
        self.current_power_fed_in_kw = cur_feed_in
        self.current_power_consumed_from_grid_kw = cur_consumption_from_grid
        self.current_power_consumed_from_pv_kw = cur_consumption_from_pv
        self.current_power_consumed_total_kw = cur_consumption_total

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
