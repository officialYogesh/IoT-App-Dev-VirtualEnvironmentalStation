import os
import random
import time
import sys
from datetime import datetime
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MQTT Configuration
MQTT_BROKER = "mqtt3.thingspeak.com"
MQTT_PORT = 1883
CHANNEL_ID = os.getenv("CHANNEL_ID")
MQTT_TOPIC = f"channels/{CHANNEL_ID}/publish"
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
PUBLISH_INTERVAL = 15 * 60  # 15 minutes

class SensorSimulator:
    def __init__(self):
        self.client = None
        self.is_connected = False
        self.validate_credentials()
        self.setup_mqtt_client()

    def validate_credentials(self):
        """Validate that all required MQTT credentials are provided"""
        if not all([MQTT_USERNAME, MQTT_CLIENT_ID, MQTT_PASSWORD]):
            print("Error: Missing required MQTT credentials in .env file")
            print("Please ensure MQTT_USERNAME, MQTT_CLIENT_ID, and MQTT_PASSWORD are set")
            sys.exit(1)

    def setup_mqtt_client(self):
        """Initialize and configure the MQTT client"""
        # Create client with the configured client ID
        self.client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=True)
        
        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        
        # Set up authentication with username and password
        self.client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)

    def on_connect(self, client, userdata, flags, rc):
        """Callback when client connects to the broker"""
        if rc == 0:
            self.is_connected = True
            print(f"Connected successfully to MQTT broker at {MQTT_BROKER}")
            print(f"Using client ID: {MQTT_CLIENT_ID}")
        else:
            print(f"Connection failed with code {rc}")
            self.is_connected = False

    def on_disconnect(self, client, userdata, rc):
        """Callback when client disconnects from the broker"""
        self.is_connected = False
        if rc != 0:
            print(f"Unexpected disconnection. Code: {rc}")
        else:
            print("Disconnected successfully")

    def on_publish(self, client, userdata, mid):
        """Callback when a message is published"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Message {mid} published successfully")

    def generate_sensor_data(self):
        """Generate simulated sensor readings"""
        return {
            "temperature": round(random.uniform(-50, 50), 2),
            "humidity": round(random.uniform(0, 100), 2),
            "co2": round(random.uniform(300, 2000), 2)
        }

    def format_payload(self, data):
        """Format sensor data into ThingSpeak payload format"""
        return f"field1={data['temperature']}&field2={data['humidity']}&field3={data['co2']}"

    def connect(self):
        """Establish connection to MQTT broker"""
        try:
            print(f"Connecting to {MQTT_BROKER}...")
            print(f"Using credentials - Username: {MQTT_USERNAME}, Client ID: {MQTT_CLIENT_ID}")
            self.client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            self.client.loop_start()
        except Exception as e:
            print(f"Failed to connect: {e}")
            sys.exit(1)

    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()

    def run(self):
        """Main loop for sensor simulation and data publishing"""
        self.connect()
        
        try:
            while True:
                if not self.is_connected:
                    print("Waiting for connection...")
                    time.sleep(1)
                    continue

                # Generate and publish sensor data
                sensor_data = self.generate_sensor_data()
                payload = self.format_payload(sensor_data)
                
                # Publish to ThingSpeak
                result = self.client.publish(MQTT_TOPIC, payload)
                if result[0] == 0:
                    print(f"Published: Temperature={sensor_data['temperature']}°C, "
                          f"Humidity={sensor_data['humidity']}%, "
                          f"CO2={sensor_data['co2']}ppm")
                else:
                    print(f"Failed to publish message. Result code: {result[0]}")

                # Wait for next publish interval
                time.sleep(PUBLISH_INTERVAL)

        except KeyboardInterrupt:
            print("\nStopping sensor simulation...")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.disconnect()
            print("Cleanup complete")

def main():
    """Main entry point"""
    print("Starting ThingSpeak MQTT Sensor Simulation")
    print(f"Channel ID: {CHANNEL_ID}")
    print(f"Broker: {MQTT_BROKER}")
    print(f"Topic: {MQTT_TOPIC}")
    print(f"Client ID: {MQTT_CLIENT_ID}")
    print(f"Username: {MQTT_USERNAME}")
    
    simulator = SensorSimulator()
    simulator.run()

if __name__ == "__main__":
    main()