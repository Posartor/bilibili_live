import requests
import json
import time
import urllib.parse
from hashlib import md5
from functools import reduce
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_UID

mixinKeyEncTab = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_UID): cv.string,
        vol.Optional(CONF_NAME): cv.string,
    }
)

def getMixinKey(orig: str):
    return reduce(lambda s, i: s + orig[i], mixinKeyEncTab, '')[:32]

def encWbi(params: dict, img_key: str, sub_key: str):
    mixin_key = getMixinKey(img_key + sub_key)
    curr_time = round(time.time())
    params['wts'] = curr_time
    params = dict(sorted(params.items()))
    params = {
        k : ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v 
        in params.items()
    }
    query = urllib.parse.urlencode(params)
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()
    params['w_rid'] = wbi_sign
    return params

def getWbiKeys():
    resp = requests.get('https://api.bilibili.com/x/web-interface/nav')
    resp.raise_for_status()
    json_content = resp.json()
    img_url: str = json_content['data']['wbi_img']['img_url']
    sub_url: str = json_content['data']['wbi_img']['sub_url']
    img_key = img_url.rsplit('/', 1)[1].split('.')[0]
    sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
    return img_key, sub_key

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
        img_key, sub_key = getWbiKeys()
        params = {"mid": self._uid, "token": "", "platform": "web", "web_location": "1550101"}
        signed_params = encWbi(params, img_key, sub_key)
        url = f"https://api.bilibili.com/x/space/wbi/acc/info?" + urllib.parse.urlencode(signed_params)
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15"
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
