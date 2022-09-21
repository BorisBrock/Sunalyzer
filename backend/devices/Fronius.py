import requests
import logging


# Fronius Symo/Gn24 devices
class Fronius:
    def __init__(self, config):
        # Demo code for config access
        logging.info(f"Fronius device: "
                     f"configured host name is "
                     f"{config.config_data['fronius']['host_name']}")

        self.host_name = config.config_data['fronius']['host_name']

        self.url_inverter = (
            f"http://{self.host_name}/solar_api/v1/GetPowerFlowRealtimeData.fcgi")
        self.url_meter = (
            f"http://{self.host_name}/solar_api/v1/GetMeterRealtimeData.cgi?Scope=System")

        # Initialize with default values
        self.total_energy_produced_kwh = 0.0
        self.total_energy_consumed_kwh = 0.0
        self.total_energy_fed_in_kwh = 0.0
        self.current_power_consumed_from_grid_kw = 0.0
        self.current_power_consumed_from_pv_kw = 0.0
        self.current_power_consumed_total_kw = 0.0
        self.current_power_fed_in_kw = 0.0

        # Test connection by doing an initial update
        try:
            self.update()
        except Exception:
            logging.error(
                "Fronius device: Error: connecting to the device failed")
            raise

    def copy_data(self, inverter_data, meter_data):
        '''Copies the results from the API request.'''
        # Inverter data
        str_total_produced_wh = inverter_data["Body"]["Data"]["Site"]["E_Total"]
        total_produced_kwh = float(str_total_produced_wh) * 0.001
        # Meter data
        str_total_consumed_from_grid_wh = meter_data["Body"]["Data"]["0"]["EnergyReal_WAC_Plus_Absolute"]
        total_consumed_from_grid_kwh = float(
            str_total_consumed_from_grid_wh) * 0.001
        str_total_fed_in_wh = meter_data["Body"]["Data"]["0"]["EnergyReal_WAC_Minus_Absolute"]
        total_fed_in_kwh = float(str_total_fed_in_wh) * 0.001
        # Compute other values
        total_self_consumption_kwh = total_produced_kwh - total_fed_in_kwh
        total_consumption_kwh = total_consumed_from_grid_kwh + total_self_consumption_kwh

        # Logging
        if logging.getLogger().level == logging.DEBUG:
            logging.debug(f"Fronius device: Absolute values:\n"
                          f" - Total produced: {str(total_produced_kwh)} kWh\n"
                          f" - Total grid consumption: {str(total_consumed_from_grid_kwh)} kWh\n"
                          f" - Total self consumption: {str(total_self_consumption_kwh)} kWh\n"
                          f" - Total consumption: {str(total_consumption_kwh)} kWh\n"
                          f" - Total fed in: {str(total_fed_in_kwh)} kWh")

        # Total/absolute values
        self.total_energy_produced_kwh = total_produced_kwh
        self.total_energy_consumed_kwh = total_consumption_kwh
        self.total_energy_fed_in_kwh = total_fed_in_kwh

        # Now extract the momentary values
        str_cur_production_w = inverter_data["Body"]["Data"]["Site"]["P_PV"]
        cur_production_kw = 0.0 if str_cur_production_w is None else float(
            str_cur_production_w) * 0.001
        str_grid_power_w = inverter_data["Body"]["Data"]["Site"]["P_Grid"]
        grid_power_kw = float(str_grid_power_w) * 0.001
        cur_feed_in_kw = (-grid_power_kw) if grid_power_kw < 0.0 else 0.0
        cur_consumption_from_grid = grid_power_kw if grid_power_kw > 0.0 else 0.0
        cur_consumption_from_pv = cur_production_kw - cur_feed_in_kw
        if cur_consumption_from_pv < 0.0:
            cur_consumption_from_pv = 0.0
        cur_consumption_total = cur_consumption_from_grid + cur_consumption_from_pv

        # Logging
        if logging.getLogger().level == logging.DEBUG:
            logging.debug(f"Fronius device: Momentary values:\n"
                          f" - Current production: {str(cur_production_kw)} kW\n"
                          f" - Current feed-in: {str(cur_feed_in_kw)} kW\n"
                          f" - Current consumption from grid: {str(cur_consumption_from_grid)}\n"
                          f" - Current consumption from PV: {str(cur_consumption_from_pv)}\n"
                          f" - Current total consumption: {str(cur_consumption_total)}")

        # Store results
        self.current_power_produced_kw = cur_production_kw
        self.current_power_fed_in_kw = cur_feed_in_kw
        self.current_power_consumed_from_grid_kw = cur_consumption_from_grid
        self.current_power_consumed_from_pv_kw = cur_consumption_from_pv
        self.current_power_consumed_total_kw = cur_consumption_total

    def update(self):
        '''Updates all device stats.'''
        try:
            # Query inverter data
            r_inverter = requests.get(self.url_inverter, timeout=5)
            r_inverter.raise_for_status()
            # Query smart meter data
            r_meter = requests.get(self.url_meter, timeout=5)
            r_meter.raise_for_status()
            # Extract and process relevant data
            self.copy_data(r_inverter.json(), r_meter.json())
        except requests.exceptions.Timeout:
            logging.error(f"Fronius device: Timeout requesting "
                          f"'{self.url_inverter}' or '{self.url_meter}'")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"Fronius device: requests exception {e} for URL "
                          f"'{self.url_inverter}' or '{self.url_meter}'")
            raise
