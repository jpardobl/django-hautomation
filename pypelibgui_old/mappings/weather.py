import requests
from pypelibgui import settings
from hautomation_restclient.cmds import pl_switch


def current_temperature(mo=None):
    return requests.get(settings.TEMPERATURE_URI).json()["temperature"]
    #return 18


def confort_temperature(mo=None):
    return 22


def economic_temperature(mo=None):
    return 18


def start_heater():
    pl_switch(
        settings.HEATER_PROTOCOL,
        settings.HEATER_DID,
        "on",
        HEATER_URL, HA_USERNAME, HA_PASSWORD)


def stop_heater():
    pl_switch(
        settings.HEATER_PROTOCOL,
        settings.HEATER_DID,
        "off",
        HEATER_URL, HA_USERNAME, HA_PASSWORD)

mappings = [
    current_temperature,
    confort_temperature,
    economic_temperature,
    start_heater,
    stop_heater, ]
