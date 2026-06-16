import pytest

import devices.Sunsynk as sunsynk_mod
from devices.Sunsynk import Sunsynk


class FakeConfig:
    '''Minimal stand-in for the Config object the device expects.'''

    def __init__(self, sunsynk_cfg):
        self.config_data = {'sunsynk': sunsynk_cfg}


class FakeTransport:
    '''Returns canned register values so the mapping logic can be tested
    without any hardware, network, or transport library installed.'''

    def __init__(self, cfg, registers):
        self.cfg = cfg
        self.registers = registers

    def describe(self):
        return "fake transport"

    def open(self):
        pass

    def close(self):
        pass

    def read_holding_registers(self, address, count):
        return [self.registers[address + i] for i in range(count)]


def _make_device(monkeypatch, registers, connection='solarman'):
    '''Builds a Sunsynk device whose transport is the FakeTransport above.'''
    def factory(cfg):
        return FakeTransport(cfg, registers)

    monkeypatch.setitem(sunsynk_mod._TRANSPORTS, connection, factory)
    return Sunsynk(FakeConfig({'connection': connection}))


# Lifetime energy counters are shared across the scenarios below.
# 32-bit (low, high) words, scaled by 0.1 kWh.
_BASE_ENERGY_REGISTERS = {
    96: 1000, 97: 0,   # Total PV production -> 100.0 kWh
    81: 500, 82: 0,    # Total grid export   ->  50.0 kWh
    85: 2000, 86: 0,   # Total load          -> 200.0 kWh
}


def test_export_scenario(monkeypatch):
    '''PV exceeds load: surplus is fed into the grid.'''
    registers = dict(_BASE_ENERGY_REGISTERS)
    registers.update({
        186: 1500,    # PV1 power 1500 W
        187: 500,     # PV2 power  500 W  -> 2.0 kW produced
        172: 64736,   # Grid CT -800 W (signed) -> exporting 0.8 kW
        178: 1200,    # Load power 1200 W -> 1.2 kW consumed
    })
    dev = _make_device(monkeypatch, registers)

    # Lifetime counters
    assert dev.total_energy_produced_kwh == pytest.approx(100.0)
    assert dev.total_energy_fed_in_kwh == pytest.approx(50.0)
    assert dev.total_energy_consumed_kwh == pytest.approx(200.0)

    # Momentary values
    assert dev.current_power_produced_kw == pytest.approx(2.0)
    assert dev.current_power_fed_in_kw == pytest.approx(0.8)
    assert dev.current_power_consumed_from_grid_kw == pytest.approx(0.0)
    assert dev.current_power_consumed_total_kw == pytest.approx(1.2)
    assert dev.current_power_consumed_from_pv_kw == pytest.approx(1.2)


def test_import_scenario(monkeypatch):
    '''Load exceeds PV: shortfall is drawn from the grid.'''
    registers = dict(_BASE_ENERGY_REGISTERS)
    registers.update({
        186: 700,     # PV1 power 700 W
        187: 200,     # PV2 power 200 W -> 0.9 kW produced
        172: 600,     # Grid CT +600 W (signed) -> importing 0.6 kW
        178: 1500,    # Load power 1500 W -> 1.5 kW consumed
    })
    dev = _make_device(monkeypatch, registers)

    assert dev.current_power_produced_kw == pytest.approx(0.9)
    assert dev.current_power_fed_in_kw == pytest.approx(0.0)
    assert dev.current_power_consumed_from_grid_kw == pytest.approx(0.6)
    assert dev.current_power_consumed_total_kw == pytest.approx(1.5)
    # consumed_total - from_grid
    assert dev.current_power_consumed_from_pv_kw == pytest.approx(0.9)


def test_unknown_connection_raises():
    '''An unrecognised transport name fails fast with a clear error.'''
    with pytest.raises(ValueError):
        Sunsynk(FakeConfig({'connection': 'carrier_pigeon'}))
