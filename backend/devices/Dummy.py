# Dummy device for testing purposes
class Dummy:
    def __init__(self, config):
        # Demo code for config access
        print(f"""Dummy device: config test -
            foo={config.config_data['dummy']['foo']}
            bar={config.config_data['dummy']['bar']}""")

        # Initialize with some random values
        self.total_energy_produced_kwh = 1200.0
        self.total_energy_consumed_kwh = 900.0
        self.total_energy_fed_in_kwh = 800.0

        self.current_power_produced_kw = 300.0
        self.current_power_consumed_from_grid_kw = 200.0
        self.current_power_consumed_from_pv_kw = 300.0
        self.current_power_consumed_total_kw = 500.0
        self.current_power_fed_in_kw = 100.0

    # Increment the values on each update, just so something changes
    def update(self):
        '''Increment the values on each update, just so something changes.'''
        self.total_energy_produced_kwh = self.total_energy_produced_kwh + 1
        self.total_energy_consumed_kwh = self.total_energy_consumed_kwh + 1
        self.total_energy_fed_in_kwh = self.total_energy_fed_in_kwh + 1

        #self.current_power_produced_kw = self.current_power_produced_kw
        #self.current_power_consumed_from_grid_kw = self.current_power_consumed_from_grid_kw
        #self.current_power_consumed_from_pv_kw = self.current_power_consumed_from_pv_kw
        #self.current_power_consumed_total_kw = self.current_power_consumed_total_kw
        #self.current_power_fed_in_kw = self.current_power_fed_in_kw
