import solara
import asyncio
import paho.mqtt as mqtt
import json
from aiomqtt import Client


class DHT22:
    def __init__(self):

        self.humidity = solara.use_reactive("No data")
        self.temperature = solara.use_reactive("No data")

        async def handle_conditions():
            try:
                async with Client("10.0.0.58") as client:
                    # Subscribe to all topics
                    await client.subscribe("conditions/#")
                    print("Subscribed to topic: conditions/#")

                    # Properly handle incoming messages
                    async for message in client.messages:
                        print(f"Message received on topic {message.topic}: {message.payload.decode()}")
                        payload = message.payload.decode()
                        payload = json.loads(message.payload.decode())
                        #print(message.topic)
                        if str(message.topic) == "conditions/dht22":
                            hum = payload['humidity']
                            temp = payload['temp']
                            self.humidity.set(hum)
                            self.temperature.set(temp)
            except asyncio.CancelledError:
                print("Task was cancelled.")
            except Exception as e:
                print(f"Error in MQTT handler: {e}")

        def start_mqtt_handler():
            """Starts the MQTT handler and returns a cleanup function."""
            task = asyncio.create_task(handle_conditions())

            # Cleanup function to cancel the task
            def cleanup():
                print("Cleaning up the task...")
                if not task.done():
                    task.cancel()

            return cleanup

        # Start the MQTT handler and provide cleanup
        solara.use_effect(start_mqtt_handler, [])


        # TBD somehow be able to pass solara reactives between methods and files
        # this code works, but I cant put these lines in a new display method
        # since humidity and temerature are not retained
    def SimpleDisplay(self):
        solara.Text(f"Current Humidity: {self.humidity.value}")
        solara.Text(f"Current Temperature: {self.temperature.value}")

