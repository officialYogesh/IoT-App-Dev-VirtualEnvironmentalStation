import os
import random
import time
import sys
import warnings
from datetime import datetime
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

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
PUBLISH_INTERVAL = 15 #* 60  # 15 minutes

def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*50)
    print(f"{text:^50}")
    print("="*50 + "\n")

def print_status(text, value=None):
    """Print a formatted status message"""
    if value is not None:
        print(f"{text:<30}: {value}")
    else:
        print(text)

def print_sensor_data(data):
    """Print formatted sensor data"""
    print("\n" + "-"*50)
    print("SENSOR READINGS")
    print("-"*50)
    print(f"Temperature: {data['temperature']:>6}°C")
    print(f"Humidity:    {data['humidity']:>6}%")
    print(f"CO2:        {data['co2']:>6}ppm")
    print("-"*50 + "\n")

class SensorSimulator:
    def __init__(self):
        self.client = None
        self.is_connected = False
        self.validate_credentials()
        self.setup_mqtt_client()

    def validate_credentials(self):
        """Validate that all required MQTT credentials are provided"""
        if not all([MQTT_USERNAME, MQTT_CLIENT_ID, MQTT_PASSWORD]):
            print_header("ERROR: Missing Credentials")
            print_status("Please ensure the following are set in your .env file:")
            print_status("- MQTT_USERNAME")
            print_status("- MQTT_CLIENT_ID")
            print_status("- MQTT_PASSWORD")
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
            print_header("CONNECTION SUCCESSFUL")
            print_status("Broker", MQTT_BROKER)
            print_status("Client ID", MQTT_CLIENT_ID)
        else:
            print_header("CONNECTION FAILED")
            print_status("Error Code", rc)
            self.is_connected = False

    def on_disconnect(self, client, userdata, rc):
        """Callback when client disconnects from the broker"""
        self.is_connected = False
        if rc != 0:
            print_header("UNEXPECTED DISCONNECTION")
            print_status("Error Code", rc)
        else:
            print_header("DISCONNECTED")
            print_status("Clean disconnection completed")

    def on_publish(self, client, userdata, mid):
        """Callback when a message is published"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print_status(f"Message {mid} published", timestamp)

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
            print_header("CONNECTING TO MQTT BROKER")
            print_status("Broker", MQTT_BROKER)
            print_status("Username", MQTT_USERNAME)
            print_status("Client ID", MQTT_CLIENT_ID)
            self.client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            self.client.loop_start()
        except Exception as e:
            print_header("CONNECTION ERROR")
            print_status("Error", str(e))
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
                    print_status("Waiting for connection...")
                    time.sleep(1)
                    continue

                # Generate and publish sensor data
                sensor_data = self.generate_sensor_data()
                payload = self.format_payload(sensor_data)
                
                # Publish to ThingSpeak
                result = self.client.publish(MQTT_TOPIC, payload)
                if result[0] == 0:
                    print_sensor_data(sensor_data)
                else:
                    print_header("PUBLISH FAILED")
                    print_status("Error Code", result[0])

                # Wait for next publish interval
                time.sleep(PUBLISH_INTERVAL)

        except KeyboardInterrupt:
            print_header("STOPPING SIMULATION")
            print_status("User requested stop")
        except Exception as e:
            print_header("ERROR")
            print_status("An error occurred", str(e))
        finally:
            self.disconnect()
            print_header("CLEANUP COMPLETE")

def main():
    """Main entry point"""
    print_header("THINGSPEAK MQTT SENSOR SIMULATION")
    print_status("Channel ID", CHANNEL_ID)
    print_status("Broker", MQTT_BROKER)
    print_status("Topic", MQTT_TOPIC)
    print_status("Client ID", MQTT_CLIENT_ID)
    print_status("Username", MQTT_USERNAME)
    print_status("Publish Interval", f"{PUBLISH_INTERVAL/60} minutes")
    
    simulator = SensorSimulator()
    simulator.run()

if __name__ == "__main__":
    main()