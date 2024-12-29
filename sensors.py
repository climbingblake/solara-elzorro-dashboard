import solara
import busio
import board
import lgpio
import time
from datetime import datetime
from tank import Tank
from config import Config, SolaraStore
from database import DatabaseManager
from stts22h import STTS22H
import asyncio


# HOST = "10.0.0.92"  # Replace with your Wemos device's IP address
# PORT = 6053             # Default API port for ESPHome
# PASSWORD = ""  # Replace with your ESPHome API password

class SensorManager:
    def __init__(self):
        try:
            # Initialize temp_sensor
            i2c = busio.I2C(board.SCL, board.SDA)
            temp_sensor = STTS22H(i2c)
        except Exception as e:
            solara.Error("Couldnt Find IC2 STT52H")
        try:
            handle = lgpio.gpiochip_open(0)  # Open GPIO chip
            lgpio.gpio_claim_output(handle, Config.TRIG_PIN)
            lgpio.gpio_claim_input(handle, Config.ECHO_PIN)
            lgpio.gpio_write(handle, Config.TRIG_PIN, 0)  # Set TRIG low
            lgpio.gpiochip_close(handle)      # Close GPIO chip
        except Exception as e:
            solara.Error("Couldnt Find GPIO")

        self.db_manager = DatabaseManager()
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.temp_sensor = self.initialize_temp_sensor()

    def initialize_temp_sensor(self):
        try:
            return STTS22H(self.i2c)
        except Exception as e:
            print(f"Failed to initialize temperature sensor: {e}")
            solara.Error(f"Failed to initialize temperature sensor: {e}")
            return None

    def take_snapshot(self):
        try:
            if not self.temp_sensor:
                raise Exception("Temperature sensor not initialized")

            distance = self.measure_distance()
            if distance is None:
                raise Exception("Faed to measure distance")

            tank = Tank(SolaraStore.tank_diameter.value, SolaraStore.tank_height.value)
            gallons = tank.gallons_remaining(float(distance))

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            temperature = self.temp_sensor.temperature



            with self.db_manager as cursor:
                cursor.execute(
                    "INSERT INTO snapshots (timestamp, temperature, gallons) VALUES (?, ?, ?)",
                    (timestamp, temperature, gallons)
                )

            self.update_snapshot_count()
            return True

        except Exception as e:
            print(f"Failed to take snapshot: {e}")
            solara.Error(f"Failed to take snapshot: {e}")
            return False

    def update_snapshot_count(self):
        recorded_data, _ = self.db_manager.fetch_records('snapshots')
        SolaraStore.numb_snapshots.set(len(recorded_data))

    @staticmethod
    def measure_distance():
        handle = None
        try:
            handle = lgpio.gpiochip_open(0)
            lgpio.gpio_claim_output(handle, Config.TRIG_PIN)
            lgpio.gpio_claim_input(handle, Config.ECHO_PIN)
            lgpio.gpio_write(handle, Config.TRIG_PIN, 0)
            time.sleep(0.5)

            lgpio.gpio_write(handle, Config.TRIG_PIN, 1)
            time.sleep(0.00001)
            lgpio.gpio_write(handle, Config.TRIG_PIN, 0)

            timeout = time.time() + 1
            pulse_start = pulse_end = 0
            while lgpio.gpio_read(handle, Config.ECHO_PIN) == 0 and time.time() < timeout:
                pulse_start = time.time()
            while lgpio.gpio_read(handle, Config.ECHO_PIN) == 1 and time.time() < timeout:
                pulse_end = time.time()

            if pulse_end == 0 or pulse_start == 0:
                return None

            pulse_duration = pulse_end - pulse_start

            measured_distance = round(pulse_duration * 17150, 2)

            print(f"----------{measured_distance}------------")
            SolaraStore.distance_value.set(measured_distance if measured_distance is not None else "Error measuring distance")

            # asyncio.ensure_future(Sensor.publish_distance(measured_distance))


            return measured_distance

        except Exception as e:
            print("An error occurred:", e)
            return None

        finally:
            if handle is not None:
                lgpio.gpiochip_close(handle)


    @staticmethod
    async def publish_distance(measured_distance):
        """Asynchronous function to publish distance to MQTT."""
        try:
            async with Client("localhost:1883") as client:
                await client.publish("watertank/distance", payload=measured_distance)
                print(f"Published distance: {measured_distance}")
        except Exception as e:
            print("Failed to publish distance:", e)