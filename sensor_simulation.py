import random
import time
import requests

# Replace with your Write API Key from ThingSpeak
WRITE_API_KEY = "YOUR_WRITE_API_KEY"

def simulate_sensor_values():
    # Generate random sensor readings
    temperature = round(random.uniform(-50, 50), 2)  # Temperature in Celsius
    humidity = round(random.uniform(0, 100), 2)       # Humidity in %
    co2 = round(random.uniform(300, 2000), 2)           # CO₂ in ppm
    return temperature, humidity, co2

def publish_to_thingspeak(temperature, humidity, co2):
    # ThingSpeak update URL
    url = "https://api.thingspeak.com/update"
    # Construct the parameters with the sensor values
    params = {
        "api_key": WRITE_API_KEY,
        "field1": temperature,
        "field2": humidity,
        "field3": co2
    }
    # Send a GET request to ThingSpeak
    response = requests.get(url, params=params)
    return response.text

def main():
    while True:
        temperature, humidity, co2 = simulate_sensor_values()
        print(f"Publishing data -> Temperature: {temperature} °C, Humidity: {humidity} %, CO2: {co2} ppm")
        result = publish_to_thingspeak(temperature, humidity, co2)
        if result == "0":
            print("Error: Data not updated. Check your API Key and channel settings.")
        else:
            print(f"Data successfully updated. Entry ID: {result}")
        # Publish data every 15 minutes
        time.sleep(60*15)

if __name__ == "__main__":
    main()