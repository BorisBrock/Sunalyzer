import requests
import logging


# HomeWizard P1 devices
class HomeWizardP1:
    def __init__(self, config):
        # Demo code for config access
        logging.info(f"HomeWizard P1 device: "
                     f"configured host name is "
                     f"{config.config_data['homewizardp1']['host_name']}")

        self.host_name = config.config_data['homewizardp1']['host_name']

        self.url_meter = (
            f"http://{self.host_name}/api/v1/data")

        # Initialize with default values
        self.total_energy_produced_kwh = 0.0
        self.total_energy_consumed_kwh = 0.0
        self.total_energy_fed_in_kwh = 0.0
        self.total_energy_consumed_from_grid_kwh = 0.0

        self.current_power_produced_kw = 0.0
        self.current_power_consumed_from_grid_kw = 0.0
        self.current_power_consumed_from_pv_kw = 0.0
        self.current_power_consumed_total_kw = 0.0
        self.current_power_fed_in_kw = 0.0

        # Test connection by doing an initial update
        try:
            self.update()
        except Exception:
            logging.error(
                "HomeWizard P1: Error: connecting to the device failed")
            raise

    def copy_data(self, meter_data):
        '''Copies the results from the API request.'''
        # Meter data
        total_consumed_from_grid_kwh = meter_data["total_power_import_kwh"]
        total_fed_in_kwh = meter_data["total_power_export_kwh"]
        # Compute other values
        # total_self_consumption_kwh = total_produced_kwh - total_fed_in_kwh
        # total_consumption_kwh = total_consumed_from_grid_kwh + total_self_consumption_kwh

        # Logging
        if logging.getLogger().level == logging.DEBUG:
            logging.debug(f"HomeWizard P1: Absolute values:\n"
                          f" - Total grid consumption: {str(total_consumed_from_grid_kwh)} kWh\n"
                          f" - Total fed in: {str(total_fed_in_kwh)} kWh")

        # Total/absolute values
        self.total_energy_fed_in_kwh = total_fed_in_kwh
        self.total_energy_consumed_from_grid_kwh = total_consumed_from_grid_kwh
        # self.total_energy_consumed_in_kwh = total_consumed_from_grid_kwh

        # Now extract the momentary values
        str_grid_power_w = meter_data["active_power_w"]
        grid_power_kw = float(str_grid_power_w) * 0.001
        cur_feed_in_kw = min(grid_power_kw, 0.0) * -1
        cur_consumption_from_grid = max(grid_power_kw, 0.0)

        # Logging
        if logging.getLogger().level == logging.DEBUG:
            logging.debug(f"HomeWizard P1 device: Momentary values:\n"
                          f" - Current feed-in: {str(cur_feed_in_kw)} kW\n"
                          f" - Current consumption from grid: {str(cur_consumption_from_grid)} kW")

        # Store results
        self.current_power_fed_in_kw = cur_feed_in_kw
        self.current_power_consumed_from_grid_kw = cur_consumption_from_grid

    def update(self):
        '''Updates all device stats.'''
        try:
            # Query smart meter data
            r_meter = requests.get(self.url_meter, timeout=5)
            r_meter.raise_for_status()
            # Extract and process relevant data
            self.copy_data(r_meter.json())
        except requests.exceptions.Timeout:
            logging.error(f"HomeWizard P1: Timeout requesting "
                          f"'{self.url_meter}'")
            raise
        except requests.exceptions.RequestException as e:
            logging.error(f"HomeWizard P1: requests exception {e} for URL "
                          f"'{self.url_meter}'")
            raise
