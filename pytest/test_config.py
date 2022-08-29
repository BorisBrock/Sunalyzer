from config import Config


# Test if the template can be read
def test_template_config_is_readable():
    cfg = Config("templates/config.yml")
    assert cfg is not None
    assert cfg.verbose_logging is True
    assert cfg.config_data["time_zone"] == "Europe/Berlin"
