import requests
import json
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_UID

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_UID): cv.string,
        vol.Required(CONF_NAME): cv.string,
    }
)

async def async_setup_entry(hass, config_entry, async_add_entities):
    uid = config_entry.data["uid"]
    custom_name = config_entry.data.get("name", None)
    sensor = BilibiliLiveSensor(uid, custom_name)
    await hass.async_add_executor_job(sensor.update)
    async_add_entities([sensor], True)

class BilibiliLiveSensor(Entity):
    def __init__(self, uid, custom_name=None):
        self._uid = uid
        self._state = None
        self._attributes = {}
        self._custom_name = custom_name

    @property
    def unique_id(self):
        return f"bilibili_live_{self._uid}"

    @property
    def name(self):
        if self._custom_name == "Bilibili Live":
            return self._attributes.get("name")
        else:
            return self._custom_name

    @property
    def state(self):
        return self._attributes.get("status")

    @property
    def extra_state_attributes(self):
        return self._attributes

    @property
    def icon(self):
        return "mdi:television-classic"

    def update(self):
        url = f"https://api.bilibili.com/x/space/acc/info?mid={self._uid}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)

        if data["data"]["live_room"]["liveStatus"]:
            status = "直播中"
        else:
            status = "休息中"

        result = {
            "status": status,
            "title": data["data"]["live_room"]["title"],
            "name": data["data"]["name"],
            "face": data["data"]["face"],
            "url": data["data"]["live_room"]["url"],
            "cover": data["data"]["live_room"]["cover"]
        }

        self._attributes = result
