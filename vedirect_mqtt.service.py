import time
import json
import paho.mqtt.client as mqtt
from vedirect import VEDirect

# Configuration
VEDIRECT_PORT = "/dev/ttyUSB0"
VEDIRECT_TIMEOUT = 60
MQTT_BROKER = "localhost"  # Update to your broker address
MQTT_PORT = 1883
MQTT_TOPIC = "vedirect/attributes"
PUBLISH_INTERVAL = 15  # seconds

# Initialize VEDirect
ve = VEDirect(VEDIRECT_PORT, VEDIRECT_TIMEOUT)

# Initialize MQTT client
mqtt_client = mqtt.Client(protocol=mqtt.MQTTv311)

# Optional: Set username and password if required
# mqtt_client.username_pw_set("your-username", "your-password")

# Connect to the MQTT broker
def connect_mqtt():
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("Connected to MQTT broker")
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        exit(1)

# Main loop to read attributes and publish to MQTT
def main():
    connect_mqtt()

    while True:
        try:
            # Read attributes from VEDirect
            attributes = ve.read_data_single()

            # Convert attributes to JSON
            attributes_json = json.dumps(attributes)

            # Publish attributes to MQTT
            mqtt_client.publish(MQTT_TOPIC, attributes_json)
            print(f"Published: {attributes_json}")

        except Exception as e:
            print(f"Error reading or publishing data: {e}")

        # Wait for the next publish interval
        time.sleep(PUBLISH_INTERVAL)

if __name__ == "__main__":
    main()
