from sensors import SensorManager

if __name__ == "__main__":
    sensor_manager = SensorManager()
    success = sensor_manager.take_snapshot()
    if success:
        print("Snapshot successfully taken.")
    else:
        print("Failed to take snapshot.")









