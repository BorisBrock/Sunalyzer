# Fronius Symo/Gn24 devices
class Fronius:
    def __init__(self, config):
        # Demo code for config access
        print(
            f"Fronius device: configured host name is {config['fronius']['host_name']}")

        # Initialize with some random values
        self.total_energy_produced_kwh = 1200.0
        self.total_energy_consumed_kwh = 900.0
        self.total_energy_fed_in_kwh = 800.0

        self.current_power_produced_kw = 300.0
        self.current_power_consumed_kw = 700.0
        self.current_power_fed_in_kw = 100.0

    def update(self):
        '''Todo: add documentation.'''
        # Increment the values on each update, just so something changes
        self.total_energy_produced_kwh = self.total_energy_produced_kwh + 1
        self.total_energy_consumed_kwh = self.total_energy_consumed_kwh + 1
        self.total_energy_fed_in_kwh = self.total_energy_fed_in_kwh + 1

        self.current_power_produced_kw = self.current_power_produced_kw + 1
        self.current_power_consumed_kw = self.current_power_consumed_kw + 1
        self.current_power_fed_in_kw = self.current_power_fed_in_kw + 1
