import solara
import time
import subprocess
from ui import SensorDisplay
from typing import Callable
from sensors import SensorManager
from database import DatabaseManager
from config import Config
from aioesphomeapi import APIClient, APIConnectionError, RequiresEncryptionAPIError
from esphome.DHT22 import DHT22
# db = DatabaseManager()
# db.initialize_db()
from victron_components import VictronMqtt


@solara.component
def Page():
    solara.lab.theme.dark = True
    sensor_manager = SensorManager()


    with solara.ColumnsResponsive():
        VictronMqtt.MQTTDashboard()
        VictronMqtt.BatteryDial()
        VictronMqtt.AmpsDial()
        VictronMqtt.PowerDial()
        VictronMqtt.TTGText()
    with solara.ColumnsResponsive():
        SensorDisplay.CombinedGraph()


    with solara.ColumnsResponsive():
        SensorDisplay.SnapshotButton()
        SensorDisplay.DistanceComponent()
        SensorDisplay.RelayButton()


    dht22_sensor = DHT22()
    dht22_sensor.SimpleDisplay()

    with solara.Row():
        solara.Button(label="Default")
        solara.Button(label="Default+color", color="primary")
        solara.Button(label="Text", text=True)
        solara.Button(label="Outlined", outlined=True)
        solara.Button(label="Outlined+color", outlined=True, color="primary")

    SensorDisplay.PowerCombinedChart()
