# Empty device to allow adding values from multiple devices
class Empty:
    def __init__(self, config):
        # Demo code for config access
        # print(f"""Dummy device: config test -
        #    foo={config.config_data['dummy']['foo']}
        #    bar={config.config_data['dummy']['bar']}""")

        # Initialize with some random values
        self.total_energy_produced_kwh = 0.0
        self.total_energy_consumed_kwh = 0.0
        self.total_energy_fed_in_kwh = 0.0
        self.total_energy_consumed_from_grid_kwh = 0.0

        self.current_power_produced_kw = 0.0
        self.current_power_consumed_from_grid_kw = 0.0
        self.current_power_consumed_from_pv_kw = 0.0
        self.current_power_consumed_total_kw = 0.0
        self.current_power_fed_in_kw = 0.0

    def update(self):
        '''Nothing to do'''
