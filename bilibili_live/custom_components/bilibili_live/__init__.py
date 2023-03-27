from homeassistant import config_entries
from homeassistant.core import HomeAssistant

DOMAIN = "bilibili_live"

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True
