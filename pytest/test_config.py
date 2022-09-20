from config import Config
import logging

# Test if the template can be read
def test_template_config_is_readable():
    cfg = Config("templates/config.yml")
    assert cfg is not None
    assert cfg.log_level is logging.DEBUG
    assert cfg.config_data["time_zone"] == "Europe/Berlin"
