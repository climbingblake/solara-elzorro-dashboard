import aioesphomeapi
import asyncio

async def main():
    """Connect to an ESPHome device and get temperature and humidity."""

    # ESPHome device details
    host = "10.0.0.92"  # Replace with your ESPHome device IP
    port = 6053
    password = ""  # Replace with your password, if any

    # Establish connection to the ESPHome API
    api = aioesphomeapi.APIClient(host, port, password)
    await api.connect(login=True)

    # Get device info for debugging
    # print(f"API Version: {api.api_version}")
    device_info = await api.device_info()
    # print(f"Device Info: {device_info}")

    # Fetch all entities (sensors, switches, etc.)
    entities_response = await api.list_entities_services()

    # Flatten nested lists into a single list
    entities = []
    for item in entities_response:
        if isinstance(item, list):
            entities.extend(item)
        else:
            entities.append(item)

    # print("Entities:")
    #for entity in entities:
    #    if hasattr(entity, "name") and hasattr(entity, "key"):
            # print(f"{entity.name} (Key: {entity.key})")

    # Identify temperature and humidity sensor keys
    temp_key = None
    hum_key = None
    for entity in entities:
        if isinstance(entity, aioesphomeapi.SensorInfo):
            if "temp" in entity.name.lower():
                temp_key = entity.key
                # print(f"Temperature sensor found: {entity.name} (Key: {entity.key})")
            elif "humi" in entity.name.lower():
                hum_key = entity.key
                # print(f"Humidity sensor found: {entity.name} (Key: {entity.key})")

    # Ensure the keys were found
    if temp_key is None or hum_key is None:
        # print("Error: Temperature or humidity sensor not found!")
        await api.disconnect()
        return None, None

    # Define callback to capture state updates
    temperature = None
    humidity = None

    def on_state(state):
        nonlocal temperature, humidity
        if state.key == temp_key:
            temperature = state.state
            # print(f"Temperature updated: {temperature} °C")
        elif state.key == hum_key:
            humidity = state.state
            # print(f"Humidity updated: {humidity} %")

    # Register the callback for state updates
    api.subscribe_states(on_state)  # Removed `await` here

    # Wait for state updates to be received
    await asyncio.sleep(1)  # Adjust wait time if necessary

    # Disconnect from the ESPHome API
    await api.disconnect()

    # Return final temperature and humidity values
    return temperature, humidity

def GetConditions():
    # asyncio.run(main)
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "asyncio.run() cannot be called" in str(e):
            # If an event loop is already running, use `asyncio.create_task()`
            loop = asyncio.get_event_loop()
            return loop.create_task(main())
        else:
            raise

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     temperature, humidity = loop.run_until_complete(main())

#     # Handle results
#     if temperature is None or humidity is None:
#         print("Failed to retrieve temperature or humidity.")
#     else:
#         print(f"Final Temperature: {temperature} °C")
#         print(f"Final Humidity: {humidity} %")


