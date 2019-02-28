import logging
from datetime import timedelta
import voluptuous as vol
import homeassistant.components as core
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv
from homeassistant.components.device_tracker import PLATFORM_SCHEMA, DeviceScanner, DOMAIN
from homeassistant.components import device_tracker
from homeassistant.const import (
    STATE_HOME, STATE_NOT_HOME, CONF_HOST, CONF_API_KEY, CONF_SCAN_INTERVAL, CONF_USERNAME
)

REQUIREMENTS = ['clearpasspy==1.0.2']

SCAN_INTERVAL = timedelta(seconds=120)
CONF_USERNAME = 'client_id'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=SCAN_INTERVAL): cv.time_period
})


DOMAIN ="device_tracker"


_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)
_LOGGER.addHandler(logging.StreamHandler())

CONF_HOST = 'host'
CONF_API_KEY = 'api_key'
CONF_SCAN_INTERVAL= 'scan_interval'

async def get_scanner(hass, config):
    cppm_host = config[DOMAIN].get(CONF_HOST)
    api_key = config[DOMAIN].get(CONF_API_KEY)
    client_id = config[DOMAIN].get(CONF_USERNAME)
    scan_interval = config[DOMAIN].get(CONF_SCAN_INTERVAL)
    grant_type = 'client_credentials'
    newScan = CPPMDeviceScanner(hass, cppm_host, client_id, api_key, grant_type, scan_interval)
    return newScan if newScan.success_init else None

class CPPMDeviceScanner(DeviceScanner):
    def __init__(self, hass, cppm_host, client_id, api_key, grant_type, scan_interval):
        _LOGGER.debug("-------------INIT CALLED--------------")
        self._hass = hass
        self._cppm_host = cppm_host
        self._api_key = api_key
        self._grant_type = grant_type
        self._client_id = client_id
        self._scan_int = scan_interval
        self.success_init = self.get_cppm_data()

    async def async_scan_devices(self):
        _LOGGER.debug("------ SCAN DEVICES CALLED. ------------")
        self.get_cppm_data()
        return [device['mac'] for device in self.results]

    async def async_get_device_name(self, device):
        _LOGGER.debug("------ RESOLVING DEVICE NAME ----")
        return [device['name'] for device in self.results]
    @Throttle(SCAN_INTERVAL)

    def get_cppm_data(self):
        """Retrieve data from Aruba Clearpass and return parsed result."""
        from clearpasspy import ClearPass
        _LOGGER.debug("--------- GET CPPM DATA CALLED------------")
        data = {
            'server': self._cppm_host,
            'grant_type': self._grant_type,
            'secret': self._api_key,
            'client': self._client_id
        }
        _LOGGER.debug("DATA: {}".format(data))

        CPPM = ClearPass(data)
        endpoints = CPPM.get_endpoints(100)['_embedded']['items']
        devices = []
        for item in endpoints:
            if CPPM.online_status(item['mac_address']) == True:
                device = {
                    'mac': item['mac_address'],
                    'name': item['mac_address']
                }
                devices.append(device)
            else:
                continue
        _LOGGER.debug("-----------Update successful!-----------")
        self.results = devices
        return True
