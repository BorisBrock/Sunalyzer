from devices.Dummy import Dummy


# Test if the template can be read
def test_template_config_is_readable():
    dev = Dummy(None)
    assert dev is not None
    # Set A
    v1_a = dev.total_energy_produced_kwh
    v2_a = dev.total_energy_consumed_kwh
    v3_a = dev.total_energy_fed_in_kwh
    v4_a = dev.current_power_produced_kw
    v5_a = dev.current_power_consumed_from_grid_kw
    v6_a = dev.current_power_consumed_from_pv_kw
    v7_a = dev.current_power_consumed_total_kw
    v8_a = dev.current_power_fed_in_kw
    # Update
    dev.update()
    # Set A
    v1_b = dev.total_energy_produced_kwh
    v2_b = dev.total_energy_consumed_kwh
    v3_b = dev.total_energy_fed_in_kwh
    v4_b = dev.current_power_produced_kw
    v5_b = dev.current_power_consumed_from_grid_kw
    v6_b = dev.current_power_consumed_from_pv_kw
    v7_b = dev.current_power_consumed_total_kw
    v8_b = dev.current_power_fed_in_kw
    # Compare
    assert v1_a <= v1_b
    assert v2_a <= v2_b
    assert v3_a <= v3_b
    assert v4_a <= v4_b
    assert v5_a <= v5_b
    assert v6_a <= v6_b
    assert v7_a <= v7_b
    assert v8_a <= v8_b
