import os
import sys
import warnings
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import logging

# Suppress all warnings including urllib3
warnings.filterwarnings("ignore", category=Warning)
# Specifically suppress urllib3 warnings
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.ERROR)

# Load environment variables
load_dotenv()

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
    print(f"Temperature: {data['field1']:>6}°C")
    print(f"Humidity:    {data['field2']:>6}%")
    print(f"CO2:        {data['field3']:>6}ppm")
    print("-"*50 + "\n")

def create_line_charts(feeds):
    """Create line charts for historical sensor data"""
    # Prepare data
    timestamps = []
    temperatures = []
    humidity = []
    co2 = []
    
    for feed in feeds:
        timestamp = datetime.strptime(feed['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        timestamps.append(timestamp)
        temperatures.append(float(feed['field1']))
        humidity.append(float(feed['field2']))
        co2.append(float(feed['field3']))
    
    # Create figure with three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
    
    # Temperature chart
    ax1.plot(timestamps, temperatures, 'r-', label='Temperature')
    ax1.set_title('Temperature Over Time')
    ax1.set_ylabel('Temperature (°C)')
    ax1.grid(True)
    ax1.legend()
    
    # Humidity chart
    ax2.plot(timestamps, humidity, 'b-', label='Humidity')
    ax2.set_title('Humidity Over Time')
    ax2.set_ylabel('Humidity (%)')
    ax2.grid(True)
    ax2.legend()
    
    # CO2 chart
    ax3.plot(timestamps, co2, 'g-', label='CO2')
    ax3.set_title('CO2 Levels Over Time')
    ax3.set_ylabel('CO2 (ppm)')
    ax3.grid(True)
    ax3.legend()
    
    # Rotate x-axis labels for better readability
    for ax in [ax1, ax2, ax3]:
        plt.setp(ax.get_xticklabels(), rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the chart
    plt.savefig('historical_readings.png')
    print_status("Charts saved as 'historical_readings.png'")

def get_historical_data(channel_id, hours=5):
    """Fetch historical data from ThingSpeak channel"""
    try:
        # Calculate the time range
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        # ThingSpeak API endpoint for historical data
        url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
        params = {
            'start': start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end': end_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if not data['feeds']:
            print_header("NO DATA AVAILABLE")
            print_status(f"No sensor data found for the last {hours} hours")
            return None
            
        return data['feeds']
        
    except requests.exceptions.RequestException as e:
        print_header("ERROR FETCHING DATA")
        print_status("Failed to connect to ThingSpeak API", str(e))
        return None
    except Exception as e:
        print_header("ERROR")
        print_status("An unexpected error occurred", str(e))
        return None

def display_historical_data(feeds):
    """Display historical data in a formatted way"""
    if not feeds:
        return
        
    print_header("HISTORICAL SENSOR DATA")
    print_status("Time Range", f"Last {len(feeds)} readings")
    
    for feed in feeds:
        timestamp = datetime.strptime(feed['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        print_status("\nTimestamp", timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        print_sensor_data(feed)
    
    # Create line charts
    create_line_charts(feeds)

def main():
    """Main entry point"""
    # Get channel ID from environment or command line
    channel_id = os.getenv("CHANNEL_ID")
    if not channel_id:
        if len(sys.argv) > 1:
            channel_id = sys.argv[1]
        else:
            print_header("ERROR: Missing Channel ID")
            print_status("Please provide the channel ID either:")
            print_status("1. Set CHANNEL_ID in your .env file")
            print_status("2. Pass it as a command line argument")
            print_status("\nUsage: python display_historical_data.py <channel_id>")
            sys.exit(1)

    print_header("FETCHING HISTORICAL SENSOR DATA")
    print_status("Channel ID", channel_id)
    print_status("Time Range", "Last 5 hours")
    
    # Fetch and display the historical data
    historical_data = get_historical_data(channel_id)
    if historical_data:
        display_historical_data(historical_data)

if __name__ == "__main__":
    main() 