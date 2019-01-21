import logging
import json

from datetime import datetime
from datetime import timedelta
import voluptuous as vol
import homeassistant.components as core
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv
from homeassistant.components.device_tracker import PLATFORM_SCHEMA, DeviceScanner, DOMAIN
from homeassistant.components import device_tracker
from homeassistant.const import (
    STATE_HOME, STATE_NOT_HOME, CONF_HOST, CONF_API_KEY, CONF_PASSWORD, CONF_SCAN_INTERVAL
)

SCAN_INTERVAL = timedelta(seconds=120)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL): cv.time_period
})


DOMAIN ="device_tracker"


_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)
_LOGGER.addHandler(logging.StreamHandler())

CONF_HOST = 'host'
CONF_API_KEY = 'password'
CONF_SCAN_INTERVAL= 'scan_interval'

def get_scanner(hass, config):
    cppm_host = config[DOMAIN].get(CONF_HOST)
    api_key = config[DOMAIN].get(CONF_API_KEY)
    scan_interval = config[DOMAIN].get(CONF_SCAN_INTERVAL)
    newScan = CPPMDeviceScanner(hass, cppm_host, api_key, scan_interval)
    return newScan if newScan.success_init else None

class CPPMDeviceScanner(DeviceScanner):
    def __init__(self, hass, cppm_host, api_key, scan_interval):
        _LOGGER.debug("-------------INIT CALLED--------------")
        self._hass = hass
        self._cppm_host = cppm_host
        self._api_key = api_key
        self._scan_int = scan_interval
        self.success_init = self.get_cppm_data()

    async def async_scan_devices(self):
        _LOGGER.debug("------ SCAN DEVICES CALLED. ------------")
        self.get_cppm_data()
        return [device['mac'] for device in self.results]

    async def async_get_device_name(self, device):
        _LOGGER.debug("------ RESOLVING DEVICE NAME ----")
        return [device['name'] for device in self.results]

    async def async_get_extra_attributes(self, device):
        """Return the IP of the given device."""
        filter_ip = next((
            result['ip'] for result in self.results
            if result['mac'] == device), None)
        return {'ip': filter_ip}

    @Throttle(SCAN_INTERVAL)
    def get_cppm_data(self):
        """Retrieve data from Aruba Clearpass and return parsed result."""
        import requests
        _LOGGER.debug("--------- GET CPPM DATA CALLED------------")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': "{}".format(self._api_key)
        }
        url = 'https://' + self._cppm_host + ':443/api/endpoint?filter=%7B%7D&sort=%2Bid&offset=0&limit=100&calculate_count=false'
        _LOGGER.debug("------------URL: {} ------------".format(url))
        r = requests.get(url, headers=headers)
        json_r = json.loads(r.text)
        devices = []
        for item in json_r['_embedded']['items']:
            url = 'https://' + self._cppm_host + ':443/api/insight/endpoint/mac/' + item['mac_address']
            r = requests.get(url, headers=headers)
            json_r = json.loads(r.text)
            if json_r['is_online'] == True:
                device = {
                    'ip': json_r['ip'],
                    'mac': json_r['mac'],
                    'name': json_r['device_name']
                }
                devices.append(device)
            else:
                continue
        _LOGGER.debug("-----------Update successful!-----------")
        self.results = devices
        return True