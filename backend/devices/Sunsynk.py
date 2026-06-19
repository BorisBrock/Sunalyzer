import logging


# =============================================================================
# Sunsynk / Deye hybrid inverters (single-phase).
#
# Supports two transports, selected via the "connection" config field:
#
#   - solarman   : talks to the inverter's WiFi/LAN data logger (the "dongle")
#                  over TCP using the Solarman V5 protocol (default port 8899).
#                  Requires the 'pysolarmanv5' package.
#   - modbus_rtu : talks directly to the inverter's RS485 port via a USB-RS485
#                  adapter (Modbus RTU over a serial line). Requires 'pymodbus'
#                  and the host serial device passed into the container.
#
# Both transports read the same registers; only the wire protocol differs.
# No cloud, no 3rd party - in keeping with Sunalyzer's offline design.
#
# IMPORTANT - REGISTER MAP:
# Sunsynk/Deye Modbus register addresses and scales vary by model and firmware.
# The values below are the de-facto-standard "single phase hybrid" set used by
# the kellerza/sunsynk library and Solar Assistant. VERIFY THEM AGAINST YOUR
# OWN INVERTER before trusting the numbers. References:
#   - https://github.com/kellerza/sunsynk  (definitions/)
#   - Solar Assistant Sunsynk/Deye register documentation
# If a value reads wrong, adjust the register/scale in the REGISTERS block.
# =============================================================================

# --- Holding register map (function code 3) -------------------------------
# Cumulative / lifetime energy counters. 32-bit (low word, high word), 0.1 kWh.
REG_TOTAL_PV_PRODUCTION = (96, 97)      # Lifetime PV generation
REG_TOTAL_GRID_EXPORT = (81, 82)        # Lifetime energy sold to grid
REG_TOTAL_LOAD = (85, 86)               # Lifetime load (house) consumption
ENERGY_SCALE_KWH = 0.1

# Instantaneous power, signed 16-bit, in Watts.
REG_PV1_POWER = 186                     # MPPT 1 power
REG_PV2_POWER = 187                     # MPPT 2 power
REG_GRID_CT_POWER = 172                 # External CT clamp: + = import, - = export
REG_LOAD_POWER = 178                    # Essential/house load power (handles battery)


class _SolarmanTransport:
    '''Reads registers via the Solarman V5 protocol (WiFi/LAN data logger).'''

    def __init__(self, cfg):
        self.host_name = cfg['host_name']
        self.logger_serial = int(cfg['logger_serial'])
        self.port = int(cfg.get('port', 8899))
        self.mb_slave_id = int(cfg.get('mb_slave_id', 1))
        self._client = None

    def describe(self):
        return (f"Solarman V5 {self.host_name}:{self.port} "
                f"(logger serial {self.logger_serial})")

    def open(self):
        # Imported lazily so the module loads without pysolarmanv5 installed.
        from pysolarmanv5 import PySolarmanV5
        self._client = PySolarmanV5(
            self.host_name,
            self.logger_serial,
            port=self.port,
            mb_slave_id=self.mb_slave_id,
            socket_timeout=5,
            verbose=False)

    def read_holding_registers(self, address, count):
        '''Returns a list of `count` register values starting at `address`.'''
        return self._client.read_holding_registers(address, count)

    def close(self):
        if self._client is not None:
            try:
                self._client.disconnect()
            except Exception:
                pass
            self._client = None


class _ModbusRtuTransport:
    '''Reads registers via Modbus RTU over a serial line (USB-RS485 adapter).'''

    def __init__(self, cfg):
        self.serial_port = cfg['serial_port']
        self.baudrate = int(cfg.get('baudrate', 9600))
        self.parity = str(cfg.get('parity', 'N'))
        self.stopbits = int(cfg.get('stopbits', 1))
        self.bytesize = int(cfg.get('bytesize', 8))
        self.mb_slave_id = int(cfg.get('mb_slave_id', 1))
        self._client = None

    def describe(self):
        return (f"Modbus RTU {self.serial_port}@{self.baudrate} "
                f"{self.bytesize}{self.parity}{self.stopbits} "
                f"(slave {self.mb_slave_id})")

    def open(self):
        # Imported lazily so the module loads without pymodbus installed.
        from pymodbus.client import ModbusSerialClient
        self._client = ModbusSerialClient(
            port=self.serial_port,
            baudrate=self.baudrate,
            parity=self.parity,
            stopbits=self.stopbits,
            bytesize=self.bytesize,
            timeout=5)
        if not self._client.connect():
            raise ConnectionError(
                f"could not open serial port {self.serial_port}")

    def read_holding_registers(self, address, count):
        '''Returns a list of `count` register values starting at `address`.'''
        result = self._client.read_holding_registers(
            address, count=count, slave=self.mb_slave_id)
        if result.isError():
            raise IOError(
                f"Modbus error reading register {address}: {result}")
        return result.registers

    def close(self):
        if self._client is not None:
            try:
                self._client.close()
            except Exception:
                pass
            self._client = None


