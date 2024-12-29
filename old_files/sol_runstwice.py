##UI updates, but runs refresh twice
import solara
import time
from ui import SensorDisplay
from typing import Callable
from sensors import SensorManager
from database import DatabaseManager
from config import Config

# db = DatabaseManager()
# db.initialize_db()

@solara.component
def Page():
    # Set the dark theme
    solara.lab.theme.dark = True
    sensor_manager = SensorManager()

    # Reactive variable to trigger UI refresh
    refresh_trigger = solara.use_reactive(0)

    # Function to poll the database
    def poll_database():
        success = sensor_manager.take_snapshot()
        if success:
            refresh_trigger.value += 1
        else:
            print("Failed to take snapshot.")

    # Function to handle periodic polling in a thread
    def polling_thread():
        while True:
            poll_database()
            time.sleep(Config.POLLING_INTERVAL)

    # Start the polling thread once
    solara.use_thread(polling_thread, dependencies=[])

    SensorDisplay.CombinedGraph()
    with solara.ColumnsResponsive():
        SensorDisplay.SnapshotButton()
        solara.Info(f"Refresh Count: {refresh_trigger.value}")
        SensorDisplay.DistanceComponent()
        with solara.Card("Relay"):
            SensorDisplay.RelayButton()

