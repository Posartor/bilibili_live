import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME

from .const import DOMAIN, CONF_UID

class BilibiliLiveConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        existing_entries = self._async_current_entries()
        if user_input is not None:
            uid = user_input[CONF_UID]
            for entry in existing_entries:
                if entry.data.get(CONF_UID) == uid:
                    return self.async_abort(reason="uid_already_configured")
            return self.async_create_entry(
                title=user_input[CONF_NAME], data=user_input
            )
        schema = vol.Schema(
            {
                vol.Required(CONF_UID): str,
                vol.Required(CONF_NAME, default="Bilibili Live"): str,
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=schema, description_placeholders={
                "existing_uids": ", ".join(entry.data[CONF_UID] for entry in existing_entries)
            }
        )
