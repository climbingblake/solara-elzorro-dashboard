# refreshing correclty, only once but UI is not updating



import threading
import solara
from sensors import SensorManager
from ui import SensorDisplay
import time

# Use a single global thread to manage polling
polling_thread_initialized = False


def initialize_polling_thread(sensor_manager, refresh_trigger):
    """Initialize the polling thread if not already started."""
    global polling_thread_initialized

    if not polling_thread_initialized:
        polling_thread_initialized = True

        def polling_thread():
            while True:
                success = sensor_manager.take_snapshot()
                if success:
                    refresh_trigger.value += 1
                    print("Snapshot taken successfully.")
                else:
                    print("Failed to take snapshot.")
                time.sleep(10)  # Wait 5 minutes between polls

        # Start the thread
        thread = threading.Thread(target=polling_thread, daemon=True)
        thread.start()


@solara.component
def Page():
    # Set the dark theme
    solara.lab.theme.dark = True
    sensor_manager = SensorManager()

    # Reactive variable to trigger UI refresh
    refresh_trigger = solara.use_reactive(0)

    # Unconditionally call the thread initialization logic in a hook
    solara.use_effect(
        lambda: initialize_polling_thread(sensor_manager, refresh_trigger),
        dependencies=[],  # Run once on component mount
    )

    # UI Components
    SensorDisplay.CombinedGraph()
    with solara.ColumnsResponsive():
        SensorDisplay.SnapshotButton()
        solara.Info(f"Refresh Count: {refresh_trigger.value}")
        SensorDisplay.DistanceComponent()
        with solara.Card("Relay"):
            SensorDisplay.RelayButton()
