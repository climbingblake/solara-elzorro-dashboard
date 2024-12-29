## without polling

import solara
import time
from ui import SensorDisplay
from typing import Callable
from sensors import SensorManager
from database import DatabaseManager


# db = DatabaseManager()
# db.initialize_db()

@solara.component
def Page():
    # Set the dark theme
    solara.lab.theme.dark = True
    sensor_manager = SensorManager()


    SensorDisplay.CombinedGraph()
    with solara.ColumnsResponsive(6, large=4):
        SensorDisplay.SnapshotButton()
        SensorDisplay.DistanceComponent()
        with solara.Card("Relay"):
            SensorDisplay.RelayButton()