# Maps the "connection" config value onto a transport implementation.
_TRANSPORTS = {
    'solarman': _SolarmanTransport,
    'modbus_rtu': _ModbusRtuTransport,
}


class Sunsynk:
    def __init__(self, config):
        cfg = config.config_data['sunsynk']

        connection = str(cfg.get('connection', 'solarman')).lower()
        if connection not in _TRANSPORTS:
            raise ValueError(
                f"Sunsynk device: unknown connection '{connection}', "
                f"expected one of {sorted(_TRANSPORTS)}")
        self.transport = _TRANSPORTS[connection](cfg)

        logging.info(f"Sunsynk device: using {self.transport.describe()}")

        # Initialize with default values
        self.total_energy_produced_kwh = 0.0
        self.total_energy_consumed_kwh = 0.0
        self.total_energy_fed_in_kwh = 0.0
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
                "Sunsynk device: Error: connecting to the device failed")
            raise

    @staticmethod
    def _to_signed(value):
        '''Interprets a 16-bit register value as a signed integer.'''
        return value - 0x10000 if value >= 0x8000 else value

    @staticmethod
    def _read_u32(reader, regs):
        '''Reads a 32-bit unsigned value from a (low_word, high_word) pair.'''
        low = reader.read_holding_registers(regs[0], 1)[0]
        high = reader.read_holding_registers(regs[1], 1)[0]
        return low + (high << 16)

    def _read_signed(self, reader, register):
        '''Reads a single signed 16-bit register.'''
        return self._to_signed(reader.read_holding_registers(register, 1)[0])

    def copy_data(self, reader):
        '''Reads the registers and maps them onto Sunalyzer's data model.'''
        # --- Cumulative / lifetime values (kWh) ---
        total_produced_kwh = self._read_u32(
            reader, REG_TOTAL_PV_PRODUCTION) * ENERGY_SCALE_KWH
        total_fed_in_kwh = self._read_u32(
            reader, REG_TOTAL_GRID_EXPORT) * ENERGY_SCALE_KWH
        # Sunsynk exposes total load directly, so use it instead of deriving.
        total_consumption_kwh = self._read_u32(
            reader, REG_TOTAL_LOAD) * ENERGY_SCALE_KWH

        if logging.getLogger().level == logging.DEBUG:
            logging.debug(f"Sunsynk device: Absolute values:\n"
                          f" - Total produced: {total_produced_kwh} kWh\n"
                          f" - Total consumption: {total_consumption_kwh} kWh\n"
                          f" - Total fed in: {total_fed_in_kwh} kWh")

        self.total_energy_produced_kwh = total_produced_kwh
        self.total_energy_consumed_kwh = total_consumption_kwh
        self.total_energy_fed_in_kwh = total_fed_in_kwh

        # --- Momentary values (kW) ---
        cur_production_kw = (
            self._read_signed(reader, REG_PV1_POWER)
            + self._read_signed(reader, REG_PV2_POWER)) * 0.001
        if cur_production_kw < 0.0:
            cur_production_kw = 0.0

        # Grid CT: positive = importing from grid, negative = feeding in
        grid_power_kw = self._read_signed(reader, REG_GRID_CT_POWER) * 0.001
        cur_feed_in_kw = (-grid_power_kw) if grid_power_kw < 0.0 else 0.0
        cur_consumption_from_grid = grid_power_kw if grid_power_kw > 0.0 else 0.0

        # Read total load directly (correctly accounts for battery charge/discharge)
        cur_consumption_total = self._read_signed(reader, REG_LOAD_POWER) * 0.001
        if cur_consumption_total < 0.0:
            cur_consumption_total = 0.0
        cur_consumption_from_pv = cur_consumption_total - cur_consumption_from_grid
        if cur_consumption_from_pv < 0.0:
            cur_consumption_from_pv = 0.0

        if logging.getLogger().level == logging.DEBUG:
            logging.debug(f"Sunsynk device: Momentary values:\n"
                          f" - Current production: {cur_production_kw} kW\n"
                          f" - Current feed-in: {cur_feed_in_kw} kW\n"
                          f" - Current consumption from grid: {cur_consumption_from_grid} kW\n"
                          f" - Current consumption from PV: {cur_consumption_from_pv} kW\n"
                          f" - Current total consumption: {cur_consumption_total} kW")

        self.current_power_produced_kw = cur_production_kw
        self.current_power_fed_in_kw = cur_feed_in_kw
        self.current_power_consumed_from_grid_kw = cur_consumption_from_grid
        self.current_power_consumed_from_pv_kw = cur_consumption_from_pv
        self.current_power_consumed_total_kw = cur_consumption_total

    def update(self):
        '''Updates all device stats.'''
        try:
            self.transport.open()
            self.copy_data(self.transport)
        except Exception as e:
            logging.error(f"Sunsynk device: error communicating with "
                          f"{self.transport.describe()}: {e}")
            raise
        finally:
            self.transport.close()
